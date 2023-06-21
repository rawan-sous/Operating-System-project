import threading

# Global variable to track the current thread index
current_thread_index = 0
# List of threads to be executed
threads = []
# Lock object for thread synchronization
lock = threading.Lock()
# Semaphore for mutual exclusion
semaphore = threading.Semaphore(1)

# Custom Thread class
class MyThread(threading.Thread):
    def __init__(self, name, function):
        super().__init__()
        self.name = name
        self.function = function

    def run(self):
        self.function()

# Function to simulate thread execution
def thread_function():
    global current_thread_index

    with semaphore:
        with lock:
            # Get the current thread index
            thread_index = current_thread_index
            # Increment the thread index for the next thread
            current_thread_index += 1

        # Simulate the execution of the thread
        print(f"Thread {thread_index} is executing.")

# Function to implement context switching
def context_switching():
    global current_thread_index

    with lock:
        # Determine the next thread index
        next_thread_index = (current_thread_index + 1) % len(threads)
        # Set the current thread index to the next thread
        current_thread_index = next_thread_index

    # Simulate context switching between threads
    print(f"Context switching from Thread {current_thread_index - 1} to Thread {current_thread_index}.")

# Number of threads to create
num_threads = 5

# Create threads and add them to the list
for i in range(num_threads):
    thread_name = f"Thread {i+1}"
    thread = MyThread(thread_name, thread_function)
    threads.append(thread)

# Start the threads
for thread in threads:
    thread.start()

# Simulate context switching between threads
while True:
    context_switching()
