import os
from .item import Item

class SqlFile(Item):

    @property
    def fileName(self):
        return "{}_{}_{}_{}.sql".format(
            self._textNum,
            self._intNum,
            self._type,
            self._value.rsplit(".", 1)[0],
        )

    def initialize(self):
        self._absFilePath = os.path.abspath(os.path.join(
            self._schema.dir, self._value
        ))

    def getContent(self):
        with open(self._absFilePath) as fstream:
            return fstream.read()
