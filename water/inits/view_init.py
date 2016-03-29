#!/usr/bin/env python
# encoding: utf-8

import os
import importlib


def __find_view(args, dirname, files):
    for filename in files:
        filepath = os.path.join(dirname, filename)
        if filepath.endswith('.py'):
            args[0].add(filepath[len(args[1]) + 1: -len('.py')].replace('/', '.').replace('\\', '.'))


def load_all_views():
    """
    loading views
    """

    base_dir = os.getcwd()
    views = set()
    os.path.walk(base_dir + '/view', __find_view, (views, base_dir))
    for item in views:
        importlib.import_module(item)


if __name__ == "__main__":
    load_all_views()
