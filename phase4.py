import threading
import time

# Define a semaphore
semaphore = threading.Semaphore(1)


# Node class representing a node in the linked list
class Node:
    def __init__(self, id, name, currentState, thread=None):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None
        self.thread = thread


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
            thread_id = input(f'Enter thread ID for thread {i + 1} (or "q" to quit): ')
            if thread_id.lower() == 'q':
                break
            elif not thread_id.isdigit():
                print('Invalid thread ID. Please enter a valid numeric ID.')
                continue
            name = input(f'Enter thread name for thread {i + 1}: ')
            entry_point = input(f'Enter entry point for thread {i + 1}: ')
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

    def execute_threads(self):
        current = self.head
        while current:
            current.thread.start()  # Start the thread
            self.update_thread_state(current.id, "Running")
            current.thread.join()  # Wait for the thread to complete
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


class Scheduler:
    def __init__(self, linked_list):
        self.linked_list = linked_list

    def schedule_threads(self):
        # Print thread list
        self.linked_list.print_thread_list()

        # Execute threads
        self.linked_list.execute_threads()


def simulate_thread_execution():
    # Enter critical section (acquire semaphore)
    semaphore.acquire()

    # Perform critical operations
    print(f"Executing critical section of thread: {threading.current_thread().name}")

    # Exit critical section (release semaphore)
    semaphore.release()

    time.sleep(0.1)  # Simulate a context switch by sleeping for a short duration


def main():
    linked_list = LinkedList()

    # Create threads
    linked_list.create_thread("Thread 1", 1, simulate_thread_execution)
    linked_list.create_thread("Thread 2", 2, simulate_thread_execution)

    # Print thread list
    linked_list.print_thread_list()

    # Terminate a thread
    thread_id = int(input("Enter thread ID to terminate: "))
    linked_list.terminate_thread(thread_id)

    # Print updated thread list
    linked_list.print_thread_list()

    # Execute remaining threads
    linked_list.execute_threads()

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
    entry_point = simulate_thread_execution
    linked_list.handle_thread_creation(thread_name, thread_id, entry_point)

    # Print updated thread list
    linked_list.print_thread_list()

    # Create a scheduler
    scheduler = Scheduler(linked_list)

    # Schedule and execute threads
    scheduler.schedule_threads()


if __name__ == "__main__":
    main()

