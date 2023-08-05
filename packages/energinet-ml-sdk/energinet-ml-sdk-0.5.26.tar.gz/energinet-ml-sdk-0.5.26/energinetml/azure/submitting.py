import azureml


class AzureSubmitContext(object):

    class SubmitError(Exception):
        pass

    class FailedToWait(SubmitError):
        pass

    class FailedToDownload(SubmitError):
        pass

    def __init__(self, model, az_run):
        self.model = model
        self.az_run = az_run

    def wait_for_completion(self):
        try:
            self.az_run.wait_for_completion(show_output=True)
        except azureml.exceptions._azureml_exception.ActivityFailedException as e:
            raise self.FailedToWait(e.message)

    def download_files(self):
        self.az_run.download_files(output_directory=self.model.path)
