class ExamplePipeLine(object):
    def process_item(self, item, spider):
        data = MyData()
        data.field1 = item['field1']
        data.field2 = item['field2']
        data.save()
        return item