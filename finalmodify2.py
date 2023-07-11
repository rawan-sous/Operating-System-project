from threading import Lock, Semaphore, Condition
import threading
import time
import sys
import queue
import random


class Node:
    def __init__(self, id, name, currentState):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None

class ThreadSafe:
    def __init__(self, value):
        self.lock = Lock()
        self.value = value

    def increment(self):
        with self.lock:
            self.value += 1

    def get_value(self):
        with self.lock:
            return self.value
class ErrorHandling:
    def __init__(self):
        self.error = None

    def set_error(self, error):
        self.error = error

    def get_error(self):
        return self.error

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
    def set_state(self, id, state):
         current = self.head
         while current:
          if current.id == id:
            current.currentState = state
            return
         current = current.next


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
        LinkedList.append(self.thread_id, self.thread_name, "Running")
        self.semaphore.release()

    def get_priority(self):
        return random.randint(0, 9)


class Scheduler:
    def __init__(self):
        self.threads = queue.PriorityQueue()
        self.current_thread_index = 0

    def add_thread(self, thread):
        self.threads.put((thread.get_priority(), self.current_thread_index, thread))
        self.current_thread_index += 1

    def get_next_thread(self):
        _, _, thread = self.threads.get()
        return thread

    def get_thread(self, thread_id):
        threads = list(self.threads.queue)
        for _, _, thread in threads:
            if thread.get_thread_id() == thread_id:
                return thread
        return None

    def get_terminated_thread(self):
        terminated_threads = []
        while not self.threads.empty():
            _, _, thread = self.threads.get()
            if not thread.is_alive():
                terminated_threads.append(thread)
        return terminated_threads

    def is_empty(self):
        return self.threads.empty()


def main():
    linked_list = LinkedList()
    scheduler = Scheduler()
    semaphore = Semaphore(2)  # Semaphore with a value of 2
    lock = Lock()
    thread_sync = Condition()
   

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
            # Terminate a thread
            thread_id = input("Enter thread id: ")

            if thread_id == "":
                continue

            try:
                thread_id = int(thread_id)
            except ValueError:
                print("Invalid thread id. Please enter a number.")
                continue

            # Remove the thread from the thread management system
            linked_list.delete(thread_id)
            terminated_threads = scheduler.get_terminated_thread()
            if terminated_threads:
                for thread in terminated_threads:
                    thread.join()

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
                linked_list.set_state(thread.get_thread_id(),thread,"terminated")
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
                print("1. Acquire")
                print("2. Release")
                sync_choice = input("Enter your choice: ")
                if sync_choice == "":
                    continue

                try:
                    sync_choice = int(sync_choice)
                except ValueError:
                    print("Invalid choice. Please enter a number.")
                    continue
                if sync_choice == 1:
                    # Acquire
                    print("Acquire")
                    lock.acquire()
                    print("Thread acquired lock.")
                elif sync_choice == 2:
                    # Release
                    print("Release")
                    lock.release()
                    print("Thread released lock.")
                else:
                    print("Invalid choice")
            elif sync_choice == 2:
                # Semaphore
                print("Semaphore")
                print("1. Acquire")
                print("2. Release")
                sync_choice = input("Enter your choice: ")
                if sync_choice == "":
                    continue

                try:
                    sync_choice = int(sync_choice)
                except ValueError:
                    print("Invalid choice. Please enter a number.")
                    continue
                if sync_choice == 1:
                    # Acquire
                    print("Acquire")
                    semaphore.acquire()
                    print("Thread acquired semaphore.")
                elif sync_choice == 2:
                    # Release
                    print("Release")
                    semaphore.release()
                    print("Thread released semaphore.")
                else:
                    print("Invalid choice")
            elif sync_choice == 3:
                # Condition
                print("Condition")
                print("1. Wait")
                print("2. Notify")
                sync_choice = input("Enter your choice: ")
                if sync_choice == "":
                    continue

                try:
                    sync_choice = int(sync_choice)
                except ValueError:
                    print("Invalid choice. Please enter a number.")
                    continue
                if sync_choice == 1:
                    # Wait
                    print("Wait")
                    with thread_sync:
                        thread_sync.wait()
                    print("Thread waiting.")
                elif sync_choice == 2:
                    # Notify
                    print("Notify")
                    with thread_sync:
                        thread_sync.notify()
                    print("Thread notified.")
                else:
                    print("Invalid choice")

        elif choice == 6:
            # Thread Communication
            print("Thread Communication")
            print("1. Shared Memory")
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
                if linked_list.is_empty() or linked_list.head.next is None:
                    print("Error: Not enough threads created.")
                else:
                    shared_data = ThreadSafe(0)  # Initialize shared data with 0

                    def thread_func(shared_data):
                        shared_data.increment()
                        print("Thread shared data:", shared_data.get_value())

                    thread1 = linked_list.head.next.thread
                    thread2 = thread1.next.thread

                    thread1.set_entry_point(lambda: thread_func(shared_data))
                    thread2.set_entry_point(lambda: thread_func(shared_data))

                    thread1.start()
                    thread2.start()

                    thread1.join()
                    thread2.join()

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
