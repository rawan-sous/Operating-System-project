Thread Creation and Termination:
#Provide an interface or command to create new threads within the
#simulator.
# Allow users to specify the entry point function for each thread.
# Implement thread termination mechanisms, such as explicit termination
#requests or thread completion detection.
import threading
import time
import random
import sys
import os
import queue
def entry_function():
        print("This is the entry point function for the thread.")
class node:
    def __init__(self, id, name, currentState):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None

class linkedList:
    def __init__(self):
        self.head = None
    def is_empty(self):
        return self.head is None
    def append(self, id, name, currentState):
        new_node = node(id, name, currentState)
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
    

    

# ...

# Inside the linkedList class, in the create_thread method
# ...
    def create_thread(self, thread_name, thread_id, entry_point):
        new_thread = thread(thread_name, thread_id, entry_function)
        self.append(thread_id, thread_name, "created")
        new_thread.start()





    def terminate_thread(self, thread_id):
        current = self.head
        prev = None
        while current:
            if current.id == thread_id:
                self.update_thread_state(thread_id, "Terminated")
                current.join()
                self.delete(thread_id)
                return
            prev = current
            current = current.next
    def thread_command(self):
        print("Thread Creation and Termination")
        print("1. Create Thread")
        print("2. Terminate Thread")
        print("3. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            thread_name = input("Enter thread name: ")
            thread_id = int(input("Enter thread id: "))

            entry_point = entry_function()
            self.create_thread(thread_name, thread_id,entry_point)
        elif choice == 2:
            thread_id = int(input("Enter thread id: "))
            self.terminate_thread(thread_id)
        elif choice == 3:
            sys.exit()
        else:
            print("Invalid choice")
    def update_thread_state(self, thread_id, state):
        current = self.head
        while current:
            if current.id == thread_id:
                current.currentState = state
                return
            current = current.next
    def display(self):
        current = self.head
        print("Thread ID\tThread Name\tCurrent State")
        while current:
            print(f"{current.id}\t\t{current.name}\t\t{current.currentState}")
            current = current.next
class thread(threading.Thread):
    def __init__(self, thread_name, thread_id, entry_point):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_id = thread_id
        self.entry_point = entry_point
    def run(self):
        print(f"Thread {self.thread_name} is running")
        time.sleep(1)
        print(f"Thread {self.thread_name} is exiting")
        time.sleep(1)
        #Thread Execution and Context Switching:
 #Implement a scheduler that determines the order in which threads are executed.
# Simulate the execution of threads by executing their associated functionsor code blocks.
# Implement context switching to switch between threads, allowing eachthread to make progress and share the CPU.

class scheduler:
    def __init__(self):
        self.ready_queue = queue.Queue()
        self.current_thread = None
        self.terminated_queue = queue.Queue()
    def add_thread(self, thread):
        self.ready_queue.put(thread)
    def get_next_thread(self):
        if self.ready_queue.empty():
            return None
        else:
            return self.ready_queue.get()
    def schedule(self):
        next_thread = self.get_next_thread()
        if next_thread is None:
            return
        if self.current_thread is not None:
            self.current_thread.save()
        self.current_thread = next_thread
        self.current_thread.restore()
    def terminate_thread(self, thread):
        self.terminated_queue.put(thread)
    def get_terminated_thread(self):
        if self.terminated_queue.empty():
            return None
        else:
            return self.terminated_queue.get()
#Synchronization Primitives:
#Include common synchronization primitives like locks, semaphores, orcondition variables.
# Allow users to create and use these primitives to synchronize access to shared resources among threads.
#Implement appropriate mechanisms to handle blocking and waking up threads waiting on synchronization primitives.
class lock:
    def __init__(self):
        self.locked = False
        self.waiting_queue = queue.Queue()
    def acquire(self):
        if self.locked:
            self.waiting_queue.put(threading.current_thread())
            threading.current_thread().block()
        else:
            self.locked = True
    def release(self):
        if self.waiting_queue.empty():
            self.locked = False
        else:
            thread = self.waiting_queue.get()
            thread.unblock()
class semaphore:
    def __init__(self, value):
        self.value = value
        self.waiting_queue = queue.Queue()
    def wait(self):
        self.value -= 1
        if self.value < 0:
            self.waiting_queue.put(threading.current_thread())
            threading.current_thread().block()
    def signal(self):
        self.value += 1
        if self.value <= 0:
            thread = self.waiting_queue.get()
            thread.unblock()
class condition:
    def __init__(self):
        self.waiting_queue = queue.Queue()
    def wait(self):
        self.waiting_queue.put(threading.current_thread())
        threading.current_thread().block()
    def signal(self):
        thread = self.waiting_queue.get()
        thread.unblock()
#Thread Synchronization:
#Implement thread synchronization mechanisms to ensure proper coordination and order of execution.
#Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class barrier:
    def __init__(self, count):
        self.count = count
        self.waiting_queue = queue.Queue()
    def wait(self):
        self.count -= 1
        if self.count > 0:
            self.waiting_queue.put(threading.current_thread())
            threading.current_thread().block()
        else:
            while not self.waiting_queue.empty():
                thread = self.waiting_queue.get()
                thread.unblock()
class join:
    def __init__(self, thread):
        self.thread = thread
    def wait(self):
        self.thread.join()
#Thread Communication:
#Implement thread communication mechanisms to allow threads to communicate with each other.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class message:
    def __init__(self, message):
        self.message = message
class mailbox:
    def __init__(self):
        self.messages = queue.Queue()
    def send(self, message):
        self.messages.put(message)
    def receive(self):
        return self.messages.get()
#Thread Safety:
#Implement thread safety mechanisms to ensure that shared resources are accessed in a thread-safe manner.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_safe:
    def __init__(self, value):
        self.value = value
        self.lock = lock()
    def increment(self):
        self.lock.acquire()
        self.value
        self.lock.release()
    def decrement(self):
        self.lock.acquire()
        self.value -= 1
        self.lock.release()
    def get_value(self):
        return self.value
#Thread Local Storage:
#Implement thread local storage to allow each thread to have its own private data.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_local:
    def __init__(self):
        self.local = {}
    def set(self, value):
        self.local[threading.current_thread()] = value
    def get(self):
        return self.local[threading.current_thread()]
#Thread Pooling:
#Implement thread pooling to allow threads to be reused for multiple tasks.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_pool:
    def __init__(self):
        self.pool = []
        self.lock = lock()
    def add_thread(self, thread):
        self.lock.acquire()
        self.pool.append(thread)
        self.lock.release()
    def get_thread(self):
        self.lock.acquire()
        if len(self.pool) > 0:
            thread = self.pool.pop()
        else:
            thread = None
        self.lock.release()
        return thread
#Thread Cancellation:
#Implement thread cancellation to allow threads to be cancelled or terminated.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_cancellation:
    def __init__(self):
        self.lock = lock()
    def cancel(self, thread):
        self.lock.acquire()
        thread.cancel()
        self.lock.release()
#Thread Scheduling:
#Implement thread scheduling to allow threads to be scheduled for execution.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_scheduler:
    def __init__(self):
        self.ready_queue = queue.Queue()
        self.blocked_queue = queue.Queue()
        self.lock = lock()
    def add_thread(self, thread):
        self.lock.acquire()
        self.ready_queue.put(thread)
        self.lock.release()
    def get_thread(self):
        self.lock.acquire()
        if self.ready_queue.empty():
            thread = None
        else:
            thread = self.ready_queue.get()
        self.lock
        return thread
    def block_thread(self, thread):
        self.lock.acquire()
        self.blocked_queue.put(thread)
        self.lock.release()
    def unblock_thread(self):
        self.lock.acquire()
        if self.blocked_queue.empty():
            thread = None
        else:
            thread = self.blocked_queue.get()
        self.lock.release()
        return thread
#Thread Priority:
#Implement thread priority to allow threads to be scheduled for execution based on priority.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_priority:
    def __init__(self):
        self.ready_queue = queue.Queue()
        self.blocked_queue = queue.Queue()
        self.lock = lock()
    def add_thread(self, thread):
        self.lock.acquire()
        self.ready_queue.put(thread)
        self.lock.release()
    def get_thread(self):
        self.lock.acquire()
        if self.ready_queue.empty():
            thread = None
        else:
            thread = self.ready_queue.get()
        self.lock
        return thread
    def block_thread(self, thread):
        self.lock.acquire()
        self.blocked_queue.put(thread)
        self.lock.release()
    def unblock_thread(self):
        self.lock.acquire()
        if self.blocked_queue.empty():
            thread = None
        else:
            thread = self.blocked_queue.get()
        self.lock.release()
        return thread
#Thread Synchronization:
#Implement thread synchronization to allow threads to synchronize their execution with other threads.
# Support operations like thread signaling, waiting, and notifying using
#synchronization primitives.
# Provide mechanisms for thread coordination, such as thread barriers or thread join operations.
class thread_synchronization:
    def __init__(self):
        self.lock = lock()
        self.condition = condition()
    def wait(self):
        self.condition.wait()
    def notify(self):
        self.condition.notify()
    def acquire(self):
        self.lock.acquire()
    def release(self):
        self.lock.release()


# Error Handling and Exception Handling:
# Implement error handling mechanisms to handle exceptions and errors
# that occur during thread execution.
# Provide appropriate error reporting and recovery mechanisms to maintain
# the stability of the system.

# Error Handling:
# Implement error handling mechanisms to handle exceptions and errors
# that occur during thread execution.
# Provide appropriate error reporting and recovery mechanisms to maintain
# the stability of the system.
class error_handling:
    def __init__(self):
        self.lock = lock()
        self.error = None
    def set_error(self, error):
        self.lock.acquire()
        self.error = e
        self.lock.release()
    def get_error(self):
        self.lock.acquire()
        error = self.error
        self.lock.release()
        return error







def main():
    linked_list = linkedList()
    #thread_pool = thread_pool()
    thread_scheduler = scheduler()

    while True:
        print("Thread Creation and Termination")
        print("1. Create Thread")
        print("2. Terminate Thread")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            thread_name = input("Enter thread name: ")
            thread_id = int(input("Enter thread id: "))
            entry_point = entry_function
            linked_list.create_thread(thread_name, thread_id, entry_point)

        elif choice == 2:
            thread_id = int(input("Enter thread id: "))
            linked_list.terminate_thread(thread_id)

        elif choice == 3:
            sys.exit()

        else:
            print("Invalid choice")

        thread_scheduler.schedule()

        terminated_thread = thread_scheduler.get_terminated_thread()
        while terminated_thread is not None:
            thread_pool.add_thread(terminated_thread)
            terminated_thread = thread_scheduler.get_terminated_thread()

        linked_list.display()

if __name__ == "__main__":
    main()
