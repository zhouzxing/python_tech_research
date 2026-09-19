import logging,os

class Log:
    def __init__(self, name, level="INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        # fix duplicated name logger
        if not self.logger.hasHandlers():
            self.set_console()

    def set_console(self):
        fh = logging.StreamHandler()
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        if not self.logger.hasHandlers():
            self.logger.addHandler(fh)

    def set_file(self, file_name):
        # 检查是否已有 FileHandler 指向同一个文件
        for h in self.logger.handlers:
            if isinstance(h, logging.FileHandler) and h.baseFilename == os.path.abspath(file_name):
                return  # 已存在，直接返回，不重复添加

        fh = logging.FileHandler(file_name, encoding='utf-8')
        fh.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        print(f'{self.logger.hasHandlers()=}')
        self.logger.addHandler(fh)

    def message(self, level, message):
        self.logger.log(getattr(logging, level.upper()), message)

# single instance
l = Log('ai-model')
l1 = Log('ai-model')

l.set_file("logplus.log")
l1.set_file("logplus.log")
l.message("info", "ai-model - 0")
l1.message("info", "ai-model - 1")