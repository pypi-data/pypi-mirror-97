import fastapi
import uvicorn
import logging
import traceback
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer
from opencensus.trace.samplers import ProbabilitySampler
from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES
from opencensus.ext.azure.trace_exporter import AzureExporter
from starlette.middleware.base import BaseHTTPMiddleware

from energinetml.settings import (
    PACKAGE_REQUIREMENT,
    APP_INSIGHT_INSTRUMENTATION_KEY,
)

from .predicting import PredictionController


logger = logging.getLogger(__name__)

# if APP_INSIGHT_INSTRUMENTATION_KEY:
#     exporter =


async def azureAppInsightsMiddleware(request: fastapi.Request, call_next):
    conn = f'InstrumentationKey={APP_INSIGHT_INSTRUMENTATION_KEY}'
    tracer = Tracer(
        exporter=AzureExporter(connection_string=conn),
        sampler=ProbabilitySampler(rate=1.0),
    )

    with tracer.span("main") as span:
        span.span_kind = SpanKind.SERVER

        tracer.add_attribute_to_current_span(
            attribute_key=COMMON_ATTRIBUTES['HTTP_URL'],
            attribute_value=str(request.url))

        try:
            response = await call_next(request)
        except Exception as e:
            logger.exception('Prediction failed')
            tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES['HTTP_STATUS_CODE'],
                attribute_value=500)
            tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES['HTTP_URL'],
                attribute_value=str(request.url))
            tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES['ERROR_NAME'],
                attribute_value=e.__class__.__name__)
            tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES['ERROR_MESSAGE'],
                attribute_value=traceback.format_exc())
            return fastapi.Response(status_code=500)
        else:
            tracer.add_attribute_to_current_span(
                attribute_key=COMMON_ATTRIBUTES['HTTP_STATUS_CODE'],
                attribute_value=response.status_code)
            return response


def create_app(model, trained_model, model_version=None):
    """
    :param energinetml.Model model:
    :param energinetml.TrainedModel trained_model:
    :param typing.Optional[str] model_version:
    :rtype: fastapi.FastAPI
    """
    controller = PredictionController(
        model=model,
        trained_model=trained_model,
        model_version=model_version,
    )

    async def predict_http_endpoint(
            request: controller.request_model,
            response: fastapi.Response):
        """
        TODO Write me!
        TODO /docs not working?
        """
        response.headers['X-sdk-version'] = str(PACKAGE_REQUIREMENT)

        return controller.predict(request)

    # -- Setup app -----------------------------------------------------------

    app = fastapi.FastAPI(
        title=model.name,
        description=(
            'Model version %s' % model_version
            if model_version
            else None
        )
    )

    if APP_INSIGHT_INSTRUMENTATION_KEY:
        app.add_middleware(
            middleware_class=BaseHTTPMiddleware,
            dispatch=azureAppInsightsMiddleware,
        )

    app.router.add_api_route(
        path='/predict',
        methods=['POST'],
        endpoint=predict_http_endpoint,
        response_model=controller.response_model,

        # TODO:
        summary='Predict using the model',
        description='TODO',
    )

    return app


def run_predict_api(model, trained_model, host, port, model_version=None):
    """
    :param energinetml.Model model:
    :param energinetml.TrainedModel trained_model:
    :param str host:
    :param int port:
    :param typing.Optional[str] model_version:
    """
    app = create_app(
        model=model,
        trained_model=trained_model,
        model_version=model_version,
    )

    uvicorn.run(app, host=host, port=port)
