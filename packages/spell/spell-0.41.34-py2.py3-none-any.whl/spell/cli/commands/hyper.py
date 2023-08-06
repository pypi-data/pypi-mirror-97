import click
from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
    SPELL_INVALID_CONFIG,
)
from spell.cli.commands.run import create_run_request
from spell.cli.log import logger
from spell.cli.utils.command_options import (
    dependency_params,
    workspace_spec_params,
    machine_config_params,
    cli_params,
    description_param,
    idempotent_option,
    project_option,
    timeout_option,
    json_hyper_param_option,
    stop_condition_option,
    tensorboard_params,
    label_param,
)
from spell.cli.utils.exceptions import ParseException
from spell.cli.utils.parse_utils import (
    parse_list_params,
    parse_random_params,
    parse_bayesian_params,
    parse_conditions,
)
from spell.cli.utils import tabulate_rows, with_emoji, ellipses, group, get_or_create_project


def common_hyper_exec_options(func):
    for opt in (
        idempotent_option,
        project_option,
        machine_config_params,
        dependency_params(resource_type="hyperparameter search"),
        workspace_spec_params,
        description_param(resource_type="hyperparameter search"),
        cli_params,
        tensorboard_params,
        label_param,
    ):
        func = opt(func)
    return func


def hyper_exec_args(func):
    # Ordering here is reverse from what might be intuitive. Since
    # click.argument is meant to be used as a decorator, if the decorator
    # is ad-hoc applied to the function they get applied in the "reverse"
    # order. This ordering is required to implement
    #    COMMAND ARGS...
    # syntax as opposed to
    #    ARGS... COMMAND
    # syntax
    func = click.argument("args", nargs=-1)(func)
    return click.argument("command")(func)


def hyper_quiet_opt(func):
    return click.option("-q", "--quiet", is_flag=True, help="Suppress logging")(func)


@group(
    name="hyper",
    short_help="Create hyperparameter searches",
    help="Create hyperparameter searches on Spell",
    docs="https://spell.ml/docs/hyper_searches/"
)
@click.pass_context
def hyper(ctx):
    pass


@hyper.command(
    name="grid",
    short_help="Execute a hyperparameter grid search",
    docs="https://spell.ml/docs/hyper_searches/#performing-grid-search",
)
@hyper_exec_args
@click.option(
    "--param",
    "params",
    multiple=True,
    metavar="NAME=VALUE[,VALUE,VALUE,...]",
    help="Specify a hyperparameter for the run. A run will be created for all "
    "hyperparameter value combinations provided. NAME should appear in the "
    'COMMAND surrounded by colons (i.e., ":NAME:" to indicate where '
    "the VALUE values should be substituted when creating each run.",
)
@json_hyper_param_option
@common_hyper_exec_options
@timeout_option
@stop_condition_option
@click.pass_context
def grid(
    ctx,
    command,
    args,
    params,
    json_params,
    provider,
    machine_type,
    pip_packages,
    requirements_file,
    apt_packages,
    docker_image,
    framework,
    commit_ref,
    description,
    envvars,
    raw_resources,
    conda_file,
    force,
    verbose,
    idempotent,
    github_url,
    github_ref,
    stop_condition,
    tensorboard_dir,
    labels,
    timeout,
    project,
    **kwargs
):
    """
    Execute a hyperparameter grid search for COMMAND remotely on Spell's infrastructure

    The grid command is used to create numerous runs simultaneously to perform a hyperparameter
    grid search. A run will be created for all possible combinations of parameters provided with
    the --param option.  All other options are the same as the spell run command and will apply
    to every run created in the hyperparameter search.
    """
    logger.info("starting hyper grid command")
    try:
        params = parse_list_params(params)
    except ParseException as e:
        raise ExitException(
            click.wrap_text(
                "Incorrect formatting of param '{}', it must be NAME=VALUE[,VALUE,VALUE,...]".format(
                    e.token
                )
            ),
            SPELL_INVALID_CONFIG,
        )
    try:
        params.update(parse_list_params(json_params, is_json=True))
    except ParseException as e:
        raise ExitException(
            click.wrap_text(
                "Incorrect formatting of json param '{}', it must be a json encoded list".format(
                    e.token
                )
            ),
            SPELL_INVALID_CONFIG,
        )
    try:
        stop_conditions = parse_conditions(stop_condition)
    except ParseException as e:
        raise ExitException(e.message)
    run_req = create_run_request(
        ctx,
        command,
        args,
        machine_type,
        pip_packages,
        requirements_file,
        apt_packages,
        docker_image,
        framework,
        commit_ref,
        description,
        envvars,
        raw_resources,
        conda_file,
        force,
        verbose,
        idempotent,
        provider,
        "user",
        github_url,
        github_ref,
        timeout=timeout,
        stop_conditions=stop_conditions,
        tensorboard_dir=tensorboard_dir,
        labels=labels,
        **kwargs
    )
    client = ctx.obj["client"]

    if project:
        run_req.project_id = get_or_create_project(client, project).id

    logger.info("sending hyper search request to api")
    with api_client_exception_handler():
        hyper = client.hyper_grid_search(params, run_req)
    utf8 = ctx.obj["utf8"]
    click.echo(
        with_emoji(u"💫", "Casting hyperparameter search #{}".format(hyper.id), utf8)
        + ellipses(utf8)
    )

    # promote param names to attributes for tabulate
    for run in hyper.runs:
        run.id = str(run.id)
        for param in params:
            setattr(run, param, run.hyper_params[param])
    # display parameters and associated run IDs
    param_names = list(params.keys())
    headers = param_names + ["Run ID"]
    columns = list(params.keys()) + ["id"]
    tabulate_rows(hyper.runs, headers=headers, columns=columns)


