import threading
import time

# Shared resources
shared_resource = []
message_queue = []

# Synchronization primitives
lock = threading.Lock()
semaphore = threading.Semaphore(2)
condition = threading.Condition()

# Thread function
def worker():
    thread_name = threading.current_thread().name

    with lock:
        shared_resource.append(thread_name)
        print(f"Thread {thread_name} modified the shared resource: {shared_resource}")

    if thread_name == "Thread-5":
        semaphore.release()

    semaphore.acquire()

    with condition:
        condition.wait()

    print(f"Thread {thread_name} woke up")

    if message_queue:
        message = message_queue.pop(0)
        print(f"Thread {thread_name} received a message: {message}")

    try:
        # Simulating an exception
        result = 1 / 0
    except ZeroDivisionError:
        print(f"Thread {thread_name} encountered a ZeroDivisionError")

    print(f"Thread {thread_name} finished execution")

# Creating and starting multiple threads
threads = []
for i in range(1, 6):
    t = threading.Thread(target=worker, name=f"Thread-{i}")
    threads.append(t)
    t.start()

# Simulating message passing
message = "Hello, threads!"
with lock:
    message_queue.append(message)

# Waiting for all the threads to acquire semaphore
while semaphore._value != 0:
    time.sleep(0.1)

# Sending a signal to wake up waiting threads
with condition:
    condition.notify_all()

# Waiting for all the threads to complete
for t in threads:
    t.join()

# Adding a delay to ensure all threads have finished execution
time.sleep(1)

print("All threads have finished execution")
