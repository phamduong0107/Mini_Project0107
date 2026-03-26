# tree.py

class TreeNode:
    def __init__(self, value):
        self.value = value  # có thể là tên nhân vật + hành động
        self.children = []  # danh sách con
    
    def add_child(self, child_value):
        """Thêm node con"""
        child_node = TreeNode(child_value)
        self.children.append(child_node)
        return child_node
    
    def traverse(self):
        """Duyệt tất cả node (DFS)"""
        nodes = [self]
        result = []
        while nodes:
            current = nodes.pop()
            result.append(current.value)
            # thêm children vào stack
            nodes.extend(reversed(current.children))
        return result
    
    def print_tree(self, level=0):
        """In cây ra để debug"""
        print("  " * level + str(self.value))
        for child in self.children:
            child.print_tree(level + 1)