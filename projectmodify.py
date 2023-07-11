from threading import Lock, Semaphore, Condition
import threading
import time
import sys
import queue
import random



class Node:
    def __init__(self, id, name, currentState, ):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None

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

    def display(self):
        current = self.head
        print("Thread ID\tThread Name\tCurrent State")
        while current:
            print(f"{current.id}\t\t{current.name}\t\t{current.currentState}")
            current = current.next

    def set_state(self, id, state):
        current = self.head
        while current:
            if current.id == id:
                current.currentState = state
                return
            current = current.next



class Thread(threading.Thread):
    def __init__(self, thread_id, thread_name, entry_point, semaphore, lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.entry_point = entry_point
        self.semaphore = semaphore
        self.lock = lock
        self.state = "created"  # Initialize the state as "created"
        

    def run(self):
        self.semaphore.acquire()  # Acquire semaphore
        print(f"Thread {self.thread_name} is running")
        self.set_state("running")  # Update the state to "running"
        time.sleep(1)
        self.semaphore.release()  # Release semaphore

    def set_state(self, state):
        self.lock.set_state(self.thread_id, state)

    def set_entry_point(self, entry_point):
        self.entry_point = entry_point

    def get_entry_point(self):
        return self.entry_point

    def get_thread_name(self):
        return self.thread_name

    def get_thread_id(self):
        return self.thread_id

    def restore(self):
     
        self.semaphore.acquire()
        self.look.append(self.thread_id, self.thread_name, "Running")
        self.semaphore.release()

    def get_priority(self):
        return random.randint(0, 9)




class Scheduler:
    def __init__(self):
        self.threads = queue.PriorityQueue()
        self.current_thread_index = 0

    def add_thread(self, thread):
        self.threads.put((thread.get_priority(), thread))

    def get_next_thread(self):
         _, thread = self.threads.get()
         return thread

    def get_thread(self, thread_id):
        threads = list(self.threads.queue)
        for _, thread in threads:
            if thread.get_thread_id() == thread_id:
                return thread
        return None

    def get_terminated_thread(self):
        terminated_threads = []
        while not self.threads.empty():
            _, thread = self.threads.get()
            if not thread.is_alive():
                terminated_threads.append(thread)
        return terminated_threads

    def is_empty(self):
       return self.threads.empty()

    


class Lock:
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

        if not self.waiting_queue.empty():
            thread = self.waiting_queue.get()
            thread.unblock()
        else:
            self.locked = False
    
    def is_locked(self):
        return self.locked
    
    def locked_by(self):
        return self.locked_by
    
    def get_waiting_queue(self):
        return self.waiting_queue
    
    def get_lock(self):
        return self.locked
    
    def get_locked_by(self):
        return self.locked_by
 


class Condition:
    def __init__(self):
        self.waiting_queue = queue.Queue()

    def wait(self):
        self.waiting_queue.put(threading.current_thread())
        threading.current_thread().block()

    def signal(self):
        thread = self.waiting_queue.get()
        thread.unblock()


class Barrier:
    def __init__(self, count):
        self.count = count
        self.waiting_queue = queue.Queue()
        self.release_lock = threading.Lock()

    def wait(self):
        self.count -= 1
        if self.count > 0:
            self.waiting_queue.put(threading.current_thread())
            threading.current_thread().block()
        else:
            with self.release_lock:
                while not self.waiting_queue.empty():
                    thread = self.waiting_queue.get()
                    thread.unblock()


class Join:
    def __init__(self, thread):
        self.thread = thread

    def wait(self):
        self.thread.join()

class Message:
    def __init__(self, message):
        self.message = message

class Mailbox:
    def __init__(self):
        self.messages = queue.Queue()

    def send(self, message):
        self.messages.put(message)

    def receive(self):
        return self.messages.get()

class ThreadSafe:
    def __init__(self, value):
        self.value = value
        self.lock = Lock()

    def increment(self):
        self.lock.acquire()
        self.value += 1
        self.lock.release()

    def decrement(self):
        self.lock.acquire()
        self.value -= 1
        self.lock.release()

    def get_value(self):
        return self.value



class ThreadLocal:
    def __init__(self):
        self.local = {}

    def set(self, value):
        self.local[threading.current_thread()] = value

    def get(self):
        return self.local[threading.current_thread()]

class ThreadPool:
    def __init__(self):
        self.pool = []
        self.lock = Lock()

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

class ThreadCancellation:
    def __init__(self):
        self.lock = Lock()

    def cancel(self, thread):
        self.lock.acquire()
        thread.cancel()
        self.lock.release()

class ThreadScheduler:
    def __init__(self):
        self.ready_queue = queue.Queue()
        self.blocked_queue = queue.Queue()
        self.lock = Lock()

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
        self.lock.release()
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

class ThreadPriority:
    def __init__(self):
        self.ready_queue = queue.Queue()
        self.blocked_queue = queue.Queue()
        self.lock = Lock()

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
        self.lock.release()
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

class ThreadSynchronization:
    def __init__(self):
        self.lock = Lock()
        self.condition = Condition()

    def acquire(self):
        with self.condition:
            self.lock.acquire()

    def release(self):
        with self.condition:
            self.lock.release()
  
    def wait(self):
        self.lock.acquire()
        self.condition.wait()
        self.lock.release()

    def notify(self):
        with self.condition:
            print("Thread notified.")
            self.condition.notify_all()




class ErrorHandling:
    def __init__(self):
        self.lock = Lock()
        self.error = None

    def set_error(self, error):
        self.lock.acquire()
        self.error = error
        self.lock.release()

    def get_error(self):
        self.lock.acquire()
        error = self.error
        self.lock.release()
        return error
def main():
    linked_list = LinkedList()
    scheduler = Scheduler()
    semaphore = Semaphore(2)  # Semaphore with a value of 2
    lock = LinkedList()
    thread_sync = ThreadSynchronization()

    while True:
        print("Thread Management Simulator")
        print("1. Create Thread")
        print("2. Terminate Thread")
        print("3. Display Thread List")
        print("4. Schedule and Execute Threads")
        print("5. Thread Synchronization")
        print("6. Thread Communication")
        print("7. Error Handling")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == "":
            continue

        try:
            choice = int(choice)
        except ValueError:
            print("Invalid choice. Please enter a number.")
            continue

        if choice == 1:
            # Create a new thread
            thread_name = input("Enter thread name: ")
            thread_id = input("Enter thread id: ")

            if thread_id == "":
                continue

            try:
                thread_id = int(thread_id)
            except ValueError:
                print("Invalid thread id. Please enter a number.")
                continue

            
            # Example: Create a new thread with a specific entry point function
            entry_point = my_entry_function
            new_thread = Thread(thread_id, thread_name, entry_point, semaphore, lock)

            # Add the thread to the thread management system
            linked_list.append(thread_id, thread_name, "created")
            scheduler.add_thread(new_thread)

        elif choice == 2:
            thread_id = input("Enter thread id: ")

            if thread_id == "":
                    continue

            try:
                    thread_id = int(thread_id)
            except ValueError:
                    print("Invalid thread id. Please enter a number.")
                    continue

                # Get the thread from the thread management system
            thread = scheduler.get_thread(thread_id)
            if thread is not None and thread.is_alive():
                    thread.join()
            linked_list.delete(thread_id)

        elif choice == 3:
            # Display the current thread list
            print("Current Thread List:")
            linked_list.display()
            print()

        elif choice == 4:
           # Schedule and execute the threads
                while not scheduler.is_empty():
                    thread = scheduler.get_next_thread()
                    thread.start()
                    thread.join()

                    # Update the thread states after joining
                    linked_list.set_state(thread.get_thread_id(), "terminated")

                print("All threads have completed.")


        elif choice == 5:
            # Thread Synchronization
            print("Thread Synchronization")
            print("1. Lock")
            print("2. Semaphore")
            print("3. Condition")
            sync_choice = input("Enter your choice: ")
            if sync_choice == "":
                continue
           


            

            if sync_choice == 1:
                # Lock
                lock.acquire()
                print("Lock acquired.")

            elif sync_choice == 2:
                # Semaphore
                semaphore.acquire()
                print("Semaphore acquired.")

            elif sync_choice == 3:
                # Condition
                thread_sync.acquire()
                print("Thread waiting...")

                # Wait for the thread to be notified
                thread_sync.wait()

        elif choice == 6:
            # Thread Communication
            print("Thread Communication")
            print("1. Shared Memory")
            print("2. Message Passing")
            comm_choice = input("Enter your choice: ")

            if comm_choice == "":
                continue

            try:
                comm_choice = int(comm_choice)
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue

            if comm_choice == 1:
                # Shared Memory
                shared_data = ThreadSafe("Shared Data")

                def thread_func():
                    shared_data.increment()
                    print("Thread shared data:", shared_data.get_value())

                thread1 = Thread(1, "Thread 1", thread_func)
                thread2 = Thread(2, "Thread 2", thread_func)

                thread1.start()
                thread2.start()

                thread1.join()
                thread2.join()

            

            else:
                print("Invalid choice")

        elif choice == 7:
            # Error Handling
            error_handler = ErrorHandling()

            def error_thread_func():
                try:
                    raise ValueError("Simulated error")
                except Exception as e:
                    error_handler.set_error(e)

            error_thread = Thread(1, "Error Thread", error_thread_func)
            error_thread.start()
            error_thread.join()

            error = error_handler.get_error()
            if error is not None:
                print("Error occurred:", error)

        elif choice == 8:
            # Exit the thread management simulator
            sys.exit()

        else:
            print("Invalid choice")



def my_entry_function():
    # Example entry point function for a thread
    print(f"This is the entry point for Thread {threading.current_thread().name} with id {threading.current_thread().ident}")

if __name__ == "__main__":
    main()