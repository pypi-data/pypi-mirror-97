
class MetricsLogger(object):
    """
    TODO
    """

    def echo(self, s):
        """
        :param str s:
        """
        raise NotImplementedError

    def log(self, name, value):
        """
        :param str name:
        :param typing.Any value:
        """
        raise NotImplementedError

    def tag(self, key, value):
        """
        :param str key:
        :param str value:
        """
        raise NotImplementedError

    def dataframe(self, name, df):
        """
        :param str name:
        :param pandas.DataFrame df:
        """
        raise NotImplementedError
