from dbfiles.errors import CounterException


class Counter(object):
    """
        Max size is 456976 == zzzz
    """
    def __init__(self):
        self._intNum = 0
        self._textValue = [97, 97, 97, 96]

    @property
    def intNum(self):
        return self._intNum

    @property
    def textNum(self):
        return "".join(chr(i) for i in self._textValue)

    def next(self):
        self._intNum += 1

        for i in reversed(range(4)):
            if self._textValue[i] == 122:
                if i == 0:
                    raise CounterException("Max Counter size {} == zzzz".format(self._intNum - 1))

                self._textValue[i] = 97
            else:
                self._textValue[i] += 1
                break

        return self.intNum, self.textNum
