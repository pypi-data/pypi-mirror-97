# -*- encoding: utf-8 -*-
import subprocess
import yaml

from suite_py.lib import logger
from suite_py.lib.handler.git_handler import GitHandler

REPO = "qainit"


def get_qa_projects(config):
    git = GitHandler(REPO, config)
    git.check_repo_cloned()
    git.sync()
    with open(f"{git.get_path()}/projects.yml", "r") as file:
        branches_obj = yaml.safe_load(file.read())

    return list(branches_obj.keys())


def qainit_deploy(args, config):
    qainit_dir = f"{config.user['projects_home']}/{REPO}"
    with open(f"{qainit_dir}/suitepy-projects.yml", "w+") as file:
        file.write(args)

    # development only
    # twig_command = f"{config.user['projects_home']}/twig-binaries/bin/twig-feature"
    return subprocess.run(
        # [twig_command, "suite", "deploy"], # development only
        ["twig", "feature", "suite", "deploy"],
        cwd=qainit_dir,
        check=True,
    )


def qainit_shutdown(youtrack_id, config):
    git = GitHandler(REPO, config)
    git.check_repo_cloned()
    git.sync()
    branch = git.search_remote_branch(f"*{youtrack_id}*")
    if branch:
        git.checkout(branch)
        git.commit("shutdown", dummy=True)
        git.push(branch)

    else:
        logger.warning(
            "I could not find a QA env for this card, if the QA exists, please shut it down manually.\nDevops are watching you! ( •͡˘ _•͡˘)"
        )
