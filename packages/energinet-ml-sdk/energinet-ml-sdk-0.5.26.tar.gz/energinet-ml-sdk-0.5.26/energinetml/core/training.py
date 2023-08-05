

class TrainingError(Exception):
    pass


class AbstractTrainingContext(object):
    """
    TODO
    """
    def train_model(self, model, tags, *args, **kwargs):
        """
        :param energinetml.Model model:
        :param typing.Dict[str, typing.Any] tags:
        :rtype: energinetml.TrainedModel
        """
        pass

    def save_output_files(self, model):
        pass


def requires_parameter(name, typ):
    def requires_parameter_decorator(func):
        def requires_parameter_inner(*args, **kwargs):
            if name not in kwargs:
                raise TrainingError('Missing parameter "%s"' % name)
            try:
                kwargs[name] = typ(kwargs.get(name))
            except ValueError:
                raise TrainingError((
                    'Parameter "%s" could not be cast to type %s: %s'
                                    ) % (name, typ.__name__, kwargs.get(name)))
            return func(*args, **kwargs)

        return requires_parameter_inner
    return requires_parameter_decorator
