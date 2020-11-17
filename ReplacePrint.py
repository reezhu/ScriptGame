# -*- coding: utf-8 -*-
# @Author  : Ree
import sys

SystemEncoding = sys.stdout.encoding


class CompatibleLogger:
    def __init__(self):
        self.old = sys.stdout

    def write(self, data):
        if isinstance(data, str):
            data = data.decode("utf-8")
        self.old.write(data.encode(SystemEncoding))

    def flush(self):
        self.old.flush()

    def reset(self):
        sys.stdout = self.old


sys.stdout = CompatibleLogger()
