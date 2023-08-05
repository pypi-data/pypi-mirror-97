import json
from .item_with_query import ItemWithQuery

class JsonFile(ItemWithQuery):
    def getContent(self):
        with open(self._absFilePath) as fstream:
            data = json.load(fstream)
        return self._query.format(file=self._srcPath, value=json.dumps(data))