@hyper.command(
    name="random",
    short_help="Execute a hyperparameter random search",
    docs="https://spell.ml/docs/hyper_searches/#performing-random-search",
)
@hyper_exec_args
@click.option(
    "-n",
    "--num-runs",
    "num_runs",
    required=True,
    type=int,
    prompt="Enter the total number of runs to execute",
    help="Total number of runs to create for the hyperparameter search",
)
@click.option(
    "-p",
    "--param",
    "params",
    multiple=True,
    metavar="NAME=VALUE[,VALUE,VALUE,...] | NAME=MIN:MAX[:linear|log|reverse_log[:int|float]]",
    help="Specify a hyperparameter for the run. Each run will sample this random parameter specification "
    "to determine a specific value for the run. The parameter values can be provided as either a "
    "list of values (from which one value will be randomly selected each run) or a range (MIN:MAX) "
    "and optional scaling ('linear', 'log', or 'reverse_log') and type ('int' or 'float'). "
    "If unspecified, a linear scaling and type float are assumed. NAME should appear in the "
    'COMMAND surrounded by colons (i.e., ":NAME:" to indicate where '
    "the VALUEs should be substituted when creating each run.",
)
@json_hyper_param_option
@common_hyper_exec_options
@timeout_option
@stop_condition_option
@click.pass_context
def random(
    ctx,
    command,
    args,
    num_runs,
    params,
    json_params,
    provider,
    machine_type,
    pip_packages,
    requirements_file,
    apt_packages,
    docker_image,
    framework,
    commit_ref,
    description,
    envvars,
    raw_resources,
    conda_file,
    force,
    verbose,
    idempotent,
    github_url,
    github_ref,
    stop_condition,
    tensorboard_dir,
    labels,
    timeout,
    project,
    **kwargs
):
    """
    Execute a hyperparameter random search for COMMAND remotely on Spell's infrastructure

    The random command is used to create numerous runs simultaneously to perform a hyperparameter
    search. As many runs as specified with --num-runs will be created and each hyperparameter specified with
    the --param option will be sampled to determine a specific value for each run.  All other options are the
    same as the spell run command and will apply to every run created in the hyperparameter search.
    """
    logger.info("starting hyper random command")
    try:
        params = parse_random_params(params)
    except ParseException as e:
        raise ExitException(
            click.wrap_text(
                "Incorrect formatting of param '{}', it must be NAME=VALUE[,VALUE,VALUE,...] or "
                "NAME=MIN:MAX[:linear|log|reverse_log[:int|float]]".format(e.token)
            ),
            SPELL_INVALID_CONFIG,
        )
    try:
        params.update(parse_list_params(json_params, is_json=True))
    except ParseException as e:
        raise ExitException(
            click.wrap_text(
                "Incorrect formatting of json param '{}', it must be a json encoded list".format(
                    e.token
                )
            ),
            SPELL_INVALID_CONFIG,
        )
    try:
        stop_conditions = parse_conditions(stop_condition)
    except ParseException as e:
        raise ExitException(e.message)
    run_req = create_run_request(
        ctx,
        command,
        args,
        machine_type,
        pip_packages,
        requirements_file,
        apt_packages,
        docker_image,
        framework,
        commit_ref,
        description,
        envvars,
        raw_resources,
        conda_file,
        force,
        verbose,
        idempotent,
        provider,
        "user",
        github_url,
        github_ref,
        timeout=timeout,
        stop_conditions=stop_conditions,
        tensorboard_dir=tensorboard_dir,
        labels=labels,
        **kwargs
    )
    client = ctx.obj["client"]

    if project:
        run_req.project_id = get_or_create_project(client, project).id

    logger.info("sending hyper search request to api")
    with api_client_exception_handler():
        hyper = client.hyper_random_search(params, num_runs, run_req)
    utf8 = ctx.obj["utf8"]
    click.echo(
        with_emoji(u"💫", "Casting hyperparameter search #{}".format(hyper.id), utf8)
        + ellipses(utf8)
    )

    # promote param names to attributes for tabulate
    for run in hyper.runs:
        run.id = str(run.id)
        for param in params:
            setattr(run, param, run.hyper_params[param])
    # display parameters and associated run IDs
    param_names = list(params.keys())
    headers = param_names + ["Run ID"]
    columns = list(params.keys()) + ["id"]
    tabulate_rows(hyper.runs, headers=headers, columns=columns)


