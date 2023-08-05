from savvihub.common.context import Context


global_context = None


def log(step, row=None):
    """
    step: a step for each iteration (required)
    row: a dictionary to log
    """
    global global_context
    if global_context is None:
        global_context = Context(experiment_required=True)
    global_context.experiment.log(row=row, step=step)
