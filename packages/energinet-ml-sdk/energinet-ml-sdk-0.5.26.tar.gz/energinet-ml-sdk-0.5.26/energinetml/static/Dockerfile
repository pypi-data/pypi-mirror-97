FROM python:3.8

ARG TRAINED_MODEL_PATH
ARG EXTRA_INDEX_URL
ARG PACKAGE_VERSION
ARG MODEL_VERSION

COPY . /model
COPY $TRAINED_MODEL_PATH /model/outputs/model.pkl

WORKDIR /model

RUN apt-get update
RUN pip3 install --upgrade twine wheel setuptools pip
RUN pip3 install --upgrade -r /model/requirements.txt --extra-index-url=$EXTRA_INDEX_URL

EXPOSE 80

CMD energinetml model serve --host 0.0.0.0 --port 80 --model-file /model/outputs/model.pkl --model-version $MODEL_VERSION
