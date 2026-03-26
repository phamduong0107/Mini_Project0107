# gui_base.py
import tkinter as tk

class BaseGameGUI:
    def __init__(self, parent_frame, game_engine):
        # Lưu lại tham chiếu đến class WerewolfGame (để gọi hàm chat, kiểm tra sống/chết...)
        self.game = game_engine  
        
        # Dọn dẹp sạch sẽ khay chứa trước khi lắp giao diện của nhân vật mới vào
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        # Tạo một khung (Frame) màu trắng có viền để vẽ các nút bấm lên
        self.action_frame = tk.Frame(parent_frame, bg="white", relief="groove", bd=2)
        self.action_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Kích hoạt hàm vẽ giao diện (Các class con sẽ tự định nghĩa hàm này)
        self.build_role_ui()

    def build_role_ui(self):
        """
        Hàm rỗng. Sẽ được các class con (như GuiBaoVe, GuiSoi...) ghi đè 
        để tự vẽ Nút bấm và Label riêng của phe mình.
        """
        pass

    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        """
        Hàm rỗng. Sẽ được hệ thống gọi mỗi khi hàm toggle_time() đổi từ Ngày sang Đêm 
        (để bật/tắt nút bấm cho phù hợp).
        """
        pass