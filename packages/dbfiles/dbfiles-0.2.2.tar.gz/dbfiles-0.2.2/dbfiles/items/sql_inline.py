from .item import Item

class SqlInline(Item):
    def getContent(self):
        return self._value
