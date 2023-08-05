from .item import Item
from .csv_file import CsvFile
from .json_file import JsonFile
from .sql_file import SqlFile
from .sql_inline import SqlInline
from .yaml_file import YamlFile


Item.itemsMap = {
    "=#": SqlInline,
    "sql": SqlFile,
    "json": JsonFile,
    "yaml": YamlFile,
    "csv": CsvFile,
}
