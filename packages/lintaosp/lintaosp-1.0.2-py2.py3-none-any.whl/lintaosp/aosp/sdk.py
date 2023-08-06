# -*- coding: utf-8 -*-

import subprocess
import sys

from lintaosp.aosp.abstract import AospAbstract
from lintaosp.proto.proto import Format, Type

CHECK_SEP = ","

LINT_LEN_MIN = 3
LINT_SEP = ":"
LINT_TYPE = [Type.ERROR, Type.INFO, Type.WARN]


class SdkException(Exception):
    def __init__(self, info):
        super().__init__(self)
        self._info = info

    def __str__(self):
        return self._info


class Sdk(AospAbstract):
    def __init__(self, config):
        if config is None:
            raise SdkException("config invalid")
        super().__init__(config)

    def _execution(self, project):
        self._remove(project, "build.gradle")
        return self._lint(project)

    def _parse(self, data):
        buf = []
        for item in data.splitlines():
            b = item.strip().split(LINT_SEP)
            if len(b) < LINT_LEN_MIN:
                continue
            file = b[0].strip()
            if b[1].strip() in LINT_TYPE:
                line = 0
                _type = b[1].strip()
                details = LINT_SEP.join(b[2:]).strip()
            elif type(int(b[1].strip())) == int:
                line = int(b[1].strip())
                _type = b[2].strip() if b[2].strip() in LINT_TYPE else ""
                details = LINT_SEP.join(b[3:]).strip()
            else:
                continue
            buf.append(
                {
                    Format.FILE: file,
                    Format.LINE: line,
                    Format.TYPE: _type,
                    Format.DETAILS: details,
                }
            )
        return buf

    def _popen(self, cmd, stdin=None):
        return subprocess.Popen(
            cmd, stdin=stdin, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )

    def _lint(self, project):
        tool = "lint.bat" if "win" in sys.platform else "lint"
        check = CHECK_SEP.join(self._config)
        cmd = [
            tool,
            "--check",
            check,
            "--disable",
            "LintError",
            "--nolines",
            "--quiet",
            project,
        ]
        with self._popen(cmd) as proc:
            out, err = proc.communicate()
            if proc.returncode != 0:
                raise SdkException(err.strip().decode("utf-8"))
        return self._parse(out.strip().decode("utf-8"))

    def _remove(self, project, file):
        cmd = ["find", project, "-type", "f", "-name", file, "-exec", "rm -f {} \\;"]
        with self._popen(cmd) as proc:
            _, _ = proc.communicate()
            if proc.returncode != 0:
                pass
