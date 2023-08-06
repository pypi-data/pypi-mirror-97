# -*- coding: utf-8 -*-

import os

from lintaosp.aosp.sdk import Sdk
from lintaosp.config.config import ConfigFile
from lintaosp.printer.printer import Printer


class AospException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Aosp(object):
    def __init__(self, config):
        if config is None:
            raise AospException("config invalid")
        self._config = config
        self._spec = config.config_file.get(ConfigFile.SPEC, None)
        if self._spec is None:
            raise AospException("spec invalid")
        self._instance = self._instantiate()

    def _dump(self, data):
        printer = Printer()
        printer.run(data=data, name=self._config.output_file, append=False)

    def _instantiate(self):
        buf = {}
        if Sdk.__name__.lower() in self._spec:
            buf[Sdk.__name__.lower()] = Sdk(self._spec[Sdk.__name__.lower()])
        return buf

    def routine(self, project):
        if not isinstance(project, str) or not os.path.exists(project):
            raise AospException("project invalid")
        buf = {}
        for key in self._spec.keys():
            if key in self._instance.keys():
                buf[key] = self._instance[key].run(project)
        if len(self._config.output_file) != 0:
            self._dump(buf)
        return buf
