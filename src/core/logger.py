import logging
import time
from pathlib import Path

LOG_PATH = Path(__file__).parent.parent / "logs"


def get_logger(log_path=None):
    # log_path是存放日志的路径,如果不存在这个logs文件夹，那么需要创建出来。
    if not log_path:
        log_path = LOG_PATH
    else:
        log_path = Path(log_path)
    if not log_path.exists():
        log_path.mkdir()
    logname = str(log_path.joinpath("chat_%s.log" % time.strftime("%Y_%m_%d")))
    logger = logging.getLogger()
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
    )
    # 创建一个FileHandler
    fh = logging.FileHandler(logname, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    # 创建一个StreamHandler,用于输出到控制台
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    # 添加两个Handler
    if not logger.handlers:
        logger.addHandler(sh)
        logger.addHandler(fh)
    return logger
