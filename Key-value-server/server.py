import grpc, threading, api_pb2_grpc, api_pb2
from concurrent import futures
    
class KeyValue(api_pb2_grpc.KeyValueServicer):
    def __init__(self):
        self.map = {}
        self.lock = threading.Lock()
        
    def Get(self, request, context):
        try:
            res = None
            with self.lock:
                if request.key in self.map:
                    res = self.map[request.key]
            if res == None:
                return api_pb2.GetResponse(value=res, status="key doesn't exist")
            return api_pb2.GetResponse(value=res, status="success")
        except Exception as e:
            print(f"Error processing get request: {e}")
            return api_pb2.GetResponse(value=None, status="something went wrong")
        
    def Put(self, request, context):
        try: 
            with self.lock:
                self.map[request.key] = request.value
            return api_pb2.PutResponse(status="success")    
        except Exception as e:
            print(f"Error processing put request: {e}")
            return api_pb2.PutResponse(status="something went wrong")
        
    def Append(self, request, context):
        try:
            # breakpoint()
            old_value = None
            with self.lock:
                if request.key in self.map:
                    old_value = self.map.get(request.key)
                    self.map[request.key] += request.args
                else:
                    self.map[request.key] = request.args
            return api_pb2.AppendResponse(old_value= old_value, status="success")    
        except Exception as e:
            print(f"Error processing Append request: {e}")
            return api_pb2.AppendResponse(old_value= None, status="something went wrong")        
        
def serve():
    port = "50051"
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    api_pb2_grpc.add_KeyValueServicer_to_server(KeyValue(), server)
    server.add_insecure_port("[::]:" + port)
    try:
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
    except Exception as e:
        print(f"Server error: {e}")
        
        
def stop():
    global server
    server.stop(0)
    
if __name__ == "__main__":
    serve()