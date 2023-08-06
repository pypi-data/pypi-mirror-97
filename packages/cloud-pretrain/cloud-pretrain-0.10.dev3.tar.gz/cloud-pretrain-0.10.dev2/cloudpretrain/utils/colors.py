# coding: utf8
from __future__ import print_function, absolute_import

from colors import color
import re


def colorize(string):
    """  "a :red{a,b,c} :green{green string}" """
    pattern = ":([a-z]+?){(.*?)}"
    split_strings = re.split(":[a-z]+?{.*?}", string)
    res = split_strings[0]
    for i, match in enumerate(re.finditer(pattern, string)):
        fg = match.group(1)
        s = match.group(2)
        res += color(s, fg=fg)
        res += split_strings[i+1]
    return res


def error(string):
    return color(string, fg="red")


def success(string):
    return color(string, fg="green")


def info(string):
    return string


def emphasize(string):
    return color(string, fg="yellow")

