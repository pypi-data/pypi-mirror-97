from energinetml import Model, TrainedModel, main


class NewModel(Model):

    def train(self, datasets, logger, seed, **params):
        """
        :param energinetml.MLDataStore datasets:
        :param energinetml.MetricsLogger logger:
        :param typing.Any seed:
        :param typing.Dict[str, typing.Any] params:
        :rtype: energinetml.TrainedModel
        """

        # TODO Train your model here and return it

        raise NotImplementedError

        return TrainedModel()

    def predict(self, trained_model, input_data, identifier):
        """
        :param energinetml.TrainedModel trained_model:
        :param energinetml.PredictionInput input_data:
        :param str identifier:
        :rtype: typing.List[typing.Any]
        """

        # TODO Predict using the trained model and return the prediction

        raise NotImplementedError


# Reference your model class and name it "model"
model = NewModel

# Allow to invoke the CLI by executing this file (do not remove these lines)
if __name__ == '__main__':
    main()
