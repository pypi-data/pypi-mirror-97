from .item_with_query import ItemWithQuery

class CsvFile(ItemWithQuery):

    def getContent(self):
        with open(self._absFilePath) as fstream:
            data = fstream.read()

        return (
            self._query.strip(" ;") + ";\n" +
            data.strip() + "\n" +
            "\\.\n"
        )
