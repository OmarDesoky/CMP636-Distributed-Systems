import grpc, threading, api_pb2_grpc, api_pb2, argparse
from concurrent import futures
from pysyncobj import SyncObj
from pysyncobj.batteries import ReplDict


class RaftKeyValue(api_pb2_grpc.RaftKeyValueServicer):
    def __init__(self, repl_dict):
        self.repl_dict = repl_dict
    def Get(self, request, context):
        try:
            res = None
            if request.key in self.repl_dict:
                res = self.repl_dict[request.key]
            if res == None:
                print(f"recieved get request with key: {request.key} and key doesn't exist")
                return api_pb2.GetResponse(value=res, status="key doesn't exist")
            print(f"recieved get request with key: {request.key} and output: {res}")
            return api_pb2.GetResponse(value=res, status="success")
        except Exception as e:
            print(f"Error processing get request: {e}")
            return api_pb2.GetResponse(value=None, status="something went wrong")
        
    def Put(self, request, context):
        try:
            self.repl_dict.set(request.key, request.value, sync=True)
            print(f"recieved put request with key: {request.key} and value: {request.value} and output: success")
            return api_pb2.PutResponse(status="success")    
        except Exception as e:
            print(f"Error processing put request: {e}")
            return api_pb2.PutResponse(status="something went wrong")
        
    def Append(self, request, context):
        try:
            old_value = None
            if request.key in self.repl_dict:
                old_value = self.repl_dict.get(request.key)
                self.repl_dict.set(request.key, old_value + request.args, sync=True)
            else:
                self.repl_dict.set(request.key, request.args, sync=True)
            print(f"recieved append request with key: {request.key} and args: {request.args} and output: {old_value}")
            return api_pb2.AppendResponse(old_value= old_value, status="success")    
        except Exception as e:
            print(f"Error processing Append request: {e}")
            return api_pb2.AppendResponse(old_value= None, status="something went wrong")        
        
def serve(server_num):
    partner_addresses = []
    for n in range(3):
        if n != server_num:
            partner_addresses.append(f"localhost:{4321+n}")
    repl_dict = ReplDict()
    SyncObj(f"localhost:{4321+int(server_num)}", partner_addresses, consumers=[repl_dict])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    api_pb2_grpc.add_RaftKeyValueServicer_to_server(RaftKeyValue(repl_dict), server)
    server.add_insecure_port(f"[::]:{50051+int(server_num)}")
    try:
        server.start()
        print(f"Server started, listening on {50051+int(server_num)}")
        server.wait_for_termination()
    except Exception as e:
        print(f"Server error: {e}")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("server_num")
    args = parser.parse_args()
    serve(args.server_num)