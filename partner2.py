import threading
import heapq
import queue
import time

# Lock implementation
lock = threading.Lock()

# Semaphore implementation
semaphore = threading.Semaphore(value=1)

# Condition variable implementation
condition_variable = threading.Condition()

# Node class representing a node in the linked list
class Node:
    def __init__(self, id, name, currentState, thread=None):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None
        self.thread = thread

def run_threads(self):
    while not self.priority_queue.empty():
        thread = self.priority_queue.get()
        simulate_thread_execution(thread)

def simulate_thread_execution(thread):
    try:
        thread.entry_point()
    except Exception as e:
        print(f"Error in thread {thread.thread_name}: {str(e)}")

# Linked list class for managing the threads
class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, id, name, currentState):
        new_node = Node(id, name, currentState)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, id):
        if self.is_empty():
            return

        if self.head.id == id:
            self.head = self.head.next
            return

        current = self.head
        prev = None
        while current:
            if current.id == id:
                prev.next = current.next
                return
            prev = current
            current = current.next

    def create_thread(self, thread_name, thread_id, entry_point):
        thread = Thread(thread_name, thread_id, entry_point, self)  # Create the Thread object
        new_node = Node(thread_id, thread_name, "Created", thread)  # Create the Node object with the thread reference
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def thread_command(self):
        i = 0
        while True:
            thread_id = input(f'Enter thread ID for thread {i+1} (or "q" to quit): ')
            if thread_id.lower() == 'q':
                break
            elif not thread_id.isdigit():
                print('Invalid thread ID. Please enter a valid numeric ID.')
                continue
            name = input(f'Enter thread name for thread {i+1}: ')
            entry_point = input(f'Enter entry point for thread {i+1}: ')
            self.create_thread(name, int(thread_id), entry_point)
            i += 1

    def terminate_thread(self, thread_id):
        current = self.head
        while current:
            if current.id == thread_id:
                if current.thread.is_alive():  # Check if the thread has been started
                    current.thread.join()  # Wait for the thread to complete before termination
                self.delete(thread_id)
                return
            current = current.next

    def update_thread_state(self, thread_id, state):
        current = self.head
        while current:
            if current.id == thread_id:
                current.currentState = state
                return
            current = current.next

    def print_thread_list(self):
        current = self.head
        while current:
            print(f"Thread ID: {current.id}, Name: {current.name}, Current State: {current.currentState}")
            current = current.next

    def handle_error(self, error_message):
        print(f"Error: {error_message}")

    def handle_thread_creation(self, thread_name, thread_id, entry_point):
        print(f"Thread {thread_name} with ID {thread_id} is created with entry point {entry_point}")

    def execute_threads(self):
        current = self.head
        while current:
            current.thread.start()  # Start the thread
            self.update_thread_state(current.id, "Running")
            current = current.next


class Thread(threading.Thread):
    def __init__(self, name, ID, entry_point, link):
        threading.Thread.__init__(self)
        self.thread_name = name
        self.thread_ID = ID
        self.entry_point = entry_point
        self.link = link  # Reference to the LinkedList object

    def run(self):
        try:
            self.entry_point()
        except Exception as e:
            print(f"Error in thread {self.thread_name}: {str(e)}")
        finally:
            self.link.update_thread_state(self.thread_ID, "Terminated")



