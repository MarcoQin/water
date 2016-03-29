#!/usr/bin/env python
# encoding: utf-8

from base_extension import PrepareExt, FinishExt
from route.base_route import ALL_ROUTES


class FindView(PrepareExt):
    """
    Find processor view via current frame's url path
    """

    def __call__(self):
        path = self.handler.request.path
        for _regex, _view in ALL_ROUTES:
            if _regex.match(path):
                self.handler.view = _view
                break


class EvalHandlerView(PrepareExt):
    """
    Find out current request handler's custom extensions and eval
    """

    def __call__(self, prepare=True):
        if not self.handler.view:
            return
        exts = self.handler.view.extensions
        if exts:
            base = PrepareExt if prepare else FinishExt
            _be_called_exts = []
            if isinstance(exts, (tuple, list)):
                for ext in exts:
                    if issubclass(ext, base):
                        _be_called_exts.append(ext)
            else:
                if issubclass(exts, base):
                    _be_called_exts.append(exts)
            for ext in _be_called_exts:
                ext(self.handler)()
