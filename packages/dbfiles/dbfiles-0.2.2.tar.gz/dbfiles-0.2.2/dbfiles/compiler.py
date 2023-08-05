import os
import uuid
import shutil
import subprocess

from .errors import CompilerException

curDir = os.path.abspath(os.path.dirname(__file__))


class Compiler(object):

    def __init__(
        self,
        dstRoot,
        force,
        debug
    ):
        self._dstRoot = dstRoot
        self._force = force
        self._debug = debug
        self._entry = []

        if self._force:
            shutil.rmtree(self._dstRoot, ignore_errors=True)

        if os.path.exists(self._dstRoot):
            print("HINT: use --force option for delete --dst-root {} before compiling".format(self._dstRoot))
            raise CompilerException("--dst-root {} already exists".format(self._dstRoot))

        os.makedirs(self._dstRoot)

    def add(self, schema):
        for item in schema.items:
            if item.type == "schema":
                self._entry.append("--from {} include {}".format(
                    schema.relPath,
                    item.relPath
                ))
                self.add(item)
            else:
                relFilePath = os.path.join(schema.relPath, item.fileName)
                absFilePath = os.path.join(self._dstRoot, relFilePath)

                absFileDir = os.path.dirname(absFilePath)
                if not os.path.exists(absFileDir):
                    os.makedirs(absFileDir)

                with open(absFilePath, "w") as fstream:
                    fstream.write(item.getContent())

                self._entry.append("\\i '{}'".format(relFilePath))

    def createEntry(self):
        with open(os.path.join(self._dstRoot, "entry.sql"), "w") as fstream:
            fstream.write(
                "\n".join(self._entry) + "\n"
            )