class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def is_empty(self):
        return len(self._queue) == 0

    def put(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def get(self):
        return heapq.heappop(self._queue)[-1]

class Scheduler:
    def __init__(self):
        self.thread_queue = queue.PriorityQueue()
        self.current_thread = None

    def add_thread(self, thread, priority):
        self.thread_queue.put((priority, thread))

    def run_threads(self):
        while not self.thread_queue.empty():
            _, thread = self.thread_queue.get()
            self.current_thread = thread
            self.current_thread.start()
            self.current_thread.join()
            self.current_thread = None

    def switch_threads(self):
        if self.current_thread:
            current_thread = self.current_thread
            self.current_thread = None
            current_thread.join()

            if not self.thread_queue.empty():
                _, next_thread = self.thread_queue.get()
                self.current_thread = next_thread
                self.current_thread.start()

def thread_entry_point():
    thread_name = threading.current_thread().name
    for i in range(5):
        print("Thread", thread_name, "is running")
        # Simulate some work
        time.sleep(1)
        # Perform context switch
        scheduler.switch_threads()

# Usage Example:

def thread_entry_point(name):
    print(f"Thread {name} is running")

    # Lock example
    lock.acquire()
    print(f"Thread {name} acquired the lock")
    time.sleep(1)
    print(f"Thread {name} releasing the lock")
    lock.release()

    # Semaphore example
    semaphore.acquire()
    print(f"Thread {name} acquired the semaphore")
    time.sleep(1)
    print(f"Thread {name} releasing the semaphore")
    semaphore.release()

    # Condition variable example
    with condition_variable:
        print(f"Thread {name} waiting on the condition variable")
        condition_variable.wait()
        print(f"Thread {name} received signal from the condition variable")


# Create the scheduler
scheduler = Scheduler()

# Add threads to the scheduler with priorities
thread1 = threading.Thread(target=thread_entry_point, args=("Thread 1",))
scheduler.add_thread(thread1, 0)

thread2 = threading.Thread(target=thread_entry_point, args=("Thread 2",))
scheduler.add_thread(thread2, 5)

thread3 = threading.Thread(target=thread_entry_point, args=("Thread 3",))
scheduler.add_thread(thread3, 3)


def execute_method(method):
    if method == "lock":
        lock.acquire()
        print(f"Lock acquired by Thread {threading.current_thread().name}")
        # Do something with the lock
        lock.release()
        print(f"Lock released by Thread {threading.current_thread().name}")
    elif method == "semaphore":
        semaphore.acquire()
        print(f"Semaphore acquired by Thread {threading.current_thread().name}")
        # Do something with the semaphore
        semaphore.release()
        print(f"Semaphore released by Thread {threading.current_thread().name}")
    elif method == "condition":
        with condition_variable:
            print(f"Signaling the condition variable by Thread {threading.current_thread().name}")
            condition_variable.notify()
    else:
        print("Invalid input. Please choose a valid method.")


while True:
    method = input("Choose the next method to execute (lock/semaphore/condition): ")
    execute_method(method)
    if method in ["lock", "semaphore", "condition"]:
        break

scheduler.run_threads()
def main():
   
   
    linked_list = LinkedList()

    # Create threads
    linked_list.create_thread("Thread 1", 1, thread_entry_point)
    linked_list.create_thread("Thread 2", 2, thread_entry_point)

    # Print thread list
    linked_list.print_thread_list()

    # Terminate a thread
    thread_id = int(input("Enter thread ID to terminate: "))
    linked_list.terminate_thread(thread_id)

    # Print updated thread list
    linked_list.print_thread_list()

    # Test thread command
    linked_list.thread_command()

    # Print updated thread list
    linked_list.print_thread_list()

    # Update thread state
    thread_id = int(input("Enter thread ID to update state: "))
    new_state = input("Enter new state for the thread: ")
    linked_list.update_thread_state(thread_id, new_state)

    # Print updated thread list
    linked_list.print_thread_list()

    # Test handle_error function
    error_message = "Error occurred!"
    linked_list.handle_error(error_message)

    # Test handle_thread_creation function
    thread_name = "Thread 3"
    thread_id = 3
    entry_point = thread_entry_point
    linked_list.handle_thread_creation(thread_name, thread_id, entry_point)

    # Print updated thread list
    linked_list.print_thread_list()

    # Create the scheduler
    scheduler = Scheduler()

    # Add threads to the scheduler with priorities
    scheduler.add_thread(linked_list.head.thread, 2)
    scheduler.add_thread(linked_list.head.next.thread, 1)

    # Continue with the remaining code...
    # Test handle_error function
    error_message = "Error occurred!"
    linked_list.handle_error(error_message)

    # Test handle_thread_creation function
    thread_name = "Thread 3"
    thread_id = 3
    entry_point = thread_entry_point
    linked_list.handle_thread_creation(thread_name, thread_id, entry_point)

    # Print updated thread list
    linked_list.print_thread_list()

    # Run the threads in the scheduler
    scheduler.run_threads()

    # Print updated thread list
    linked_list.print_thread_list()





if __name__ == "__main__":
    main()