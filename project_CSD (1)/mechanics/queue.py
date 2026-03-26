# queue.py

from player.node import Node

class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self, nhan_vat):
        """Thêm nhân vật vào cuối queue"""
        new_node = Node(nhan_vat)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            new_node.prev = self.rear
            self.rear = new_node
    
    def dequeue(self):
        """Lấy nhân vật ở đầu queue ra"""
        if self.is_empty():
            return None
        removed_node = self.front
        self.front = self.front.next
        if self.front:
            self.front.prev = None
        else:
            self.rear = None
        removed_node.next = None
        return removed_node.nhan_vat
    
    def peek(self):
        """Xem nhân vật ở đầu queue mà không xóa"""
        if self.is_empty():
            return None
        return self.front.nhan_vat