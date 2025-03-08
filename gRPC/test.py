from threading import Thread
import server
import client as client

if __name__ == "__main__":
    # Create Server
    server_thread = Thread(target=server.serve, name="server")
    server_thread.start()
    # Create 12 Clients
    threads = []
    for n in range(12):
        t = Thread(target=client.run, name="Client" + str(n))
        t.start()
        threads.append(t)
    # Wait for all Clients to finish
    for t in threads:
        t.join()
