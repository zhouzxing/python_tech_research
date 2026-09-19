# log.py
import logging

class Log:
    # name, level no need to record
    def __init__(self, name):
        self.__log_name = name
        self.__log_levlel = None
        # deal duplicate handler
        self.__handlers = []
        # init default logger
        self.set_console()

    def set_console(self):
        self.logger = logging.getLogger(self.__log_name)
        # self.logger.setLevel(eval("logging." + level.upper()))
        fh = logging.StreamHandler()
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                       ,datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(log_format)
        if fh not in self.__handlers:
            self.logger.addHandler(fh)
            self.__handlers.append(fh)

    def set_file(self, file_name):
        self.logger = logging.getLogger(self.__log_name)
        # self.logger.setLevel(eval("logging." + level.upper()))
        fh = logging.FileHandler(file_name,encoding='utf-8') # FileHandler 的默认模式是 'a'，用 'a+' 在某些平台上可能导致文件指针行为异常。
        log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                                       ,datefmt='%Y-%m-%d %H:%M:%S')
        fh.setFormatter(log_format)
        if fh not in self.__handlers:
            self.logger.addHandler(fh)
            self.__handlers.append(fh)

    def message(self,level,message):
        # self.logger.log(eval("logging." + level.upper()),message) # not safe for eval
        self.logger.log(getattr(logging,level.upper()),message)



l = Log('ai-model')
l.message("warning","test Log class to console")

# l.set_file('libplus.log')
# l.message("info","test info Log to file")
