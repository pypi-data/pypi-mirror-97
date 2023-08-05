
class SubmitContext(object):
    def submit_model(self):
        raise NotImplementedError

    def wait_for_completion(self):
        raise NotImplementedError

    def download_files(self):
        raise NotImplementedError
