# -*- coding: utf-8 -*-
"""
celery cli handlers help module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase


@celery_cli_handler()
class HelpCLIHandler(CeleryCLIHandlerBase):
    """
    help cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of HelpCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.HELP)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        return super()._inject_params(params)
