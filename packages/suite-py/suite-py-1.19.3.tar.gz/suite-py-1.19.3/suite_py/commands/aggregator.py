# -*- coding: utf-8 -*-
import sys
import re

from halo import Halo

from suite_py.lib import logger
from suite_py.lib.handler.captainhook_handler import CaptainHook
from suite_py.lib.handler import prompt_utils


class Aggregator:
    def __init__(self, config, show_list, change):
        self._captainhook = CaptainHook(config)
        self._show_list = show_list
        self._change = change

    def run(self):
        if self._show_list:
            self._list_aggregators()
            return

        if self._change:
            aggregator = self._select_aggregator()
            address = prompt_utils.ask_questions_input(
                "Insert QA url or press enter to set staging URL: ",
                default_text="staging.prima.it",
            )

            if address.startswith("http"):
                address = re.sub(r"https?://?", "", address)

            change_request = self._captainhook.change_aggregator(aggregator, address)
            self._handle_captainhook_response(change_request, aggregator, address)

    def _handle_captainhook_response(self, request, aggregator, address):
        if request.status_code == 200:
            change_request = request.json()
            if change_request["success"]:
                logger.info(f"CNAME updated! Now {aggregator} is pointing to {address}")
            else:
                cases = {
                    "cloudflare_error": "Error during Cloudflare invocation.",
                    "unknown_dns_record": "Impossible to find DNS record associated with aggregator.",
                    "unknown_aggregator": "Aggregator not found.",
                    "invalid_qa_address": "The QA address does not meet the requirements.",
                }
                logger.error(cases.get(change_request["error"], "unknown error"))
        else:
            logger.error("An error has occurred on Captainhook.")

    def _select_aggregator(self):
        with Halo(text="Loading aggregators...", spinner="dots", color="magenta"):
            choices = [
                {"name": agg["name"], "value": agg["name"]}
                for agg in self._captainhook.aggregators().json()
            ]
        if choices:
            choices.sort(key=lambda x: x["name"])
            return prompt_utils.ask_choices("Select aggregator: ", choices)

        logger.error("There are no aggregators on Captainhook.")
        sys.exit(-1)

    def _list_aggregators(self):
        with Halo(text="Loading...", spinner="dots", color="magenta"):
            aggregators = self._captainhook.aggregators()

        if aggregators.status_code != 200:
            logger.error("Unable to retrieve the list of aggregators.")
            return

        message = "\n".join(
            [f"* {a['name']:>20} => {a['content']:>32}" for a in aggregators.json()]
        )

        logger.info(f"\nAvailable aggregators:\n{message}\n")
