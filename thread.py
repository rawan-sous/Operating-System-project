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

    def print_list(self):
        current = self.head
        while current:
            print(f"Thread ID: {current.id}, Name: {current.name}, Current State: {current.currentState}")
            current = current.next

class Thread(threading.Thread):
 
    link = LinkedList()

    def __init__(self, name, ID,entry_point):
        threading.Thread.__init__(self)
        self.thread_name = name
        self.thread_ID = ID
        self.entry_point = entry_point
    def run(self):
        self.entry_point()