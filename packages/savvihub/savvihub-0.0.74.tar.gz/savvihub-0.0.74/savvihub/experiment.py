import collections
import numbers

import six

from openapi_client import ResponseExperimentInfo
from savvihub import history
from savvihub.exceptions import ArgumentException


class Experiment:
    def __init__(self, experiment: ResponseExperimentInfo, client):
        self.id = experiment.id
        self.client = client
        self._history = None

    @classmethod
    def from_given(cls, experiment_id, client):
        return cls(client.experiment_id_read(experiment_id), client)

    @property
    def history(self):
        if not self._history:
            self._history = history.History(self)
        return self._history

    def log(self, row, *, step=None):
        if not isinstance(row, collections.Mapping):
            raise ArgumentException(".log() takes a dictionary as a parameter")

        if any(not isinstance(key, six.string_types) for key in row.keys()):
            raise ArgumentException("The key of dictionary in .log() parameter must be str")

        for k in row.keys():
            if not k:
                raise ArgumentException("Logging empty key is not supported")

        if not isinstance(step, numbers.Number):
            raise ArgumentException(f"Step must be a number, not {type(step)}")
        if step is None or step < 0:
            raise ArgumentException(f"Step must be a positive integer, not {step}")
        if not isinstance(type(step), int):
            step = int(round(step))

        self.history.update(self.client, row, step)
