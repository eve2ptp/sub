import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def parse_traffic(traffic_str: str) -> int:
    """
    将 '2GB', '2TB', '2MB' 转换为字节数 (Bytes)
    """
    traffic_str = traffic_str.upper().strip()
    units = {"TB": 1024**4, "GB": 1024**3, "MB": 1024**2, "KB": 1024**1, "B": 1}

    for unit, multiplier in units.items():
        if traffic_str.endswith(unit):
            try:
                number = float(traffic_str.replace(unit, "").strip())
                return int(number * multiplier)
            except ValueError:
                break
    return 0


def parse_datetime(time_str: str) -> int:
    """
    将 '2026-03-21 17:50:11' 转换为 Unix 时间戳
    """
    try:
        dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp())
    except ValueError:
        return 0


def generate_sub_info(upload="0B", download="0B", total="10GB", expire="2099-01-01 00:00:00"):
    """
    生成符合订阅标准的 Header 字符串
    """
    u = parse_traffic(upload)
    d = parse_traffic(download)
    t = parse_traffic(total)
    e = parse_datetime(expire)
    logger.info("=" * 50)
    logger.info(f"📅 服务器到期时间：{expire}")
    logger.info(f"📶 总流量：{total}")
    logger.info(f"📥 已用流量：{download}")
    logger.info(f"📊 剩余流量：{float(total[:-2]) - float(download[:-2]):.2f}GB")
    logger.info("=" * 50)
    return f"upload={u}; download={d}; total={t}; expire={e}"
