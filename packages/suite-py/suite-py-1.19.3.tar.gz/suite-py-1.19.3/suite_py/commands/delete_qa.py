# -*- coding: utf-8 -*-
import sys

from suite_py.lib import logger
from suite_py.lib.handler.git_handler import GitHandler
from suite_py.lib.handler.youtrack_handler import YoutrackHandler
from suite_py.lib.qainit import qainit_shutdown


class DeleteQA:
    def __init__(self, project, config, tokens):
        self._project = project
        self._config = config
        self._youtrack = YoutrackHandler(config, tokens)
        self._git = GitHandler(project, config)

    def run(self):
        branch_name = self._git.current_branch_name()

        logger.info("Shutting down QA if it exists...")
        qainit_shutdown(branch_name, self._config)

        sys.exit()
