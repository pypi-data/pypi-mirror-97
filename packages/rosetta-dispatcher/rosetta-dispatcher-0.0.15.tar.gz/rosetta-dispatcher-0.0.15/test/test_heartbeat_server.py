import time

from heartbeat.heartbeat_observer import HeartbeatObserver
from heartbeat.heatbeat_reporter import HeartbeatReporter

host = '61.160.36.168'
port = 4032


def callback(result):
    print("test", result)


hbo = HeartbeatObserver(namespaces=["test_heartbeat"],
                        redis_host=host,
                        redis_port=port,
                        interval=10,
                        callback=callback)
hbo.start()

while True:
    time.sleep(1)
