import json
from datetime import datetime

from rosetta_dispatcher.dispatch_client import DispatchClient

host = '61.160.36.168'
port = 4032

dc = DispatchClient(redis_host=host, redis_port=port)

count = 0
data = {
    "source_language": "zh",
    "target_language": "en",
    "terminology_list": [
    ],
    "chapter_content": [
        "我的世界"
    ]
}
while True:
    start = datetime.utcnow()
    result = dc.process(service_queue='NMT_RPC_QUEUE_DEV', data=json.dumps(data), timeout=10)
    end = datetime.utcnow()
    print(end-start)
    print(result)
    count+=1