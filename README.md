# sub

生成订阅地址并加上 RackNerd 剩余流量显示

## 自动生成

[智能自适应 VLESS + WS + Cloudflare Tunnel 代理](https://hub.docker.com/r/7techlife/seven)

## 手动生成
PS. 除非有流媒体解锁或其他需求，否直不建议在 outbounds 套 Warp。入口已经是 Cloudflare CDN 的情况下服务器只做流量中转，再转 Warp 会变成 Cloudflare → VPS → 再回 Cloudflare 的回连套娃。

1. 在 cloudflare tunnel 新增 `vless.<your_domain>`，指向 http://localhost:9797
2. `sing-box run -c vless.conf`

```json
{
    "log":{
        "disabled":false,
        "level":"info",
        "timestamp":true
    },
    "inbounds":[
        {
            "type":"vless",
            "tag":"proxy",
            "listen":"::",
            "listen_port":9797,
            "users":[
                {
                    "uuid":"c8f5160b-035d-407c-b386-0a3e0f8a8166",
                    "flow":""
                }
            ],
            "transport":{
                "type":"ws",
                "path":"/c8f5160b-035d-407c-b386-0a3e0f8a8166",
                "max_early_data":2048,
                "early_data_header_name":"Sec-WebSocket-Protocol"
            }
        }
    ],
    "outbounds":[
        {
            "type":"direct",
            "tag":"direct"
        }
    ]
}
```

## 配置文件

```sh
# 设置 RackNerd API
# https://nerdvm.racknerd.com/

# VLESS_LINKS
vless://c8f5160b-035d-407c-b386-0a3e0f8a8166@usa.visa.com:2053?encryption=none&security=tls&sni=vless.<your_domain>&host=vless.<your_domain>&fp=chrome&type=ws&path=%2Fc8f5160b-035d-407c-b386-0a3e0f8a8166%3Fed%3D2048#cf_tunnel_visa_us_2053

# VALID_TOKENS
# 填写 UUID 防止被滥用
```


## 启动

```bash
# Local development
python3.10 -m pip install -r requirements.txt
python3.10 src/app.py

# Docker
docker build -t sub:local .
docker-compose up -d
```

## Ref
[Clash 订阅响应头](https://www.clashverge.dev/guide/url_schemes.html#_3)