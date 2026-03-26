class Graph:
    def __init__(self):
        self.adj_list = {}  # {player_name: [connected_players]}

    # Thêm 1 node/player
    def add_node(self, player_name):
        if player_name not in self.adj_list:
            self.adj_list[player_name] = []

    # Thêm edge (quan hệ 2 chiều)
    def add_edge(self, player1, player2):
        if player1 not in self.adj_list:
            self.add_node(player1)
        if player2 not in self.adj_list:
            self.add_node(player2)
        self.adj_list[player1].append(player2)
        self.adj_list[player2].append(player1)

    # Lấy danh sách láng giềng (connected players)
    def neighbors(self, player_name):
        return self.adj_list.get(player_name, [])

    # Hiển thị graph (debug)
    def display(self):
        print("=== GRAPH PLAYER RELATION ===")
        for player, neighbors in self.adj_list.items():
            print(f"{player}: {', '.join(neighbors) if neighbors else 'Không có liên kết'}")