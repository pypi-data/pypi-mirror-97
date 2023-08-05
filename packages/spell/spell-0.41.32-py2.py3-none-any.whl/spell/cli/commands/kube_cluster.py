import click
from enum import Enum
from packaging import version
import os
import subprocess
import tempfile
import yaml
from spell.cli.constants import SERVING_CLUSTER_VERSION
from spell.cli.log import logger
from spell.cli.commands.cluster_aws import (
    EKS_DEFAULT_NODEGROUP_TYPE,
    eks_add_nodegroup,
    eks_scale_nodegroup,
    eks_delete_nodegroup,
    eks_update,
    eks_add_arn,
    eks_delete_cluster,
)
from spell.cli.commands.cluster_gcp import (
    GKE_DEFAULT_NODEGROUP_TYPE,
    gke_add_nodepool,
    gke_scale_nodepool,
    gke_delete_nodepool,
    gke_update,
    gke_delete_cluster,
)
import spell.cli.commands.cluster_aws as cluster_aws
import spell.cli.commands.cluster_gcp as cluster_gcp
from spell.cli.utils import (
    tabulate_rows,
    require_import,
    require_install,
    cluster_utils,
    command,
)
from spell.cli.utils.command import docs_option
from spell.cli.exceptions import api_client_exception_handler, ExitException


class ServingClusterUpgradeAction(Enum):
    CLUSTER = 1
    GRAFANA_CREDS = 2


@click.group(
    name="kube-cluster",
    short_help="Manage a serving cluster",
    help="Manage a model serving kubernetes cluster (EKS or GKE)",
)
@docs_option("https://spell.ml/docs/serving_clusters/")
@click.pass_context
def kube_cluster(ctx):
    pass


@command(
    name="kubectl", help="Issue kubectl commands against the serving cluster",
)
@click.argument("args", nargs=-1)
@click.pass_context
@cluster_utils.pass_cluster
def kubectl(ctx, cluster, args):
    serving_cluster_name = cluster.get("serving_cluster_name")
    if not serving_cluster_name:
        click.echo("No serving cluster found!")
        return

    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        for line in spell_client.cluster_kubectl(cluster["name"], args):
            click.echo(line)


