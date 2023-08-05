import requirements
import os

from spell.api.models import RunRequest
from spell.cli.exceptions import ExitException


def get_conda_contents(conda_file):
    if conda_file is not None:
        if not os.path.isfile(conda_file):
            raise ExitException("--conda-file file not found: " + conda_file)
        with open(conda_file) as conda_file:
            return conda_file.read()


# returns a list of pip packages
def get_requirements_file(requirements_file):
    if requirements_file is None:
        return []
    pip_packages = []
    if not os.path.isfile(requirements_file):
        raise ExitException("--pip-req file not found: " + requirements_file)
    with open(requirements_file, "r") as rf:
        for req in requirements.parse(rf):
            pip_packages.append(req.line)
    return pip_packages


def get_run_request(client, kwargs):
    """Converts an python API request's kwargs to a RunRequest"""
    # grab conda env file contents
    if "conda_file" in kwargs:
        kwargs["conda_file"] = get_conda_contents(kwargs.pop("conda_file"))

    # grab pip packages from requirements file
    pip_packages = []
    if "pip_packages" in kwargs:
        pip_packages = kwargs.pop("pip_packages")
    if "requirements_file" in kwargs:
        pip_packages.extend(get_requirements_file(kwargs.pop("requirements_file")))

    # set workflow id
    if "workflow_id" not in kwargs and client.active_workflow:
        kwargs["workflow_id"] = client.active_workflow.id

    return RunRequest(run_type="user", pip_packages=pip_packages, **kwargs)


def validate_pip(pip):
    if pip.find("==") != pip.find("="):
        raise ExitException(
            f"Invalid pip dependency {pip}: = is not a valid operator. Did you mean == ?"
        )


def format_pip_apt_versions(pip, apt):
    if pip:
        for x in pip:
            validate_pip(x)
        pip = [convert_name_version_pair(x, "==") for x in pip]
    if apt:
        apt = [convert_name_version_pair(x, "=") for x in apt]
    return (pip, apt)


def convert_name_version_pair(package, separator):
    split = package.split(separator)
    return {"name": split[0], "version": split[1] if len(split) > 1 else None}
