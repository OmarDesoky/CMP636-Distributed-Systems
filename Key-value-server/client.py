import grpc, threading, api_pb2_grpc, api_pb2, argparse

def run(operation, key, value):
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = api_pb2_grpc.KeyValueStub(channel)
            thread_id = threading.current_thread().name
            if operation == "Put":
                req = api_pb2.PutRequest(key= key, value= value)
                response = stub.Put(req)
                print(f"{thread_id} sent put request with key: {key} and value: {value} and received {response.status}")
            elif operation == "Append":
                req = api_pb2.AppendRequest(key= key, args= value)
                response = stub.Append(req)
                print(f"{thread_id} sent append request with key: {key} and args: {value} and received old_value: {response.old_value} and status: {response.status}")
            else:
                req = api_pb2.GetRequest(key=key)
                response = stub.Get(req)
                print(f"{thread_id} sent get request with key: {key} and received value: {response.value} and status: {response.status}")
    except grpc.RpcError as e:
        print(f"RPC error: {e.code()} - {e.details()}")     
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=["Put", "Append", "Get"])
    parser.add_argument("key")
    parser.add_argument("value", nargs="?", default="")

    args = parser.parse_args()
    run(args.operation, args.key, args.value)