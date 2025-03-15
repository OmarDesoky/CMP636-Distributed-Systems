from threading import Thread
import server
import client
import random, time

if __name__ == "__main__":
    # Create Server
    server_thread = Thread(target=server.serve, name="server", daemon=True)
    server_thread.start()
    # Sleep for 500ms for server to init.
    time.sleep(0.5)
    # Test Get, Put, and Append At Same Time
    threads = []
    for n in range(5):
        random_operation = random.choice(["Get", "Put", "Append"])
        t = Thread(target=client.run, name="Client" + str(n), args=(random_operation, "K1", "Client" + str(n)))
        t.start()
        threads.append(t)
    # Wait for all Clients to finish
    for t in threads:
        t.join()
    
    server.stop()