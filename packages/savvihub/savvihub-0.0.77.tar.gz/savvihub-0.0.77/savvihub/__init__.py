import os

from savvihub.api.savvihub import SavviHubClient
from savvihub.experiment import Experiment

experiment_context = None


def log(step, row=None):
    """Log a metric during a SavviHub experiment.

    This function must be called on the SavviHub infrastructure to log the metric.
    If not executed on SavviHub's infrastructure, this function has no effect.

    :param step: a step(positive integer) for each iteration (required)
    :param row: a dictionary to log
    """
    global experiment_context
    if experiment_context is None:
        experiment_id = os.environ.get('SAVVIHUB_EXPERIMENT_ID', None)
        access_token = os.environ.get('SAVVIHUB_ACCESS_TOKEN', None)
        if experiment_id is None or access_token is None:
            return

        client = SavviHubClient(auth_header={'Authorization': f'Token {access_token}'})
        experiment_context = Experiment.from_given(experiment_id, client)

    experiment_context.log(row=row, step=step)
