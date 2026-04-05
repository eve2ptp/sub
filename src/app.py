import base64
import logging
import os

from fastapi import FastAPI, HTTPException, Query, Request, Response

from src.api import get_server_usage
from src.config import VALID_TOKENS, VLESS_LINKS
from src.utils import generate_sub_info

# 配置日志
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/sub")
def sub(request: Request, token: str = Query(None)):
    logger.info(f"Received request with token: {token}")

    # 检查是否是本地请求，本地请求不需要token
    client_host = request.client.host
    
    # 判断是否为本地/私有IP
    def is_private_ip(ip: str) -> bool:
        import ipaddress
        try:
            ip_obj = ipaddress.ip_address(ip)
            return ip_obj.is_private or ip_obj.is_loopback
        except ValueError:
            return False
    
    is_local = client_host in ("127.0.0.1", "localhost", "::1") or is_private_ip(client_host)
    logger.info(f"Request from: {client_host}, is_private: {is_private_ip(client_host)}, is_local: {is_local}")

    if not is_local and (not token or token not in VALID_TOKENS):
        logger.warning(f"Invalid token: {token}")
        raise HTTPException(status_code=403, detail="Invalid Token")

    # 获取服务器用量数据
    user_data = get_server_usage()
    logger.info(f"Server usage data: {user_data}")

    # 生成订阅信息头部
    sub_info = generate_sub_info(
        upload=user_data["upload"], download=user_data["download"], total=user_data["total"], expire=user_data["expire_time"]
    )
    logger.info(f"Generated sub info: {sub_info}")

    # 从配置读取vless链接
    content = "\n".join(VLESS_LINKS)
    logger.info("Successfully generated vless_links from config")

    headers = {"subscription-userinfo": sub_info, "Content-Type": "text/plain; charset=utf-8"}

    encoded_result = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    return Response(content=encoded_result, headers=headers, media_type="text/plain; charset=utf-8")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
