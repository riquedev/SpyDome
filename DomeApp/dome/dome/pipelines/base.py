from typing import Optional
from jsonschema import validate as _schema_validate

class BaseSpyPipeline(object):
    __doc__ = ""
    __html__ = ""
    raw_item = None
    params = None
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "method": {"type": "string"},
                "kwargs": {"type": "object"}
            }
        }
    }

    def __init__(self, params, **kwargs):
        self.params = params
        self.validate()

    def schema_validate(self):
        _schema_validate(self.params, self.schema)
        return self

    def validate(self):
        self.schema_validate()

    def process_item(self, item, spider, last_pipeline: Optional['SpiderProcess']):
        pass
