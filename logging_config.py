import logging
import os
import sys

# 日志目录不存在时自动创建，保证 clone 下来直接能跑
os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("main")

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt= "%Y-%m-%d %H:%M:%S",

    handlers=[
        logging.FileHandler("logs/logginglogs.log",encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]

)