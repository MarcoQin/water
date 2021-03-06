#!/usr/bin/env python
# encoding: utf-8

import os
import importlib


def __find_view(args, dirname, files):
    module_name_slice = slice(len(args[1]) + 1, -len('.py'))
    for filename in files:
        if filename.startswith("."):
            continue
        filepath = os.path.join(dirname, filename)
        if filepath.endswith('.py'):
            args[0].add(filepath[module_name_slice].replace('/', '.').replace('\\', '.'))


def load_all_views():
    """
    loading views
    """

    #  base_dir = os.getcwd()
    base_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir))
    views = set()
    # os.path.walk(base_dir + '/view', __find_view, (views, base_dir))
    for root, dirs, files in os.walk(os.path.join(base_dir, 'view')):
        __find_view((views, base_dir), root, files)
    for item in views:
        print(item)
        importlib.import_module(item)


if __name__ == "__main__":
    load_all_views()