@hyper.command(
    name="bayesian",
    short_help="Execute a hyperparameter bayesian search",
    docs="https://spell.ml/docs/hyper_searches/#performing-bayesian-search",
)
@hyper_exec_args
@click.option(
    "-n",
    "--num-runs",
    "num_runs",
    required=True,
    type=int,
    prompt="Enter the maximum number of runs to execute",
    help="Maximum number of runs for the hyperparameter search",
)
@click.option(
    "-r",
    "--parallel-runs",
    "parallel_runs",
    required=True,
    type=int,
    prompt="Enter the number of runs to parallelize",
    help="Number of parallel runs to use for each iteration",
)
@click.option(
    "--metric",
    "metric",
    required=True,
    type=str,
    prompt="Enter the metric to optimize",
    help="Metric name that will be used ",
)
@click.option(
    "-a",
    "--metric-agg",
    "metric_agg",
    required=True,
    type=click.Choice(["avg", "min", "max", "last"]),
    prompt="Enter the metric aggregation method",
)
@click.option(
    "-p",
    "--param",
    "params",
    multiple=True,
    metavar="NAME=MIN:MAX[:int|float]",
    help="Specify a hyperparameter for the run in the form: a range (MIN:MAX) "
    "If unspecified, type float is assumed. NAME should appear in the "
    'COMMAND surrounded by colons (i.e., ":NAME:" to indicate where '
    "the VALUEs should be substituted when creating each run.",
)
@common_hyper_exec_options
@click.pass_context
def bayesian(
    ctx,
    command,
    args,
    num_runs,
    parallel_runs,
    metric,
    metric_agg,
    params,
    provider,
    machine_type,
    pip_packages,
    requirements_file,
    apt_packages,
    docker_image,
    framework,
    commit_ref,
    description,
    envvars,
    raw_resources,
    conda_file,
    force,
    verbose,
    idempotent,
    github_url,
    github_ref,
    tensorboard_dir,
    labels,
    project,
    **kwargs
):
    """
    Execute a hyperparameter bayesian search for COMMAND remotely on Spell's infrastructure

    The bayesian command is used to create parallelized bayesian optimization hyperparameter optimization
    with num_runs number of total runs, parallelized in sets of parallel_runs
    """
    logger.info("starting hyper bayesian command")
    try:
        params = parse_bayesian_params(params)

    except ParseException as e:
        raise ExitException(
            click.wrap_text(
                "Incorrect formatting of param '{}', it must be NAME=MIN:MAX[:int|float]".format(
                    e.token
                )
            ),
            SPELL_INVALID_CONFIG,
        )
    run_req = create_run_request(
        ctx,
        command,
        args,
        machine_type,
        pip_packages,
        requirements_file,
        apt_packages,
        docker_image,
        framework,
        commit_ref,
        description,
        envvars,
        raw_resources,
        conda_file,
        force,
        verbose,
        idempotent,
        provider,
        "user",
        github_url,
        github_ref,
        tensorboard_dir=tensorboard_dir,
        labels=labels,
        **kwargs
    )
    client = ctx.obj["client"]

    if project:
        run_req.project_id = get_or_create_project(client, project).id

    logger.info("sending hyper search request to api")
    with api_client_exception_handler():
        hyper = client.hyper_bayesian_search(
            params, num_runs, parallel_runs, metric, metric_agg, run_req
        )
    utf8 = ctx.obj["utf8"]
    click.echo(
        with_emoji(u"💫", "Casting hyperparameter search #{}".format(hyper.id), utf8)
        + ellipses(utf8)
    )

    # promote param names to attributes for tabulate
    for run in hyper.runs:
        run.id = str(run.id)
        for param in params:
            setattr(run, param, run.hyper_params[param])
    # display parameters and associated run IDs
    param_names = list(params.keys())
    headers = param_names + ["Run ID"]
    columns = list(params.keys()) + ["id"]
    tabulate_rows(hyper.runs, headers=headers, columns=columns)


