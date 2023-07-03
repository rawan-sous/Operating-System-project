import threading

# Node class representing a node in the linked list
class Node:
    def __init__(self, id, name, currentState):
        self.id = id
        self.name = name
        self.currentState = currentState
        self.next = None
        self.thread = None
        self.thread_name = None
        self.thread_ID = None
        self.entry_point = None
        self.link = None
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
        new_thread = Thread(thread_name, thread_id, entry_point, self)
        new_node = Node(thread_id, thread_name, "Created")
        new_node.thread = new_thread  # Assign the Thread object to the Node
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node


    def terminate_thread(self, thread_id):
        current = self.head
        prev = None
        while current:
            if current.id == thread_id:
                self.update_thread_state(thread_id, "Terminated")
                thread = current.thread  # Retrieve the Thread object from the Node
                thread.join()  # Wait for the thread to complete before termination
                self.delete(thread_id)
                return
            prev = current
            current = current.next

    
    def thread_command(self):
        i = 0
        while True:
            thread_id = input(f'Enter thread ID for thread {i+1} (or "q" to quit): ')
            if thread_id.lower() == 'q':
                break
            name = input(f'Enter thread name for thread {i+1}: ')
            
            self.create_thread(name, thread_id,  entry_point_function)
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
            thread = current.thread  # Retrieve the Thread object from the Node
            thread.start()  # Call start() on the Thread object
            current = current.next



class Thread(threading.Thread):
    def __init__(self, name, ID, entry_point, link):
        threading.Thread.__init__(self)
        self.thread_name = name
        self.thread_ID = ID
        self.entry_point = entry_point
        self.link = link

    def run(self):
        self.entry_point()  # Call the entry point function

    # Rest of the Thread class implementation

def entry_point_function():
    # Entry point function for thread 1
    thread_name = threading.current_thread().name
    thread_ID = threading.current_thread().ident
    print(f"Thread {thread_name} ({thread_ID}) is running")



def main():
    linked_list = LinkedList()

    # Create threads and specify entry point functions
    linked_list.create_thread("Thread 1", 1, entry_point_function)
    linked_list.create_thread("Thread 2", 2, entry_point_function)

    # Print the list of threads
    linked_list.print_thread_list()

    # Test the handle_thread_creation function
    linked_list.handle_thread_creation("Thread 3", 3, entry_point_function)

    # Execute the threads
    linked_list.execute_threads()
    linked_list.print_thread_list()
    linked_list.terminate_thread(1)

# Call the main function
if __name__ == "__main__":
    main()
