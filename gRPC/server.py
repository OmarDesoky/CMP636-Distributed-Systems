import grpc, threading, vote_pb2_grpc, vote_pb2, os
from concurrent import futures
    
class Voter(vote_pb2_grpc.VoterServicer):
    def __init__(self):
        self.true_votes = 0
        self.false_votes = 0
        self.total_votes = 12
        self.lock = threading.Lock()
        
    def SendVote(self, request, context):
        try: 
            with self.lock:
                if request.vote_value:
                    self.true_votes += 1
                else:
                    self.false_votes += 1
                
                if (self.true_votes > self.total_votes / 2) or (self.false_votes > self.total_votes / 2):
                    print(f"voting closed. majority reached: true={self.true_votes} and flase={self.false_votes}")
                    server.stop(0)
                elif self.false_votes == self.true_votes and self.false_votes == self.total_votes / 2:
                    print("voting is draw")
                    server.stop(0)
                    
            return vote_pb2.VoteResponse(id=request.id, status="voting succeeded")
        except Exception as e:
            print(f"Error processing vote from {request.id}: {e}")
            return vote_pb2.VoteResponse(id=request.id, status="error occurred")
        
def serve():
    port = "50051"
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    vote_pb2_grpc.add_VoterServicer_to_server(Voter(), server)
    server.add_insecure_port("[::]:" + port)
    try:
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
    except Exception as e:
        print(f"Server error: {e}")

    
    
    
if __name__ == "__main__":
    serve()