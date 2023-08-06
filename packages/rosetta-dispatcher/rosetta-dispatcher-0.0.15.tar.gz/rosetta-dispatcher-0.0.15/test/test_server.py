from time import sleep

from rosetta_dispatcher.dispatch_server import DispatchServer
from rosetta_dispatcher.model.dispatch_response_model import DispatchResponseModel
from rosetta_dispatcher.model.dispatch_types import DispatchResponseStatus

host = '61.160.36.168'
port = 4032

ds = DispatchServer(redis_host=host, redis_port=port)

count = 0
while True:
    result = ds.fetch('NMT_RPC_QUEUE_DEV', batch_count=16)
    print(f'fetched: {len(result)}')
    response_list = [DispatchResponseModel(correlation_id=request.correlation_id, status=DispatchResponseStatus.OK,
                                         data=request.data) for request in result]

    ds.batch_send_response(result, response_list)


