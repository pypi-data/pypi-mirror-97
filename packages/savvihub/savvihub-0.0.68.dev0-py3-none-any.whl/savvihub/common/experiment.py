import collections
import numbers

import six

from savvihub import history
from savvihub.api.types import SavviHubExperiment


class Experiment(SavviHubExperiment):
    def __init__(self, experiment: SavviHubExperiment, client):
        super().__init__(experiment.dict)
        self.client = client
        self._history = None

    @classmethod
    def from_given(cls, experiment, client):
        experiment = cls(experiment, client)
        return experiment

    @property
    def history(self):
        if not self._history:
            self._history = history.History(self)
        return self._history

    def log(self, row, *, step=None):
        if not isinstance(row, collections.Mapping):
            raise ValueError(".log() takes a dictionary as a parameter")

        if any(not isinstance(key, six.string_types) for key in row.keys()):
            raise ValueError("The key of dictionary in .log() parameter must be str")

        for k in row.keys():
            if not k:
                raise ValueError("Logging empty key is not supported")

        if not isinstance(step, numbers.Number):
            raise ValueError(f"Step must be a number, not {type(step)}")
        if step < 0:
            raise ValueError(f"Step must be a positive integer, not {step}")
        if not isinstance(type(step), int):
            step = int(round(step))

        self.history.update(self.client, row, step)