@hyper.command(
    name="stop",
    short_help="Stop a hyperparameter search",
    docs="https://spell.ml/docs/hyper_searches/#interrupting-a-hyperparameter-search",
)
@click.argument("hyper-search-id")
@hyper_quiet_opt
@click.pass_context
def stop(ctx, hyper_search_id, quiet):
    """
    Stop a hyperparameter search specified by HYPER-SEARCH-ID.

    All runs in the hyperparameter search that are running are sent a stop signal
    that ends current execution and transitions them to the "Saving" state.
    Stopped runs will continue to transition through the "Pushing" and "Saving" steps after stopping.
    If runs have not started yet, they are killed.  Any runs that are already in a final state are
    unaffected.
    """

    client = ctx.obj["client"]

    with api_client_exception_handler():
        logger.info("Stopping hyperparameter search {}".format(hyper_search_id))
        client.stop_hyper_search(hyper_search_id)

    if not quiet:
        click.echo("Stopping hyperparameter search {}.".format(hyper_search_id))


@hyper.command(
    name="kill",
    short_help="Kill a hyperparameter search",
    docs="https://spell.ml/docs/hyper_searches/#interrupting-a-hyperparameter-search",
)
@click.argument("hyper-search-id")
@hyper_quiet_opt
@click.pass_context
def kill(ctx, hyper_search_id, quiet):
    """
    Kill a hyperparameter search specified by HYPER-SEARCH-ID.

    All runs in the hyperparameter search are killed. Any runs that are already in a final state are
    unaffected.
    """

    client = ctx.obj["client"]

    with api_client_exception_handler():
        logger.info("Killing hyperparameter search {}".format(hyper_search_id))
        client.kill_hyper_search(hyper_search_id)

    if not quiet:
        click.echo("Killing hyperparameter search {}.".format(hyper_search_id))
