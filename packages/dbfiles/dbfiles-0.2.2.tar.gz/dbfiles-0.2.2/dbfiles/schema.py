import os
import json
import yaml

from jsonschema import Draft7Validator

from .counter import Counter
from .items import Item
from .errors import SchemaException


curDir = os.path.abspath(os.path.dirname(__file__))

def loadSchema(filePath):
    with open(filePath) as fstream:
        schema = yaml.load(fstream, Loader=yaml.FullLoader)

    Draft7Validator.check_schema(schema)
    return schema

class Loader(object):

    _root = os.getcwd()

    @property
    def absPath(self):
        return self._absPath

    @property
    def relPath(self):
        return self._relPath


    @property
    def fileName(self):
        return self._fileName

    @property
    def dir(self):
        return self._dir

    def __init__(self, filePath):
        self._absPath = os.path.abspath(os.path.join(Loader._root, filePath))
        self._relPath = os.path.relpath(self._absPath, Loader._root)
        self._fileName = os.path.basename(self._absPath)
        self._dir = os.path.dirname(self._absPath)

    @classmethod
    def setRoot(cls, root):
        cls._root = root


class YamlFileLoader(Loader):

    @property
    def data(self):
        return self._data

    def __init__(self, filePath):
        super().__init__(filePath)

        with open(self._absPath) as fstream:
            self._data = yaml.load(fstream, Loader=yaml.FullLoader)


class JsonInlineLoader(Loader):

    _validator = Draft7Validator(loadSchema(os.path.join(curDir, "json_inline.yaml")))

    @property
    def data(self):
        return self._data

    def __init__(self, jsonString):
        inlineSchema = json.loads(jsonString)

        if not JsonInlineLoader._validator.is_valid(inlineSchema):
            error = "Invalid inline schema: jsonString[:128]={}".format(jsonString[:128])
            for err in JsonInlineLoader._validator.iter_errors(inlineSchema):
                print("Error: {}".format(err.message))
                print("Context: {}".format(err.absolute_schema_path))

            raise SchemaException(error)

        self._data = inlineSchema["data"]

        super().__init__(inlineSchema["filePath"])


class Schema(object):

    _validator = Draft7Validator(loadSchema(os.path.join(curDir, "schema.yaml")))

    @property
    def counter(self):
        return self._counter

    @property
    def absPath(self):
        return self._loader._absPath

    @property
    def relPath(self):
        return self._loader.relPath

    @property
    def fileName(self):
        return self._loader._fileName

    @property
    def dir(self):
        return self._loader._dir

    @property
    def data(self):
        return self._loader.data

    @property
    def items(self):
        return self._items

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def __init__(self, loader, parents=[]):
        self._loader = loader

        if self.relPath in parents:
            raise SchemaException("Circular include schema {}, parents={}".format(
                self.relPath,
                parents
            ))

        if not Schema._validator.is_valid(self.data):
            error = "Invalid schema {}".format(self._absPath)
            for err in Schema._validator.iter_errors(self.data):
                print("Error: {}".format(err.message))
                print("Context: {}".format(err.absolute_schema_path))

            raise SchemaException(error)

        self._counter = Counter()

        self._items = []
        for itemDict in self.data["main"]:
            if "include" in itemDict:
                subSchemaAbsPath = os.path.abspath(os.path.join(self.dir, itemDict["include"]))
                subSchemaRelPath = os.path.relpath(subSchemaAbsPath, Loader._root)
                self._items.append(Schema(YamlFileLoader(subSchemaRelPath), parents + [self.relPath]))
            else:
                self._items.append(Item.create(self, itemDict))
