# player/LinkedList.py
from player.node import Node

class LinkedList:
    def __init__(self):
        self.head = None

    # Thêm 1 NhanVat vào cuối LinkedList
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        temp = self.head
        while temp.next:
            temp = temp.next
        temp.next = new_node

    # Xóa những người chết
    def remove_dead(self):
        while self.head and not self.head.nhan_vat.is_alive:
            self.head = self.head.next
        temp = self.head
        while temp and temp.next:
            if not temp.next.nhan_vat.is_alive:
                temp.next = temp.next.next
            else:
                temp = temp.next

    # Duyệt LinkedList, trả về iterator
    def iter_nodes(self):
        temp = self.head
        while temp:
            yield temp
            temp = temp.next

    # Hiển thị danh sách player (debug)
    def display(self):
        temp = self.head
        print("=== DANH SÁCH NGƯỜI CHƠI ===")
        while temp:
            print(f"{temp.nhan_vat.ten} | Role: {temp.nhan_vat.__class__.__name__} | {'Sống' if temp.nhan_vat.is_alive else 'Chết'}")
            temp = temp.next

    def traverse(self):
        """Duyệt tất cả node, yield nhan_vat"""
        current = self.head
        while current:
            yield current.nhan_vat
            current = current.next