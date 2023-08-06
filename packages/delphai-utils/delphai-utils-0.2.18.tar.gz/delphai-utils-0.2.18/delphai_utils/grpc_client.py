from grpc.experimental.aio import insecure_channel as async_insecure_channel
from grpc import insecure_channel


def get_grpc_client(Stub, address: str, is_async: bool = True):
  if is_async:
    channel = async_insecure_channel(address)
  else:
    channel = insecure_channel(address)
  client = Stub(channel)
  return client