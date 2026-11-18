import sys
import os
import yaml
import argparse
import subprocess
from logging_config import logger

# ping 的参数与输出编码在 Windows / Linux 上不同，这里统一处理
if os.name == "nt":
    PING_COUNT_FLAG = "-n"      # Windows: -n 表示发送次数
    PING_ENCODING = "gbk"       # Windows 控制台 ping 输出是 GBK
else:
    PING_COUNT_FLAG = "-c"      # Linux/macOS: -c 表示发送次数
    PING_ENCODING = "utf-8"

def loadyaml():
    parser = argparse.ArgumentParser(description="ping ip tools")
    parser.add_argument("--yaml",default="yaml_config/ips.yaml" , help="input yaml")
    return parser.parse_args()

def openyaml(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error("file not found")
        sys.exit(1)
    except Exception:
        logger.error("Unknow error")
        sys.exit(1)

def subprocessIP(ip, packet, timeout_num):
    result = subprocess.run(
        ["ping", PING_COUNT_FLAG, packet, ip],
        check=True,
        capture_output=True,
        text=True,
        encoding=PING_ENCODING,
        errors="replace",
        timeout=timeout_num,
    )
    return result

def main():

    ips = openyaml(loadyaml().yaml)["ips"]
    logger.info("启动自检 自检ip:'127.0.0.1'")

    try:
        subprocessIP("127.0.0.1", "1", 4)
        logger.info(f"目标IP:'127.0.0.1'状态: 自检成功")
    except Exception as e:
        logger.error(f"目标IP:'127.0.0.1'状态: 自检失败")
        sys.exit(1)

    logger.info(f"一共获取到{len(ips)}台服务器 工具自检成功 启动循环\n")

    for ip in ips:
        try:
            result = subprocessIP(ip, "2", 3)
            logger.info(f"目标IP: {ip} 状态: Success!{result.stdout}")
        except subprocess.TimeoutExpired:
            logger.error(f"目标IP: {ip} 状态: 超时 (Timeout) Error!")
        except subprocess.CalledProcessError:
            logger.error(f"目标IP: {ip} 状态: 不通 (Unreachable) Error!")
        except Exception as e:
            logger.error(f"目标IP: {ip} 状态: 未知错误 -> {e}")

if __name__ == "__main__":
    main()