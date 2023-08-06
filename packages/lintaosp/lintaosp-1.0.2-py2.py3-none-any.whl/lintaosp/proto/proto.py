# -*- coding: utf-8 -*-


"""Prototype
{
  "file": "name",
  "line": 1,
  "type": "Error",
  "details": "text"
}
"""


class Format:
    DETAILS = "details"
    FILE = "file"
    LINE = "line"
    TYPE = "type"


class Type:
    ERROR = "Error"
    INFO = "Info"
    WARN = "Warning"
