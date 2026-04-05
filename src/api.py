import logging
import re

import requests

from config import API_HASH, API_KEY, API_URL

logger = logging.getLogger(__name__)

# 匹配流量数据
TRAFFIC_PATTERN = re.compile(r"<.*?>(?P<total>\d*?),(?P<used>\d*?),(?P<free>\d*?),(?P<per>\d*?)</.*?>")


def get_server_usage() -> dict:
    """
    获取服务器用量数据
    返回: {"upload": "0B", "download": str, "total": str, "expire_time": str}
    """
    logger.info("Fetching server usage data")
    post_data = {
        "key": API_KEY,
        "hash": API_HASH,
        "action": "info",
        "bw": "true",
    }

    response = requests.post(API_URL, data=post_data)
    response.raise_for_status()
    text = response.text
    logger.debug(f"API response: {text}")

    # 提取流量数据
    for match in re.finditer(r"(<(?P<type>\w*?)>.*?</\w*?>)", text):
        if match.group(2) == "bw":
            data = TRAFFIC_PATTERN.match(match.group()).groupdict()
            logger.info(f"Parsed traffic data: {data}")

            # 字节转 GB
            total_gb = float(data["total"]) / 1024**3
            used_gb = float(data["used"]) / 1024**3
            result = {
                "upload": "0B",
                "download": f"{used_gb:.2f}GB",
                "total": f"{total_gb:.2f}GB",
                "expire_time": "2027-04-01",  # 假设固定，或从API获取
            }
            logger.info(f"Calculated usage: {result}")
            return result

    logger.error("Failed to parse traffic data")
    raise ValueError("Failed to parse traffic data")
