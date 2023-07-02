import threading

# Shared data
shared_data = []
shared_data_lock = threading.Lock()  # Lock to synchronize access to shared_data
condition = threading.Condition()  # Condition variable for thread signaling
barrier = threading.Barrier(3)  # Thread barrier to synchronize three threads

# Worker function
def worker(id):
    global shared_data
    
    # Perform some computation
    # ...

    # Acquire the lock before accessing the shared data
    shared_data_lock.acquire()
    
    try:
        # Access and modify the shared data
        shared_data.append(id)
        
        # Signal other threads that the shared data has been updated
        condition.notify_all()
        
    finally:
        # Release the lock after accessing the shared data
        shared_data_lock.release()

    # Perform thread synchronization using a barrier
    barrier.wait()

# Create multiple worker threads
num_threads = 3
threads = []

for i in range(num_threads):
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)

# Start the worker threads
for t in threads:
    t.start()

# Wait for all worker threads to finish
for t in threads:
    t.join()

# Perform thread synchronization using a condition variable
shared_data_lock.acquire()
try:
    # Wait until the shared data has been updated by all threads
    while len(shared_data) < num_threads:
        condition.wait()

    # Proceed with further processing once all threads have updated the shared data
    # ...
finally:
    shared_data_lock.release()

# Access the final shared data
print("Shared data:", shared_data)
