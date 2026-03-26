from player.node import Node

# ==== Stack cơ bản ====
class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        temp = self.top
        self.top = self.top.next
        return temp.nhan_vat

    def peek(self):
        if self.top is None:
            return None
        return self.top.nhan_vat

    def is_empty(self):
        return self.top is None

    def display(self):
        temp = self.top
        print("=== STACK ===")
        while temp:
            print(temp.nhan_vat)
            temp = temp.next

# ==== StackManager cho 2 luồng ====
class StackManager:
    def __init__(self):
        self.vote_stack = Stack()
        self.chat_stack = Stack()

    # ===== VOTE =====
    def push_vote(self, vote_event):
        self.vote_stack.push(vote_event)

    def pop_vote(self):
        return self.vote_stack.pop()

    def peek_vote(self):
        return self.vote_stack.peek()

    def is_empty_vote(self):
        return self.vote_stack.is_empty()

    def display_vote(self):
        print("=== VOTE STACK ===")
        self.vote_stack.display()

    # ===== CHAT =====
    def push_chat(self, chat_message):
        self.chat_stack.push(chat_message)

    def pop_chat(self):
        return self.chat_stack.pop()

    def peek_chat(self):
        return self.chat_stack.peek()

    def is_empty_chat(self):
        return self.chat_stack.is_empty()

    def display_chat(self):
        print("=== CHAT STACK ===")
        self.chat_stack.display()