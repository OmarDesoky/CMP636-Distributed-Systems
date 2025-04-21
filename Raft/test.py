from threading import Thread
import server
import client
import random, time

if __name__ == "__main__":
    # Create Servers
    server_threads = []
    for n in range(3):
        server_thread = Thread(target=server.serve, name="server", args=(n, ), daemon=True)
        server_thread.start()
        server_threads.append(server_thread)
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
        
    for t in server_threads:
        t.join()