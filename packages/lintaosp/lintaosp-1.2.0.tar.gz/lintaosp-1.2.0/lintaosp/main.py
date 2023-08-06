# -*- coding: utf-8 -*-

import sys

from lintaosp.aosp.aosp import Aosp, AospException
from lintaosp.cmd.argument import Argument
from lintaosp.cmd.banner import BANNER
from lintaosp.config.config import Config, ConfigException
from lintaosp.flow.flow import Flow, FlowException
from lintaosp.logger.logger import Logger
from lintaosp.queue.queue import Queue, QueueException


def main():
    print(BANNER)

    argument = Argument()
    arg = argument.parse(sys.argv)

    try:
        config = Config()
        config.config_file = arg.config_file
        config.lint_project = arg.lint_project
        config.listen_url = arg.listen_url
        config.output_file = arg.output_file
    except ConfigException as e:
        Logger.error(str(e))
        return -1

    try:
        aosp = Aosp(config)
    except AospException as e:
        Logger.error(str(e))
        return -2

    Logger.info("lint running")

    if len(config.listen_url) != 0:
        try:
            flow = Flow(config)
            flow.run(aosp.routine)
        except FlowException as e:
            Logger.error(str(e))
            return -3
    else:
        try:
            queue = Queue(config)
            queue.run(aosp.routine, config.lint_project)
        except QueueException as e:
            Logger.error(str(e))
            return -4

    Logger.info("lint exiting")

    return 0
