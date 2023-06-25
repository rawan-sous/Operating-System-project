import threading

# Node class representing a node in the linked list
class Node:
    def __init__(self, id, name, currentState):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None

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
        thread = Thread(thread_name, thread_id, entry_point)
        self.append(thread_id, thread_name, "Created")
        thread.start()

    def terminate_thread(self, thread_id):
        current = self.head
        prev = None
        while current:
            if current.id == thread_id:
                self.update_thread_state(thread_id, "Terminated")
                current.join()  # Wait for the thread to complete before termination
                self.delete(thread_id)
                return
            prev = current
            current = current.next
    
    def thread_command(self):
        i = 0
        while True:
            thread_id = input(f'Enter thread ID for thread {i+1}: ')
            name = input(f'Enter thread name for thread {i+1}: ')
            entry_point = input(f'Enter entry point for thread {i+1}: ')
            self.create_thread(name, thread_id, entry_point)
            i += 1

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
            self.update_thread_state(current.id, "Running")
            current.start()
            current = current.next


class Thread(threading.Thread):
    def __init__(self, name, ID, entry_point):
        threading.Thread.__init__(self)
        self.thread_name = name
        self.thread_ID = ID
        self.entry_point = entry_point

    def run(self):
        try:
            self.entry_point()
        except Exception as e:
            print(f"Error in thread {self.thread_name}: {str(e)}")
        finally:
            self.link.update_thread_state(self.thread_ID, "Terminated")

    def entry_point(self):
        print(f"Thread {self.thread_name} is running")


