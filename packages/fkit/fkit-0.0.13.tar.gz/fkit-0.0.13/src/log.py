import logging  # 引入logging模块
import os.path
import time
import traceback
import sys
from src import config

class Logger:
    def __init__(self):
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)  # Log等级总开关
        
        # 第二步，创建一个handler，用于写入日志文件
        cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
        log_path = cli_path + '/Logs/'
        is_exist = os.path.exists(log_path)
        if not is_exist:
            os.makedirs(log_path)
        log_name = log_path + "error" + '.log'
        logfile = log_name
        fh = logging.FileHandler(logfile, encoding="utf-8", mode='w')
        fh.setLevel(logging.ERROR)  # 输出到file的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        
        # 再创建一个handler，用于输出到控制台    
        ch = logging.StreamHandler()  
        ch.setLevel(logging.CRITICAL)
        
        # 第四步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)

    @staticmethod
    def error_logger(content):
        string = "\n    "
        for line in traceback.format_stack():
            string += line.strip()

        string += "\n    "+content
        logging.error(string)
        print("ERROR:" + content)
        sys.exit()

    @staticmethod
    def critical_logger(content):
        string = "\n    "
        for line in traceback.format_stack():
            string += line.strip()

        string += "\n   "+content
        logging.critical(string)
        sys.exit()
