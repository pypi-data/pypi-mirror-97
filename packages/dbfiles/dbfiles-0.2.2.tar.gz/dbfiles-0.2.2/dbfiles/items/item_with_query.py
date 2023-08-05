import os
from .item import Item


class ItemWithQuery(Item):
    @property
    def fileName(self):
        return "{}_{}_{}_{}.sql".format(
            self._textNum,
            self._intNum,
            self._type,
            self._srcPath.rsplit(".", 1)[0],
        )

    @property
    def srcPath(self):
        return self._srcPath

    @property
    def srcName(self):
        return self._srcName

    def initialize(self):
        self._srcPath, self._query = [part.strip() for part in self._value.split("=#", maxsplit=1)]
        self._srcName = os.path.basename(self._srcPath)
        self._absFilePath = os.path.abspath(os.path.join(self._schema.dir, self._srcPath))
