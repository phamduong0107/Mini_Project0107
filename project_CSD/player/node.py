
class Node:
    def __init__(self, nhan_vat):
        self.nhan_vat = nhan_vat  # object NhanVat hoặc tên nhân vật
        self.next = None          # trỏ đến Node kế tiếp
        self.prev = None          # trỏ đến Node trước (nếu dùng double linked list)
        
    def __str__(self):
        return f"Node({self.nhan_vat.ten})" if hasattr(self.nhan_vat, 'ten') else f"Node({self.nhan_vat})"