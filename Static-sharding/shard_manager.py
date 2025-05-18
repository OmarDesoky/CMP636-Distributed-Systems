from concurrent import futures
import grpc
import api_pb2
import api_pb2_grpc

NUM_GROUPS = 2
GROUP_PORTS = [40051, 50051]

class ShardManagerServicer(api_pb2_grpc.ShardManagerServicer):
    def GetShardIndex(self, request, context):
        key = request.key
        shard_index = hash(key) % NUM_GROUPS
        port = GROUP_PORTS[shard_index]
        return api_pb2.ShardResponse(port=port)

def serve():
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        api_pb2_grpc.add_ShardManagerServicer_to_server(ShardManagerServicer(), server)
        server.add_insecure_port('[::]:30051')
        server.start()
        print("Shard Manager running on port 30051...")
        server.wait_for_termination()
    except Exception as e:
        print(f"Server error: {e}")
