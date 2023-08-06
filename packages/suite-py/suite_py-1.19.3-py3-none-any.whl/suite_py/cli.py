#! -*- encoding: utf-8 -*-
import os
import sys

import click
from autoupgrade import Package

from suite_py.__version__ import __version__
from suite_py.commands.ask_review import AskReview
from suite_py.commands.check import Check
from suite_py.commands.create_branch import CreateBranch
from suite_py.commands.create_qa import CreateQA
from suite_py.commands.delete_qa import DeleteQA
from suite_py.commands.release import Release
from suite_py.commands.deploy import Deploy
from suite_py.commands.generator import Generator
from suite_py.commands.id import ID
from suite_py.commands.ip import IP
from suite_py.commands.merge_pr import MergePR
from suite_py.commands.open_pr import OpenPR
from suite_py.commands.project_lock import ProjectLock
from suite_py.commands.status import Status
from suite_py.commands.aggregator import Aggregator
from suite_py.commands.secret import Secret
from suite_py.lib.config import Config
from suite_py.lib.handler import git_handler as git
from suite_py.lib.handler import prompt_utils
from suite_py.lib.tokens import Tokens


@click.group()
@click.option(
    "--project",
    type=click.Path(exists=True),
    default=os.getcwd(),
    help="Path of the project to run the command on (the default is current directory)",
)
@click.option(
    "--timeout",
    type=click.INT,
    help="Timeout in seconds for Captainhook operations",
)
@click.pass_context
def main(ctx, project, timeout):
    Package("suite_py").upgrade()
    print(f"v{__version__}")

    config = Config()

    if not git.is_repo(project):
        print(f"the folder {project} is not a git repo")
        sys.exit(-1)

    if not os.path.basename(project) in os.listdir(config.user["projects_home"]):
        print(f"the folder {project} is not in {config.user['projects_home']}")
        sys.exit(-1)

    if not config.user.get("skip_confirmation", False) and not prompt_utils.ask_confirm(
        f"Do you want to continue on project {os.path.basename(project)}?"
    ):
        sys.exit()

    ctx.ensure_object(dict)
    ctx.obj["project"] = os.path.basename(project)
    if timeout:
        config.user["captainhook_timeout"] = timeout
    ctx.obj["config"] = config
    ctx.obj["tokens"] = Tokens()
    os.chdir(os.path.join(config.user["projects_home"], ctx.obj["project"]))


@main.command(
    "create-branch", help="Create local branch and set the YouTrack card in progress"
)
@click.option("--card", type=click.STRING, help="YouTrack card number (ex. PRIMA-123)")
@click.pass_obj
def cli_create_branch(obj, card):
    CreateBranch(obj["project"], card, obj["config"], obj["tokens"]).run()


@main.command("lock", help="Lock project on staging or prod")
@click.argument(
    "environment", type=click.Choice(("staging", "production", "deploy", "merge"))
)
@click.pass_obj
def cli_lock_project(obj, environment):
    ProjectLock(obj["project"], environment, "lock", obj["config"]).run()


@main.command("unlock", help="Unlock project on staging or prod")
@click.argument(
    "environment", type=click.Choice(("staging", "production", "deploy", "merge"))
)
@click.pass_obj
def cli_unlock_project(obj, environment):
    ProjectLock(obj["project"], environment, "unlock", obj["config"]).run()


@main.command("open-pr", help="Open a PR on GitHub")
@click.pass_obj
def cli_open_pr(obj):
    OpenPR(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("ask-review", help="Requests a PR review")
@click.pass_obj
def cli_ask_review(obj):
    AskReview(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("create-qa", help="Create QA env (integration with qainit)")
@click.pass_obj
def cli_create_qa(obj):
    CreateQA(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("delete-qa", help="Delete QA env (integration with qainit)")
@click.pass_obj
def cli_delete_qa(obj):
    DeleteQA(obj["project"], obj["config"], obj["tokens"]).run()


@main.command(
    "merge-pr", help="Merge the selected branch to master if all checks are OK"
)
@click.pass_obj
def cli_merge_pr(obj):
    MergePR(obj["project"], obj["config"], obj["tokens"]).run()


@main.group("release", help="Manage releases")
def release():
    pass


@release.command("create", help="Create a github release")
@click.option("--deploy", is_flag=True, help="Trigger deploy after release creation")
@click.pass_obj
def cli_release_create(obj, deploy):
    Release(
        "create", obj["project"], obj["config"], obj["tokens"], flags={"deploy": deploy}
    ).run()


@release.command("deploy", help="Deploy a github release")
@click.pass_obj
def cli_release_deploy(obj):
    Release("deploy", obj["project"], obj["config"], obj["tokens"]).run()


@release.command("rollback", help="Rollback a deployment")
@click.pass_obj
def cli_release_rollback(obj):
    Release("rollback", obj["project"], obj["config"], obj["tokens"]).run()


@main.command("deploy", help="Deploy master branch in production")
@click.pass_obj
def cli_deploy(obj):
    Deploy(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("status", help="Current status of a project")
@click.pass_obj
def cli_status(obj):
    Status(obj["project"], obj["config"]).run()


@main.command("check", help="Verify authorisations for third party services")
@click.pass_obj
def cli_check(obj):
    Check(obj["config"], obj["tokens"]).run()


@main.command("id", help="Get the ID of the hosts where the task is running")
@click.argument("environment", type=click.Choice(("staging", "production")))
@click.pass_obj
def cli_id(obj, environment):
    ID(obj["project"], environment).run()


@main.command("ip", help="Get the IP addresses of the hosts where the task is running")
@click.argument("environment", type=click.Choice(("staging", "production")))
@click.pass_obj
def cli_ip(obj, environment):
    IP(obj["project"], environment).run()


@main.command("generator", help="Generate different files from templates")
@click.pass_obj
def cli_generator(obj):
    Generator(obj["project"], obj["config"], obj["tokens"]).run()


@main.command("aggregator", help="Manage CNAMEs of aggregators in QA envs")
@click.option("-l", "--list", "show_list", required=False, count=True)
@click.option("-c", "--change", "change", required=False, count=True)
@click.pass_obj
def cli_aggregator(obj, show_list, change):
    Aggregator(obj["config"], show_list, change).run()


@main.command(
    "secret", help="Manage secrets grants in multiple countries (aws-vault needed)"
)
@click.option("-c", "--create", "create_action", required=False, count=True)
@click.option("-g", "--grant", "grant_action", required=False, count=True)
@click.option("-b", "--base-profile", "base_profile", required=False)
@click.pass_obj
def cli_secret(obj, create_action, grant_action, base_profile):
    Secret(
        obj["project"], obj["config"], create_action, grant_action, base_profile
    ).run()
