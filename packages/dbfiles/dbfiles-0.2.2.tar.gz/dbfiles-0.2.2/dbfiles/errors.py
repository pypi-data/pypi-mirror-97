

class DbfilesException(Exception):
    pass


class CounterException(DbfilesException):
    pass


class SchemaException(DbfilesException):
    pass


class CompilerException(DbfilesException):
    pass