@command(
    name="create",
    short_help="Sets up a GKE/EKS kubernetes cluster in your Spell VPC. Required for model serving.",
    help="""Sets up a GKE or EKS kubernetes cluster in your Spell VPC.
    This cluster is required for model serving.
    Spell will automatically create a CPU node group for you which will have at least
    one machine running at all times.""",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option("-p", "--profile", help="AWS profile to pull credentials from")
@click.option(
    "--kube-cluster-name",
    hidden=True,
    default="spell-model-serving",
    help="Name of the GKE/EKS cluster to create or the existing cluster if --use-existing",
)
@click.option(
    "--kube-cluster-domain",
    hidden=True,
    default="",
    help="If non-empty, tell the API to try to register using this as the *.spell.services subdomain",
)
@click.option(
    "--auth-api-url",
    hidden=True,
    type=str,
    help="URL of the spell API server used by Ambassador for authentication. "
    "This must be externally accessible",
)
@click.option(
    "--nodes-min",
    type=int,
    default=1,
    help="Minimum number of nodes in the model serving cluster (default 1)",
)
@click.option(
    "--nodes-max",
    type=int,
    default=2,
    help="Minimum number of nodes in the model serving cluster (default 2)",
)
@click.option(
    "--node-disk-size",
    type=int,
    default=50,
    help="Size of disks on each node in GB (default 50GB)",
)
@click.option(
    "--use-existing",
    is_flag=True,
    default=False,
    help="""This is an advanced option to use an existing EKS/GKE cluster instead of creating a new one.
    It will reapply kubernetes configurations. Because Spell sets up your cluster in a particular manner
    this option is only likely to work with clusters created exactly the way we set ours up. This flag
    is likely only valuable if you experienced an error the first time you tried to run this command,
    but the kube cluster creation succeeded.""",
)
@click.option(
    "--aws-zones",
    type=str,
    default=None,
    help="Allows AWS clusters to explicitly list the availability zones used for the EKS cluster. "
    "List the desired AZs as comma separated values, ex: 'us-east-1a,us-east-1c,us-east-1d'. "
    "NOTE: Most users will NOT have to do this. This is useful if there are problems with "
    "one or more of the AZs in the region of your cluster.",
)
@cluster_utils.for_aws(
    require_import("kubernetes", pkg_extras="cluster-aws"),
    require_install("eksctl", "kubectl", "aws-iam-authenticator"),
    cluster_utils.pass_aws_session(
        perms=[
            "Leverage eksctl to create an EKS cluster",
            "Leverage eksctl to create an auto scaling group to back the cluster",
        ]
    ),
)
@cluster_utils.for_gcp(
    require_import("kubernetes", "googleapiclient", pkg_extras="cluster-gcp"),
    require_install("gcloud", "kubectl"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.handle_aws_profile_flag,
)
def create_kube_cluster(
    ctx,
    cluster,
    kube_cluster_name,
    kube_cluster_domain,
    auth_api_url,
    nodes_min,
    nodes_max,
    node_disk_size,
    use_existing,
    aws_zones,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    """
    Deploy a GKE or EKS cluster for model serving
    by auto-detecting the cluster provider.
    """
    spell_client = ctx.obj["client"]
    if cluster["cloud_provider"] not in ["AWS", "GCP"]:
        raise ExitException("Serving clusters can only be created in AWS and GCP Spell clusters")

    click.echo("Generating default node group config...")
    default_ng_config = {
        "min_nodes": nodes_min,
        "max_nodes": nodes_max,
        "disk_size_gb": node_disk_size,
    }
    if cluster["cloud_provider"] == "AWS":
        default_ng_config["instance_type"] = EKS_DEFAULT_NODEGROUP_TYPE
        default_ng_config["name"] = "default"
    if cluster["cloud_provider"] == "GCP":
        default_ng_config["instance_type"] = GKE_DEFAULT_NODEGROUP_TYPE
        default_ng_config["name"] = "default-pool"

    # NOTE(waldo) for legacy reasons 'is_public' only controls load balancer visibility for ambassador;
    # a cluster with is_public set to 'False' will use an internal load balancer for ambassador;
    # since ambassador is used as the ingress gateway for all model servers.
    # the eks/gke cluster which is created by this setup is still a public cluster in that
    # nodes are publicly addressible; however no ports should be open + accessible to an unauthenticated party
    is_public = (
        click.prompt(
            "Would you like your model servers to be public or private? "
            "Private model servers will only be accessible from within the cluster's VPC.",
            type=click.Choice(["public", "private"]),
        ).strip()
        == "public"
    )

    serving_cluster_location = ""
    if cluster["cloud_provider"] == "GCP":
        from googleapiclient import discovery

        compute_service = discovery.build("compute", "v1", credentials=gcp_creds)
        gcp_project_name = cluster["networking"]["gcp"]["project"]
        region = cluster["networking"]["gcp"]["region"]
        serving_cluster_location = cluster_gcp.get_zone_from_region(
            compute_service, gcp_project_name, region
        )

    with api_client_exception_handler():
        spell_client.register_serving_cluster(
            cluster["name"],
            SERVING_CLUSTER_VERSION,
            is_public=is_public,
            kube_config=None,
            default_ng_config=default_ng_config,
            serving_cluster_domain=kube_cluster_domain,
            serving_cluster_name=kube_cluster_name,
            serving_cluster_status="created",
            serving_cluster_location=serving_cluster_location,
        )

    # Provision the k8s serving cluster from the cloud provider
    if cluster["cloud_provider"] == "AWS":
        # default auth_api_url to --api-url if it's not overriden by --auth-api-url
        auth_api_url = auth_api_url or ctx.obj["client_args"]["base_url"]

        if use_existing:
            click.echo("Skipping EKS cluster creation, existing contexts are:")
            cluster_utils.check_kube_context()
        else:
            cluster_aws.create_eks_cluster(
                cluster,
                aws_session.profile_name,
                kube_cluster_name,
                aws_session,
                nodes_min,
                nodes_max,
                node_disk_size,
                aws_zones,
            )

    elif cluster["cloud_provider"] == "GCP":
        from googleapiclient import discovery

        gcp_project_name = cluster["networking"]["gcp"]["project"]
        region = cluster["networking"]["gcp"]["region"]
        subnet = cluster["networking"]["gcp"]["subnet"]
        network = cluster["networking"]["gcp"]["vpc"]
        service_account = cluster["role_credentials"]["gcp"]["service_account_id"]

        if not use_existing:
            cluster_gcp.create_gke_cluster(
                kube_cluster_name,
                gcp_project_name,
                service_account,
                serving_cluster_location,
                nodes_min,
                nodes_max,
                node_disk_size,
                network,
                subnet,
            )
        else:
            if not click.confirm("Are you sure you want to use {}?".format(kube_cluster_name)):
                raise ExitException(
                    "Please run without --use-existing or specify a different --kube-cluster-name"
                )
            cmd = [
                "gcloud",
                "container",
                "clusters",
                "get-credentials",
                "--project",
                gcp_project_name,
                "--zone",
                serving_cluster_location,
                kube_cluster_name,
            ]
            subprocess.check_call(cmd)

    # Generate kubeconfig
    if cluster["cloud_provider"] == "AWS":
        with tempfile.NamedTemporaryFile(mode="r", suffix=".yaml") as f:
            cmd = (
                "eksctl",
                "utils",
                "write-kubeconfig",
                "--profile",
                aws_session.profile_name,
                "--cluster",
                kube_cluster_name,
                "--kubeconfig",
                f.name,
            )
            try:
                subprocess.check_call(cmd)
            except Exception as e:
                raise ExitException("Retrieving kubeconfig failed. Error was: {}".format(e))
            kubecfg_yaml = f.read()
    elif cluster["cloud_provider"] == "GCP":
        with tempfile.NamedTemporaryFile(mode="r", suffix=".yaml") as f:
            cmd = (
                "gcloud",
                "container",
                "clusters",
                "get-credentials",
                kube_cluster_name,
                "--zone",
                serving_cluster_location,
                "--project",
                gcp_project_name,
            )
            env = os.environ.copy()
            env["KUBECONFIG"] = f.name
            try:
                subprocess.check_call(cmd, env=env)
            except Exception as e:
                raise ExitException("Retrieving kubeconfig failed. Error was: {}".format(e))
            parsed_yaml = yaml.safe_load(f)

        # update kubeconfig to use the custom `gcp-svc` auth-provider
        if (
            "users" not in parsed_yaml
            or len(parsed_yaml["users"]) != 1
            or "user" not in parsed_yaml["users"][0]
            or "auth-provider" not in parsed_yaml["users"][0]["user"]
        ):
            raise Exception("Unexpected kubeconfig yaml generated from gcloud command")
        parsed_yaml["users"][0]["user"]["auth-provider"] = {
            "name": "gcp-svc",
            "config": {"service-acct": service_account},
        }
        kubecfg_yaml = yaml.dump(parsed_yaml, default_flow_style=False)

    # update the API, again
    with api_client_exception_handler():
        spell_client.register_serving_cluster(
            cluster["name"],
            SERVING_CLUSTER_VERSION,
            is_public=is_public,
            kube_config=kubecfg_yaml,
            default_ng_config=default_ng_config,
            serving_cluster_domain=kube_cluster_domain,
            serving_cluster_name=kube_cluster_name,
            serving_cluster_status="provisioned",
        )

    if cluster["cloud_provider"] == "AWS":
        cluster_aws.eks_configure_k8s(
            ctx, aws_session, cluster, auth_api_url, kube_cluster_name, aws_zones, is_public
        )
    elif cluster["cloud_provider"] == "GCP":
        cluster_gcp.gke_configure_k8s(
            ctx, gcp_project_name, kube_cluster_name, service_account, cluster, is_public
        )

    cluster_utils.echo_delimiter()
    grafana_password = cluster_utils.prompt_grafana_password()
    cluster_utils.update_grafana_configuration(cluster, grafana_password)

    cluster_utils.echo_delimiter()
    with api_client_exception_handler():
        status_code = spell_client.register_serving_cluster(
            cluster["name"],
            SERVING_CLUSTER_VERSION,
            is_public=is_public,
            kube_config=kubecfg_yaml,
            default_ng_config=default_ng_config,
            serving_cluster_domain=kube_cluster_domain,
            serving_cluster_name=kube_cluster_name,
            serving_cluster_status="ready",
        )
        if status_code == 202:
            click.echo("please wait a few minutes for DNS entries to propagate.")

    cluster_utils.echo_delimiter()
    cluster_utils.print_grafana_credentials(cluster, grafana_password)

    cluster_utils.echo_delimiter()

    if is_public:
        click.echo("Checking health of TLS ...")
        try:
            kubectl("-n", "ambassador", "get", "secrets/ambassador-certs")
        except Exception:
            logger.warn(
                "Model servers may not be securely reachable over HTTPS for the next 15 minutes."
                + "If this does not self-resolve, please contact Spell"
            )

    click.echo("Cluster setup complete!")


@command(
    name="update",
    short_help="Update an existing GKE/EKS kubernetes cluster in your Spell VPC.",
    help="""Update an existing GKE/EKS kubernetes cluster in your Spell VPC.""",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p", "--profile", help="AWS profile to pull credentials from",
)
@click.option(
    "--kube-cluster-name",
    hidden=True,
    default="spell-model-serving",
    help="Name of the GKE/EKS cluster to update",
)
@click.option(
    "--auth-api-url",
    hidden=True,
    type=str,
    help="URL of the spell API server used by Ambassador for authentication. "
    "This must be externally accessible",
)
@click.option(
    "--aws-zones",
    type=str,
    default=None,
    help="Allows AWS clusters to explicitly list the availability zones used for the EKS cluster. "
    "List the desired AZs as comma separated values, ex: 'us-east-1a,us-east-1c,us-east-1d'. "
    "NOTE: Most users will NOT have to do this. This is useful if there are problems with "
    "one or more of the AZs in the region of your cluster.",
)
@click.option(
    "-f", "--force", is_flag=True, help="Force a first-time update",
)
@click.option("--update-grafana-password", is_flag=True, help="Just update Grafana password.")
@cluster_utils.for_aws(
    require_import("kubernetes", pkg_extras="cluster-aws"),
    require_install("kubectl", "aws-iam-authenticator"),
    cluster_utils.pass_aws_session(perms=["Use kubectl to modify your EKS cluster"]),
)
@cluster_utils.for_gcp(
    require_import("kubernetes", "googleapiclient", pkg_extras="cluster-gcp"),
    require_install("gcloud", "kubectl"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.handle_aws_profile_flag,
)
def update_kube_cluster(
    ctx,
    cluster,
    kube_cluster_name,
    auth_api_url,
    aws_zones,
    force,
    update_grafana_password,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    cluster_utils.check_kube_context()  # TODO(waldo): Replace this check with a --kube-context flag + click confirm
    current_version = cluster.get("serving_cluster_version")
    upgrade_action = (
        ServingClusterUpgradeAction.GRAFANA_CREDS
        if update_grafana_password
        else ServingClusterUpgradeAction.CLUSTER
    )
    print_grafana_creds = False

    # Pre-upgrade 'migrations'

    if upgrade_action == ServingClusterUpgradeAction.CLUSTER:
        if current_version and version.parse(current_version) < version.parse("0.10.0"):
            click.echo("This update adds support for Grafana.")
            grafana_password = cluster_utils.prompt_grafana_password()

        _perform_kube_cluster_upgrade(
            ctx,
            cluster,
            kube_cluster_name,
            auth_api_url,
            aws_zones,
            force,
            aws_session=aws_session,
            gcp_project=gcp_project,
            gcp_creds=gcp_creds,
        )
        if current_version and version.parse(current_version) < version.parse("0.10.0"):
            cluster_utils.update_grafana_configuration(cluster, grafana_password)
            print_grafana_creds = True

    elif upgrade_action == ServingClusterUpgradeAction.GRAFANA_CREDS:
        if not current_version:
            raise ExitException(
                "Grafana is not installed on this cluster. \
                Try running `spell kube-cluster update` without --update-password."
            )
        grafana_password = cluster_utils.prompt_grafana_password()
        cluster_utils.update_grafana_configuration(cluster, grafana_password)
        print_grafana_creds = True

    if print_grafana_creds:
        cluster_utils.print_grafana_credentials(cluster, grafana_password)


def _perform_kube_cluster_upgrade(
    ctx,
    cluster,
    kube_cluster_name,
    auth_api_url,
    aws_zones,
    force,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    if not cluster.get("serving_cluster_name"):
        raise SystemExit(
            "Model serving is not enabled for this cluster; please run `spell kube-cluster create`."
        )
    current_version = cluster.get("serving_cluster_version")
    if not current_version:
        if not force:
            raise ExitException(
                "This is the first time update-kube-cluster has been run for this serving cluster."
                + " If your cluster was created before 09/16/2020, please upgrade by"
                + " using `delete-kube-cluster` and `create-kube-cluster` instead. Use --force to bypass."
            )
        click.echo(
            "Upgrading serving cluster version to {}. Hang tight!".format(SERVING_CLUSTER_VERSION)
        )
    elif (
        current_version
        and version.parse(current_version).major != version.parse(SERVING_CLUSTER_VERSION).major
    ):
        raise ExitException(
            (
                "This update is a major update (moving from {} to {}). Use `delete-kube-cluster`"
                + " and `create-kube-cluster` to continue."
            ).format(current_version, SERVING_CLUSTER_VERSION)
        )
    elif current_version:
        if not force and not click.confirm(
            "This will upgrade serving cluster version to {}, from {}. Continue?".format(
                SERVING_CLUSTER_VERSION, current_version
            )
        ):
            return

    if cluster["cloud_provider"] == "AWS":
        kubecfg_yaml, _ = eks_update(
            ctx, aws_session, cluster, auth_api_url, kube_cluster_name, aws_zones
        )
    elif cluster["cloud_provider"] == "GCP":
        kubecfg_yaml = gke_update(
            ctx, gcp_project, gcp_creds, cluster, auth_api_url, kube_cluster_name,
        )
    else:
        raise ExitException("Unsupported cloud provider")

    cluster_utils.finalize_kube_cluster()

    spell_client = ctx.obj["client"]
    click.echo("Sending update notification to Spell...")
    with api_client_exception_handler():
        # TODO: move update request to its own endpoint separate from register
        spell_client.register_serving_cluster(
            cluster["name"],
            SERVING_CLUSTER_VERSION,
            is_public=cluster["is_serving_cluster_public"],
            kube_config=kubecfg_yaml,
            default_ng_config=None,
            serving_cluster_name=kube_cluster_name,
            serving_cluster_status="ready",
        )
    click.echo(f"Successfully updated serving cluster to version {SERVING_CLUSTER_VERSION}!")
    if not current_version:
        logger.warn(
            "If you encounter issues after update, try deleting and recreating your cluster."
        )


@command(
    name="delete", help="Delete your EKS/GKE kubernetes cluster", hidden=True,
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p", "--profile", help="AWS profile to pull credentials from",
)
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(perms=["Leverage eksctl to delete the model serving cluster"]),
)
@cluster_utils.for_gcp(
    require_install("gcloud"), cluster_utils.handle_aws_profile_flag,
)
def delete_kube_cluster(ctx, cluster, aws_session=None):
    serving_cluster_name = cluster.get("serving_cluster_name")
    if not serving_cluster_name:
        click.echo("No serving cluster found, nothing to do!")
        return

    if cluster["cloud_provider"] == "AWS":
        eks_delete_cluster(aws_session.profile_name, serving_cluster_name)
    if cluster["cloud_provider"] == "GCP":
        project_id = cluster["networking"]["gcp"]["project"]
        gke_delete_cluster(project_id, cluster)

    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        spell_client.deregister_serving_cluster(cluster["name"])
    click.echo("Cluster delete complete!")


@command(
    name="add-user",
    help="Grant another AWS User in your account permissions to manage your kube cluster. "
    "These permissions are required for anyone to update the cluster or create/remove node groups. "
    "The user must be in the same account you use to manage this cluster, "
    "which we will deduce from the AWS profile you provide (you will be prompted to confirm).",
)
@click.pass_context
@click.argument("user")
@cluster_utils.pass_cluster
@click.option("-p", "--profile", help="AWS profile to pull credentials from")
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(
        perms=["Leverage eksctl to grant an AWS IAM User kube admin privileges"]
    ),
)
def kube_cluster_add_user(ctx, user, cluster, aws_session=None):
    if cluster["cloud_provider"] == "GCP":
        raise ExitException("This command is only intended for AWS")
    if not cluster.get("serving_cluster_name"):
        raise ExitException(
            "No kube cluster found. You can run 'spell kube-cluster create' to make one"
        )

    sts = aws_session.client("sts")
    identity = sts.get_caller_identity()
    account_id = identity.get("Account")
    if not account_id:
        raise ExitException("Unable to determine your AWS account from your profile")
    if not click.confirm(
        "Grant user {} from account {} the ability to manage your kube cluster?".format(
            user, account_id
        )
    ):
        return

    arn = "arn:aws:iam::{}:user/{}".format(account_id, user)
    eks_add_arn(aws_session.profile_name, cluster, arn)

    click.echo("{} added!".format(user))


# Node-groups
@click.group(
    name="node-group",
    short_help="Manage kube cluster node groups",
    help="Manage node groups used for model serving cluster nodes\n\n"
    "With no subcommand, display all your node groups",
    invoke_without_command=True,
)
@click.pass_context
@cluster_utils.pass_cluster
def node_group(ctx, cluster):
    pass


@click.command(name="list", short_help="Display all your node groups")
@docs_option("https://spell.ml/docs/serving_clusters/#listing-node-groups")
@click.pass_context
@cluster_utils.pass_cluster
def node_group_list(ctx, cluster):
    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        node_groups = spell_client.get_node_groups(cluster["name"])
    if node_groups:

        def prettify_instance_type(instance_type, accels, is_spot):
            type_str = instance_type or "Custom"
            accels_str = ""
            if accels:
                accel_strs = []
                for accel in accels:
                    accel_type = accel["type"]
                    # GCP accelerator types start with "nvidia-tesla-" so we can trim the prefix
                    if accel_type.startswith("nvidia-tesla-"):
                        accel_type = accel_type[len("nvidia-tesla-") :]
                    accel_strs.append("{}x{}".format(accel_type, accel["count"]))
                accels_str = "+" + ",".join(accel_strs)
            cluster_spot_name = "preemptible" if cluster["cloud_provider"] == "GCP" else "spot"
            spot_str = " ({})".format(cluster_spot_name) if is_spot else ""
            return "{}{}{}".format(type_str, accels_str, spot_str)

        tabulate_rows(
            [
                (
                    sg["name"],
                    prettify_instance_type(sg["instance_type"], sg["accelerators"], sg["is_spot"]),
                    sg["disk_size_gb"],
                    sg["min_nodes"],
                    sg["max_nodes"],
                )
                for sg in node_groups
            ],
            headers=["NAME", "INSTANCE TYPE", "DISK SIZE", "MIN NODES", "MAX NODES"],
        )
    else:
        click.echo("No node groups found for cluster {}".format(cluster["name"]))


@click.command(name="add", short_help="Add a new node group to a Spell model serving cluster")
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p",
    "--profile",
    help="Specify an AWS profile to pull credentials from to perform the NodeGroup create operation",
)
@click.option(
    "--name", required=True, help="Name of the node group",
)
@click.option(
    "--instance-type", help="Instance type to use for the nodes",
)
@click.option(
    "--accelerator",
    "accelerators",
    multiple=True,
    metavar="NAME[:COUNT]",
    help="(GCP only) Accelerator to attach to nodes, can be specified multiple times for multiple accelerator types",
)
@click.option(
    "--min-nodes", type=int, help="Minimum number of autoscaled nodes in the node group",
)
@click.option(
    "--max-nodes", type=int, help="Maximum number of autoscaled nodes in the node group",
)
@click.option(
    "--spot", is_flag=True, default=None, help="Use spot instances for node group nodes",
)
@click.option(
    "--disk-size", type=int, help="Size of disks on each node in GB",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True, dir_okay=False),
    help="Path to file containing eksctl NodeGroup or GKE node pool spec. Note this is "
    "an advanced option for users who want to specify a custom node group or node pool configuration.",
)
@cluster_utils.for_aws(
    cluster_utils.pass_aws_session(
        perms=["Leverage eksctl to create a new autoscaling group to back the node group"],
    ),
)
@cluster_utils.for_gcp(
    require_import("googleapiclient.discovery", pkg_extras="cluster-gcp"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.handle_aws_profile_flag,
)
@docs_option("https://spell.ml/docs/serving_clusters/#creating-node-groups")
def node_group_add(
    ctx,
    cluster,
    name,
    instance_type,
    accelerators,
    min_nodes,
    max_nodes,
    spot,
    disk_size,
    config_file,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    """
    Deploy a GKE node pool or eksctl node group for model serving
    """
    spell_client = ctx.obj["client"]

    accel_configs = ",".join(accelerators)

    config_contents = None
    if config_file:
        with open(config_file) as f:
            config_contents = f.read()

    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    if config_contents is None:
        click.echo("Retrieving config...")
        with api_client_exception_handler():
            config = spell_client.generate_node_group_config(
                cluster["name"],
                name,
                instance_type,
                accel_configs,
                min_nodes,
                max_nodes,
                spot,
                disk_size,
            )

    if cluster["cloud_provider"] == "AWS":
        eks_add_nodegroup(name, config, aws_session.profile_name)
    elif cluster["cloud_provider"] == "GCP":
        # External cluster service acct credentials given to nodes in the new node group
        gcp_service_account = cluster["role_credentials"]["gcp"]["service_account_id"]
        gke_add_nodepool(name, config, gcp_service_account, gcp_creds)
    else:
        raise ExitException("Cluster has invalid provider {}".format(cluster["cloud_provider"]))

    with api_client_exception_handler():
        spell_client.create_node_group(cluster["name"], name, config)
    click.echo("Successfully created node group {}!".format(name))


@click.command(
    name="scale", short_help="Adjust minimum and maximum node counts for a given node group",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p",
    "--profile",
    help="Specify an AWS profile to pull credentials from to perform the NodeGroup scale operation",
)
@click.option(
    "--min-nodes", type=int, help="Minimum number of autoscaled nodes in the node group",
)
@click.option(
    "--max-nodes", type=int, help="Maximum number of autoscaled nodes in the node group",
)
@click.argument("node_group_name")
@cluster_utils.for_gcp(
    require_import("googleapiclient.discovery", pkg_extras="cluster-gcp"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.handle_aws_profile_flag,
)
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(
        perms=[
            "Retrieve the EC2 autoscaling group corresponding to the node group",
            "Adjust the MinSize and MaxSize of the autoscaling group",
        ],
    ),
)
@docs_option("https://spell.ml/docs/serving_clusters/#scaling-node-groups")
def node_group_scale(
    ctx,
    cluster,
    node_group_name,
    min_nodes,
    max_nodes,
    aws_session=None,
    gcp_project=None,
    gcp_creds=None,
):
    """
    Adjust autoscaling min/max nodes for a node group
    """
    if min_nodes is None and max_nodes is None:
        raise click.UsageError("One of --min-nodes or --max-nodes must be specified")

    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        node_group = spell_client.get_node_group(cluster["name"], node_group_name)

    if node_group.is_default and max_nodes is not None and max_nodes < 1:
        raise ExitException(
            'Cannot scale default node group "{}" to below 1 node'.format(node_group_name)
        )

    # Special-case scaling GPU node group types to be manually scaled until GPU HPA
    # is implemented
    is_gpu_type = False
    if cluster["cloud_provider"] == "AWS":
        is_gpu_type = cluster_utils.is_gpu_instance_type(node_group.instance_type)
    elif cluster["cloud_provider"] == "GCP":
        is_gpu_type = bool(node_group.accelerators)
    if is_gpu_type:
        msg = "Autoscaling is not yet supported for GPU types."
        if max_nodes:
            msg += " Use the --min-nodes flag exclusively to manually scale the node group."
            raise click.UsageError(msg)
        if cluster["cloud_provider"] == "GCP" and min_nodes == 0:
            msg += " Max nodes cannot be set to 0, consider deleting the node group instead."
            msg += " Setting min nodes to 0 and max nodes to 1."
            logger.warning(msg)
            max_nodes = 1
        else:
            msg += " Statically scaling the node group to {} nodes.".format(min_nodes)
            logger.warning(msg)
            max_nodes = min_nodes

    min_nodes = node_group.min_nodes if min_nodes is None else min_nodes
    max_nodes = node_group.max_nodes if max_nodes is None else max_nodes
    if cluster["cloud_provider"] == "AWS":
        eks_scale_nodegroup(aws_session, cluster, node_group_name, min_nodes, max_nodes)
    elif cluster["cloud_provider"] == "GCP":
        gke_scale_nodepool(gcp_creds, node_group, min_nodes, max_nodes)
    else:
        raise ExitException("Cluster has invalid provider {}".format(cluster["cloud_provider"]))

    with api_client_exception_handler():
        spell_client.scale_node_group(cluster["name"], node_group_name, min_nodes, max_nodes)
    click.echo("Successfully scaled node group {}!".format(node_group_name))


@click.command(
    name="delete", short_help="Delete a node group",
)
@click.pass_context
@cluster_utils.pass_cluster
@click.option(
    "-p", "--profile", help="AWS profile to pull credentials from",
)
@click.argument("node_group_name")
@cluster_utils.for_aws(
    require_install("eksctl"),
    cluster_utils.pass_aws_session(
        perms=["Leverage eksctl to delete the autoscaling group backing the node group"],
    ),
)
@cluster_utils.for_gcp(
    require_import("googleapiclient.discovery", pkg_extras="cluster-gcp"),
    cluster_utils.pass_gcp_project_creds,
    cluster_utils.handle_aws_profile_flag,
)
@docs_option("https://spell.ml/docs/serving_clusters/#deleting-node-groups")
def node_group_delete(
    ctx, cluster, node_group_name, aws_session=None, gcp_project=None, gcp_creds=None,
):
    """
    Delete a node group
    """
    spell_client = ctx.obj["client"]

    cluster_utils.validate_org_perms(spell_client, ctx.obj["owner"])

    with api_client_exception_handler():
        node_group = spell_client.get_node_group(cluster["name"], node_group_name)

    if node_group.is_default:
        raise ExitException('Cannot delete cluster default node group "{}"'.format(node_group_name))

    active_servers = [
        server
        for server in node_group.model_servers
        if server.status in ["running", "starting", "updating"]
    ]

    if len(active_servers) > 0:
        server_names = [server.server_name for server in active_servers]
        if not click.confirm(
            "These active model servers will be stopped: ({}). Are you sure?".format(
                ", ".join(server_names)
            )
        ):
            click.echo("Aborted.")
            return
        for model_server in active_servers:
            spell_client.stop_model_server(model_server.server_name)

    if cluster["cloud_provider"] == "AWS":
        eks_delete_nodegroup(aws_session.profile_name, node_group)
    elif cluster["cloud_provider"] == "GCP":
        gke_delete_nodepool(gcp_creds, node_group)
    else:
        raise ExitException("Cluster has invalid provider {}".format(cluster["cloud_provider"]))

    with api_client_exception_handler():
        spell_client.delete_node_group(cluster["name"], node_group_name)
    click.echo("Successfully deleted node group {}!".format(node_group_name)),


kube_cluster.add_command(create_kube_cluster)
kube_cluster.add_command(update_kube_cluster)
kube_cluster.add_command(delete_kube_cluster)
kube_cluster.add_command(kube_cluster_add_user)
kube_cluster.add_command(kubectl)

kube_cluster.add_command(node_group)
node_group.add_command(node_group_list)
node_group.add_command(node_group_add)
node_group.add_command(node_group_scale)
node_group.add_command(node_group_delete)
