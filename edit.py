from threading import Lock, Semaphore ,Condition
import threading
import time
import sys
import queue
import random


class Node:
    def __init__(self, id, name, currentState, priority):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.priority = priority
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def append(self, id, name, currentState, priority):
        new_node = Node(id, name, currentState, priority)
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
        print("Thread ID\tThread Name\tCurrent State\tPriority")
        while current:
            print(f"{current.id}\t\t{current.name}\t\t{current.currentState}\t\t{current.priority}")
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
        self.blocked_event = threading.Event()  # Event to indicate whether the thread is blocked or not
        self.priority = self.get_priority()  # Set the initial priority

    def run(self):
        self.semaphore.acquire()
        self.state = "running"
        self.semaphore.release()
        self.entry_point()
        self.semaphore.acquire()
        self.state = "terminated"
        self.semaphore.release()

    def block(self):
        self.blocked_event.wait()  # Wait until unblocked

    def unblock(self):
        self.blocked_event.set()  # Set the event to unblocked state

    def set_entry_point(self, entry_point):
        self.entry_point = entry_point

    def get_entry_point(self):
        return self.entry_point

    def get_thread_name(self):
        return self.thread_name

    def get_thread_id(self):
        return self.thread_id

    def get_priority(self):
        return random.randint(0, 9)


class MyThread(Thread):
    released_thread_ids = []

    def __init__(self, thread_id, thread_name, entry_point, semaphore, lock):
        super().__init__()
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.entry_point = entry_point
        self.semaphore = semaphore
        self.lock = lock
        self.state = "created"

    def run(self):
        self.semaphore.acquire()
        self.state = "running"
        self.semaphore.release()
        self.entry_point()
        self.semaphore.acquire()
        self.state = "terminated"
        self.semaphore.release()
        self.lock.acquire()
        MyThread.released_thread_ids.append(self.thread_id)
        self.lock.release()


class Scheduler:
    def __init__(self):
        self.threads = queue.PriorityQueue()
        self.current_thread_index = 0

    def add_thread(self, thread):
        self.threads.put((thread.priority, thread))

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


class Barrier:
    def __init__(self, count):
        self.count = count
        self.waiting_queue = queue.Queue()
        self.release_lock = threading.Lock()
        self.blocked_event = threading.Event()  # Event to indicate whether the threads are blocked or not

    def wait(self):
        self.count -= 1
        if self.count > 0:
            self.waiting_queue.put(threading.current_thread())
            self.blocked_event.wait()  # Wait until unblocked by the last thread
        else:
            with self.release_lock:
                while not self.waiting_queue.empty():
                    thread = self.waiting_queue.get()
                    thread.unblock()

    def unblock(self):
        self.blocked_event.set()  # Set the event to unblocked state


class ThreadSafe:
    def __init__(self, value=None):
        self.value = value
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        with self.lock:
            self.value -= 1

    def set_value(self, new_value):
        with self.lock:
            self.value = new_value

    def get_value(self):
        with self.lock:
            return self.value


def main():
    linked_list = LinkedList()
    scheduler = Scheduler()
    semaphore = Semaphore(2)  # Semaphore with a value of 2
    condition = Condition()
    lock = Lock()
    barrier = Barrier(1)  # Using Barrier with a count of 3
    shared_memory = ThreadSafe()


    while True:
        print("Thread Management Simulator")
        print("1. Create Thread")
        print("2. Terminate Thread")
        print("3. Display Thread List")
        print("4. Schedule and Execute Threads")
        print("5. Thread Synchronization")
        print("6. Thread Communication")
        print("7. Exit")
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

            # Get the priority for the thread
            priority = random.randint(0, 9)

            # Example: Create a new thread with a specific entry point function
           # Example: Create a new thread with a specific entry point function and priority
            entry_point = my_entry_function
            priority = random.randint(0, 9)
            new_thread = Thread(thread_id, thread_name, entry_point, semaphore, lock, priority)


            # Add the thread to the thread management system
            linked_list.append(thread_id, thread_name, "created", priority)
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
                linked_list.delete(thread.get_thread_id())

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

            try:
                sync_choice = int(sync_choice)
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue

            if sync_choice == 1:
                # Lock
                print("Lock")
                lock.acquire()
                print(f"Lock acquired by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")
                print(0)
                # ...
                lock.release()
                print(f"Lock released by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")

            elif sync_choice == 2:
                # Semaphore
                print("Semaphore")
                semaphore.acquire()
                print(f"Semaphore acquired by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")
                print(0)
                # ...
                semaphore.release()
                print(f"Semaphore released by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")

            elif sync_choice == 3:
                # Condition
                print("Condition")
                condition.acquire()
                print(f"Condition acquired by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")
                # Condition wait
                condition.wait()
                print(f"Condition released by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")
                # Condition signal
                condition.notify()
                print(f"Condition signaled by Thread {threading.current_thread().name}with ID {threading.current_thread().ident} ")
                condition.release()

            else:
                print("Invalid choice")

        elif choice == 6:
            # Thread Communication - Shared Memory
            print("Thread Communication - Shared Memory")
            print("1. Read")
            print("2. Write")
            sync_choice = input("Enter your choice: ")
            if sync_choice == "":
                continue

            try:
                sync_choice = int(sync_choice)
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue

            if sync_choice == 1:
                # Read
                print("Read")
                semaphore.acquire()
                print(f"Semaphore acquired by Thread {threading.current_thread().name}with ID {threading.current_thread().ident}  for reading")
                # Read from shared memory
                lock.acquire()
                print(f"Lock acquired by Thread {threading.current_thread().name}with ID {threading.current_thread().ident}  for reading")
                # Read operation on shared memory
                print("Shared memory value:", shared_memory.get_value())
                lock.release()
                print(f"Lock released by Thread {threading.current_thread().name}with ID {threading.current_thread().ident}  after reading")
                semaphore.release()
                print(f"Semaphore released by Thread {threading.current_thread().name}with ID {threading.current_thread().ident}  after reading")

            elif sync_choice == 2:
                # Write
                print("Write")
                semaphore.acquire()
                print(f"Semaphore acquired by Thread {threading.current_thread().name} with ID {threading.current_thread().ident} for writing")
                # Write to shared memory
                lock.acquire()
                print(f"Lock acquired by Thread {threading.current_thread().name} with ID {threading.current_thread().ident} for writing")
                # Write operation on shared memory
                new_value = input("Enter shared memory value: ")
                shared_memory.set_value(new_value)
                lock.release()
                print(f"Lock released by Thread {threading.current_thread().name} with ID {threading.current_thread().ident} after writing")
                semaphore.release()
                print(f"Semaphore released by Thread {threading.current_thread().name} with ID {threading.current_thread().ident} after writing")

            else:
                print("Invalid choice")

        elif choice == 7:
            sys.exit()

        else:
            print("Invalid choice. Please enter a valid choice.")


def my_entry_function():
    # Example entry point function for a thread
    print(f"This is the entry point for Thread {threading.current_thread().name} with id {threading.current_thread().ident}")


if __name__ == "__main__":
     main()
