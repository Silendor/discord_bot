import logging

class Bot_Logging():
    '''Set up log settings'''

    def __init__(self, logger_target, log_level):
        '''Initialize static parameters'''
        self.logger_target = logger_target
        self.filename = '{}.log'.format(self.logger_target)
        self.encoding = 'utf-8'
        self.mode = 'w'
        self.log_format = '%(asctime)s:%(levelname)s:%(name)s: %(message)s'
        self.log_level = self.define_log_level(log_level)
        logging.basicConfig(filename=self.filename, level=logging.ERROR)
        # self.log_to_file()

    def log_to_file(self):
        self.logger = logging.getLogger(self.logger_target)
        self.logger.setLevel(self.log_level)
        self.handler = logging.FileHandler(filename=self.filename, 
                            encoding=self.encoding, mode=self.mode)
        self.handler.setFormatter(logging.Formatter(self.log_format))
        self.logger.addHandler(self.handler)

    def log_to_console(self):
        logging.basicConfig(level=self.log_level)

    def define_log_level(self, log_level):
        if log_level == 'CRITICAL':
            return logging.CRITICAL
        elif log_level == 'ERROR':
            return logging.ERROR
        elif log_level == 'WARNING':
            return logging.WARNING
        elif log_level == 'INFO':
            return logging.INFO
        elif log_level == 'DEBUG':
            return logging.DEBUG