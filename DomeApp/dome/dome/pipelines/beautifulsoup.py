from typing import Optional

from bs4 import BeautifulSoup
from scrapy import Request

from .base import BaseSpyPipeline


class BeautifulSoupPipeline(BaseSpyPipeline):
    __doc__ = ""
    __html__ = ""
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "method": {"type": "string"},
                "args": {"type": "array"},
                "kwargs": {"type": "object"}
            }
        }
    }

    def _is_iter(self, obj) -> bool:
        has_method = hasattr(obj, '__iter__')
        not_is_bs = not isinstance(obj, BeautifulSoup)
        return all([has_method, not_is_bs])

    def _request_method(self, instance, request_method: str, *args, **kwargs):
        allowed_methods = self.get_pipeline_methods(instance)
        assert request_method in allowed_methods, f"Method {request_method} not found in BeautifulSoup instance. Allowed Methods: {allowed_methods}"
        method = getattr(instance, request_method, None)
        assert method is not None, f"Method {request_method} not found in BeautifulSoup instance"

        if callable(method):
            if len(args):
                bs = method(*args, **kwargs)
            else:
                bs = method(**kwargs)
        else:
            bs = method

        return bs

    def get_pipeline_methods(self, instance):
        return dir(instance)

    def process_item(self, item: Request, spider, last_pipeline: Optional['SpiderProcess']):
        bs = BeautifulSoup(item.body, 'lxml')

        for class_request in self.params:
            request_method = class_request['method']
            args = class_request.get('args', [])
            kwargs = class_request.get('kwargs', {})

            if self._is_iter(bs):
                _new_bs = []
                for iter_bs in bs:
                    _new_bs = self._request_method(iter_bs, request_method, *args, **kwargs)
                bs = _new_bs
            else:
                bs = self._request_method(bs, request_method, *args, **kwargs)

        return bs
