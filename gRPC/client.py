import grpc, threading, random, vote_pb2_grpc, vote_pb2

def run():
    try:
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = vote_pb2_grpc.VoterStub(channel)
            thread_id = threading.current_thread().name
            random_vote = random.choice([True, False])
            req = vote_pb2.VoteRequest(id= thread_id, vote_value = random_vote)
            response = stub.SendVote(req)
            print(thread_id + " sent " + str(random_vote) + " and received " + response.status)
    except grpc.RpcError as e:
        print(f"RPC error: {e.code()} - {e.details()}")     
        
if __name__ == "__main__":
    run()