import grpc, threading, vote_pb2_grpc, vote_pb2
from concurrent import futures
    
class Voter(vote_pb2_grpc.VoterServicer):
    def __init__(self):
        self.true_votes = 0
        self.false_votes = 0
        self.total_votes = 12
        self.voting_closed = False
        self.lock = threading.Lock()
        
    def SendVote(self, request, context):
        try: 
            with self.lock:
                if self.voting_closed:
                    return vote_pb2.VoteResponse(id=request.id, status="voting closed")
                if request.vote_value:
                    self.true_votes += 1
                else:
                    self.false_votes += 1
                
                if self.true_votes > self.total_votes / 2:
                    self.voting_closed = True
                    print("voting closed. majority reached: true with value " + str(self.true_votes))
                elif self.false_votes > self.total_votes / 2:
                    self.voting_closed = True
                    print("voting closed. majority reached: false with value " + str(self.false_votes))
                elif self.false_votes == self.true_votes and self.false_votes == self.total_votes / 2:
                    print("voting is draw")
                    
            return vote_pb2.VoteResponse(id=request.id, status="voting succeeded")
        except Exception as e:
            print(f"Error processing vote from {request.id}: {e}")
            return vote_pb2.VoteResponse(id=request.id, status="error occurred")
        
def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    vote_pb2_grpc.add_VoterServicer_to_server(Voter(), server)
    server.add_insecure_port("[::]:" + port)
    try:
        server.start()
        print("Server started, listening on " + port)
        server.wait_for_termination()
    except Exception as e:
        print("Server error: " + e)

    
    
    
if __name__ == "__main__":
    serve()