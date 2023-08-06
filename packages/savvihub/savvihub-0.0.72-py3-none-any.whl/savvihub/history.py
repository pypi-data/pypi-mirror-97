from datetime import datetime
from typing import Dict, List

from openapi_client import ProtoExperimentMetric


class History:
    def __init__(self, experiment):
        self.experiment = experiment
        self.rows = []
        self._step_index = 0

    def update(self, client, row, step):
        """
        Update row in history
        """
        metrics: Dict[str, List[ProtoExperimentMetric]] = {}
        for k, v in row.items():
            if k in metrics:
                metrics[k].append(ProtoExperimentMetric(
                    step=step,
                    timestamp=datetime.utcnow().timestamp(),
                    value=str(v),
                ))
            else:
                metrics[k] = [ProtoExperimentMetric(
                    step=step,
                    timestamp=datetime.utcnow().timestamp(),
                    value=str(v),
                )]

        self.rows.append(row)
        client.experiment_metrics_update(self.experiment.id, metrics)
