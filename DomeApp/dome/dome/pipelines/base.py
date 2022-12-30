from typing import Optional


class BaseSpyPipeline:
    __doc__ = ""
    __html__ = ""
    raw_item = None

    def process_item(self, item, spider, last_pipeline: Optional['SpiderProcess']):
        pass