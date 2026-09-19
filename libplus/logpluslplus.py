import logging
import os

class Log:
    _added = {}   # 类级别：记录每个 logger 已添加的 Handler 标识

    def __init__(self, name, level="INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        self.logger.propagate = False   # 避免向 root 传播导致重复
        if not self.logger.hasHandlers():
            self.set_console()

    def _handler_exists(self, key):
        return key in Log._added.get(self.logger.name, set())

    def _mark_handler(self, key):
        Log._added.setdefault(self.logger.name, set()).add(key)

    def set_console(self):
        if self._handler_exists("console"):
            return
        fh = logging.StreamHandler()
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(fh)
        self._mark_handler("console")

    def set_file(self, file_name):
        key = f"file:{os.path.abspath(file_name)}"
        if self._handler_exists(key):
            return
        fh = logging.FileHandler(file_name, encoding='utf-8')
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        self.logger.addHandler(fh)
        self._mark_handler(key)

    def message(self, level, message):
        self.logger.log(getattr(logging, level.upper()), message)


l = Log('ai-model')
l1 = Log('ai-model')

l.set_file("logplus.log")
l1.set_file("logplus.log")
l.message("info", "ai-model - 0")
l1.message("info", "ai-model - 1")