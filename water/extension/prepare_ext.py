#!/usr/bin/env python
# encoding: utf-8

from water.extension.base_extension import (BaseExtension,
                                            PrepareExt,
                                            FinishExt,
                                            ParamHandleExt,)
from water.route.base_route import ALL_ROUTES, API_HANDLER_MAP
from water.utils.common_utils import unquote_or_none


class FindView(PrepareExt):
    """
    Find processor view via current frame's url path
    """

    def __call__(self):
        if self.handler.view:
            return
        # when the method is post, find via api_id first
        if self.handler.request.method == "POST":
            api_id = self.handler.request.headers.get("Api_id")
            if api_id and api_id.isdigit():
                api_id = int(api_id)
                if api_id in API_HANDLER_MAP:
                    self.handler.view = API_HANDLER_MAP[api_id]
                    return

        path = self.handler.request.path
        for _regex, _view in ALL_ROUTES:
            match = _regex.match(path)
            if match:
                self.handler.view = _view
                if _regex.groups:
                    # Pass matched groups to the view processor.  Since
                    # match.groups() includes both named and
                    # unnamed groups, we want to use either groups
                    # or groupdict but not both.
                    if _regex.groupindex:
                        self.handler.path_kwargs = dict(
                            (str(k), unquote_or_none(v))
                            for (k, v) in match.groupdict().items())
                    else:
                        self.handler.path_args = [unquote_or_none(s)
                                                  for s in match.groups()]
                break


nodes = {
    'prepare': PrepareExt,
    'finish': FinishExt,
    'param': ParamHandleExt,
}


class EvalHandlerViewExt(BaseExtension):
    """
    Find out current request handler's custom extensions and eval
    """

    def __call__(self, node=None):
        _be_called_exts = []
        if not self.handler.view:
            return
        exts = self.handler.view.extensions
        if exts and node:
            base = nodes.get(node)
            if not base:
                return
            if isinstance(exts, (tuple, list)):
                for ext in exts:
                    if issubclass(ext, base):
                        _be_called_exts.append(ext)
            else:
                if issubclass(exts, base):
                    _be_called_exts.append(exts)
            for ext in _be_called_exts:
                ext(self.handler)()
        return len(_be_called_exts)
