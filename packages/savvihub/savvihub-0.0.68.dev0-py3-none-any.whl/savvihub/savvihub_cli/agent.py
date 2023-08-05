import json
import subprocess
import time

import typer

from savvihub import Context
from savvihub.common.constants import DEBUG

agent_app = typer.Typer()


@agent_app.callback(hidden=True)
def main():
    return


@agent_app.command()
def collect_system_metrics(
    metrics_collector_binary: str = typer.Option("system-metrics-collector", "--collector-binary"),
    prometheus_url: str = typer.Option(..., "--prometheus-url"),
    paths: str = typer.Option(None, "--paths"),
    collect_period: int = typer.Option(5, "--collect-period", min=5),
):
    context = Context(experiment_required=True)
    client = context.authorized_client

    while True:
        args = [
            "-prometheus-url",
            prometheus_url,
            "-experiment",
            context.experiment.slug,
        ]
        if paths:
            args.extend(['-paths', paths])

        p = subprocess.Popen([
            metrics_collector_binary,
            *args,
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        if not stdout:
            continue

        if DEBUG:
            print("system-metrics-collector: stdout", stdout)
            print("system-metrics-collector: stderr", stderr)

        metrics = {}
        rows = json.loads(stdout)
        if not rows:
            time.sleep(collect_period)
            continue

        for row in rows:
            metrics[row['name']] = [{
                'timestamp': float(row['timestamp']),
                'value': row['value'],
            }]

        client.experiment_system_metrics_update(context.experiment.id, metrics)
        time.sleep(collect_period)
