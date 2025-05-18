from threading import Thread
import server
import shard_manager
import client
import time

if __name__ == "__main__":
    # Create Shard Manager
    shardManager_thread = Thread(target=shard_manager.serve, name="server")
    shardManager_thread.start()
    
    # Sleep for 500ms for Shard manger to init.
    time.sleep(0.5)
    
    # Create G1 Servers
    serverG1_threads = []
    for n in range(3):
        serverG1_thread = Thread(target=server.serve, name="server", args=(n, 40051, 4444, ), daemon=True)
        serverG1_thread.start()
        serverG1_threads.append(serverG1_thread)
        
    # Create G2 Servers
    serverG2_threads = []
    for n in range(3):
        serverG2_thread = Thread(target=server.serve, name="server", args=(n, 50051, 5555, ), daemon=True)
        serverG2_thread.start()
        serverG2_threads.append(serverG2_thread)  
        
    # Sleep for 500ms for server to init.
    time.sleep(0.5)
    # Test Get, Put, and Append At Same Time
    threads = []    
    
    # Test Get, Put, and Append At Same Time
    client_thread1 = Thread(target=client.run, name="client", args=("Append", "K1", "V1"))
    client_thread2 = Thread(target=client.run, name="client", args=("Append", "K1", "V2"))
    client_thread3 = Thread(target=client.run, name="client", args=("Append", "K1", "V3"))
    client_thread4 = Thread(target=client.run, name="client", args=("Append", "K1", "V4"))
    client_thread5 = Thread(target=client.run, name="client", args=("Append", "K2", "V1"))
    client_thread6 = Thread(target=client.run, name="client", args=("Append", "K2", "V2"))
    client_thread7 = Thread(target=client.run, name="client", args=("Append", "K2", "V3"))
    client_thread8 = Thread(target=client.run, name="client", args=("Append", "K2", "V4"))
    client_thread1.start()
    client_thread2.start()
    client_thread3.start()
    client_thread4.start()
    client_thread5.start()
    client_thread6.start()
    client_thread7.start()
    client_thread8.start()
    
    client_thread1.join()
    client_thread2.join()
    client_thread3.join()
    client_thread4.join()
    client_thread5.join()
    client_thread6.join()
    client_thread7.join()
    client_thread8.join()
        
    shardManager_thread.join()
        
    for t in serverG1_threads:
        t.join()
        
    for t in serverG2_threads:
        t.join()