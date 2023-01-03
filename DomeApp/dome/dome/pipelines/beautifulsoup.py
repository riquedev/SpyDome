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

    def process_item(self, item: Request, spider, last_pipeline: Optional['SpiderProcess']):
        bs = BeautifulSoup(item.body)

        for class_request in self.params:
            request_method = class_request['method']
            args = class_request.get('args', [])
            kwargs = class_request.get('kwargs', {})
            assert hasattr(bs, request_method)
            method = getattr(bs, request_method)
            if callable(method):
                if len(args):
                    bs = method(*args, **kwargs)
                else:
                    bs = method(**kwargs)
            else:
                bs = method

        return bs
