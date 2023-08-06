import click
import pprint

from energinetml.core.logger import MetricsLogger


class AzureMlLogger(MetricsLogger):
    def __init__(self, run):
        """
        :param azureml.core.Run run:
        """
        self.run = run

    def echo(self, s):
        click.echo(s)

    def log(self, name, value):
        self.run.log(name, value)
        self.echo('LOG: %s = %s' % (name, value))

    def tag(self, key, value):
        self.run.tag(key, value)
        self.echo('TAG: %s = %s' % (key, value))

    def table(self, name, dict_of_lists, echo=True):
        list_of_dicts = [dict(zip(dict_of_lists, t))
                         for t in zip(*dict_of_lists.values())]

        for d in list_of_dicts:
            self.run.log_table(name, d)

        if echo:
            # TODO print actual table
            self.echo('%s:' % name)
            self.echo(pprint.PrettyPrinter(indent=4).pformat(dict_of_lists))

    def dataframe(self, name, df):
        df = df.reset_index()
        self.table(name, df.to_dict(orient='list'), echo=False)
        self.echo(df.to_string())
