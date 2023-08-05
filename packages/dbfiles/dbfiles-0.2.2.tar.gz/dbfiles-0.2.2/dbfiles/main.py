import os
import argparse
import yaml

from dbfiles.schema import Schema, Loader
from dbfiles.schema import YamlFileLoader, JsonInlineLoader
from dbfiles.compiler import Compiler



def parseArgs():
    parser = argparse.ArgumentParser(prog="dbfiles")

    parser.add_argument("--src-root", dest="srcRoot", default=os.path.abspath(os.getcwd()))
    parser.add_argument("--dst-root", dest="dstRoot", default=os.path.abspath(os.getcwd()))
    parser.add_argument("--schemas", nargs="*", dest="schemas", default=[])
    parser.add_argument("--inlineSchemas", nargs="*", dest="inlineSchemas", default=[])
    parser.add_argument("--force", dest="force", action="store_true", default=False)
    parser.add_argument("--debug", dest="debug", action="store_true", default=False)

    args = parser.parse_args()

    if len(args.schemas) == 0 and len(args.inlineSchemas) == 0:
        raise Exception("Required oneOf --schemas or --inlineSchemas")

    return args


def main():
    args = parseArgs()

    Loader.setRoot(args.srcRoot)
    compiler = Compiler(args.dstRoot, args.force, args.debug)

    for schemaPath in args.schemas:
        schema = Schema(YamlFileLoader(schemaPath))
        compiler.add(schema)

    for jsonString in args.inlineSchemas:
        schema = Schema(JsonInlineLoader(jsonString))
        compiler.add(schema)

    compiler.createEntry()

if __name__ == "__main__":
    main()
