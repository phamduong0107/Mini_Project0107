# gui.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import ttk, messagebox
from game.setup_game import setup_game 

from gui_chat import GameChat, KHO_HOI_THOAI
from game.logic_game import GameLogic

# Gọi factory bốc linh kiện giao diện
from gui_roles import get_role_gui_class

class WerewolfGame(GameLogic, GameChat):
    def __init__(self, root):
        self.root = root
        self.root.title("Ma Sói Pro")
        self.root.geometry("950x750")

        self.game_frame = None
        self.chat_text = None
        self.grid_frame = None
        self.dialogues = KHO_HOI_THOAI
        
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_frame()
        self.root.config(bg="#2C3E50")
        frame = tk.Frame(self.root, bg="#2C3E50")
        frame.pack(expand=True)

        tk.Label(frame, text="🐺 TRÒ CHƠI MA SÓI 🐺", font=("Arial", 32, "bold"), fg="#ECF0F1", bg="#2C3E50").pack(pady=30)
        tk.Label(frame, text="CHỌN CHẾ ĐỘ CHƠI", font=("Arial", 16), fg="#BDC3C7", bg="#2C3E50").pack(pady=10)

        for num in [8, 15, 20]:
            tk.Button(frame, text=f"▶ PLAY ({num} Người)", font=("Arial", 16, "bold"), width=20, height=2, 
                      bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white",
                      command=lambda n=num: self.start_game(n)).pack(pady=10)

        tk.Button(frame, text="❓ Hướng dẫn", font=("Arial", 12), bg="#34495E", fg="white", 
                  command=lambda: messagebox.showinfo("Hướng dẫn", "Luật chơi:\n- Sáng: Vote treo cổ, bầu trưởng làng.\n- Đêm: Sói cắn, Phù thủy ném bình...\n- Có thể nhập SỐ (VD: 3) thay vì tên đầy đủ để thao tác nhanh.")).pack(pady=20)
        self.game_frame = frame

    def start_game(self, so_luong):
        self.players = setup_game(so_luong)  
        self.is_day = True 
        self.time_left = 60
        self.timer_running = False
        self.chi_tiet_vote = []
        
        self.ngay_thu = 1
        self.truong_lang = None
        self.soi_gian_du = False  
        self.has_shown_death_dialog = False
        self.night_actions = {"soi_target": [], "bao_ve_target": None, "phu_thuy_cuu": False, "phu_thuy_doc_target": None, "tho_san_target": None}
        self.danh_sach_vote = [] 
        self.show_role_reveal_screen()

    def show_role_reveal_screen(self):
        self.clear_frame()
        self.root.config(bg="#2C3E50")
        frame = tk.Frame(self.root, bg="#2C3E50")
        frame.pack(expand=True)
        
        tk.Label(frame, text="CHUẨN BỊ VÀO LÀNG", font=("Arial", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
        self.btn_boc_bai = tk.Button(frame, text="Nhận Thân Phận", font=("Arial", 16, "bold"), bg="#F1C40F", fg="black", command=self.bat_dau_dem_nguoc)
        self.btn_boc_bai.pack(pady=20)
        
        self.lbl_role_result = tk.Label(frame, text="", font=("Arial", 20, "bold"), fg="#1ABC9C", bg="#2C3E50")
        self.lbl_role_result.pack(pady=10)
        
        self.btn_vao_lang = tk.Button(frame, text="Vào Game", font=("Arial", 16), bg="#2ECC71", fg="white", state="disabled", command=self.vao_game)
        self.btn_vao_lang.pack(pady=20)
        self.game_frame = frame

    def show_game_screen(self):
        self.clear_frame()
        self.root.config(bg="#ECF0F1")
        frame = tk.Frame(self.root, bg="#ECF0F1")
        frame.pack(fill="both", expand=True)
        self.main_game_frame = frame 

        self.chat_frame = tk.Frame(frame, width=450, bg="white", relief="groove", bd=2)
        self.chat_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        top_info = tk.Frame(self.chat_frame, bg="white")
        top_info.pack(pady=5, fill=tk.X)
        self.time_lbl = tk.Label(top_info, text="☀️ BAN NGÀY", font=("Arial", 14, "bold"), fg="#2980B9", bg="white")
        self.time_lbl.pack(side=tk.LEFT, padx=10)
        self.lbl_countdown = tk.Label(top_info, text="Thời gian: 02:30", font=("Arial", 14, "bold"), fg="#E74C3C", bg="white")
        self.lbl_countdown.pack(side=tk.RIGHT, padx=10)
        
        chat_container = tk.Frame(self.chat_frame)
        chat_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(chat_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chat_text = tk.Text(chat_container, state="disabled", wrap=tk.WORD, yscrollcommand=scrollbar.set, font=("Arial", 11))
        self.chat_text.pack(side=tk.LEFT, fill="both", expand=True)
        scrollbar.config(command=self.chat_text.yview)

        inp = tk.Frame(self.chat_frame, bg="white")
        inp.pack(fill=tk.X, padx=5, pady=5)
        self.chat_combobox = ttk.Combobox(inp, font=("Arial", 12), state="readonly")
        self.chat_combobox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        tk.Button(inp, text="Gửi Chat", bg="#3498DB", fg="white", font=("Arial", 10, "bold"), command=self.xu_ly_gui_tin).pack(side=tk.RIGHT)

        btns = tk.Frame(self.chat_frame, bg="white")
        btns.pack(fill=tk.X, pady=5)
        self.btn_vote_truong_lang = tk.Button(btns, text="👑 Bầu Trưởng Làng", font=("Arial", 10, "bold"), bg="#9B59B6", fg="white", command=lambda: self.hien_thi_khung_vote("BẦU TRƯỞNG LÀNG"))
        self.btn_vote_truong_lang.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
        self.btn_vote = tk.Button(btns, text="🗳️ Vote Treo Cổ", state="disabled", font=("Arial", 10, "bold"), bg="#E67E22", fg="white", command=lambda: self.hien_thi_khung_vote("VOTE TREO CỔ"))
        self.btn_vote.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        self.cap_nhat_danh_sach_hoi_thoai()

        # ================== KHUNG BÊN PHẢI ==================
        self.right_frame = tk.Frame(frame, bg="#ECF0F1")
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        tk.Label(self.right_frame, text=f"BẠN: {self.my_character.ten} ({self.my_character.__class__.__name__})", font=("Arial", 14, "bold"), fg="#27AE60", bg="#ECF0F1").pack(pady=5)
        
        self.grid_frame = tk.Frame(self.right_frame, bg="#ECF0F1")
        self.grid_frame.pack(fill="both", expand=True)
        self.cap_nhat_giao_dien_luoi()
        
        # Lắp Bảng điều khiển riêng của từng Nhân Vật vào dưới Lưới
        self.role_ui_container = tk.Frame(self.right_frame, bg="#ECF0F1")
        self.role_ui_container.pack(fill=tk.BOTH, expand=True, pady=10)
        
        RoleClass = get_role_gui_class(self.my_character.__class__.__name__)
        self.role_gui = RoleClass(self.role_ui_container, self)
        
        self.game_frame = frame
        
        if not self.truong_lang:
            self.xuat_thong_bao_chat("--- TRÒ CHƠI BẮT ĐẦU. NGÀY 1: HÃY BẦU TRƯỞNG LÀNG ---")
        else:
            self.btn_vote_truong_lang.config(state="disabled")

    def cap_nhat_giao_dien_luoi(self):
        for widget in self.grid_frame.winfo_children(): widget.destroy()
            
        temp = self.players.head
        row, col = 0, 0
        while temp:
            nv = temp.nhan_vat
            if not nv.is_alive: bg_color, fg_color = "#7F8C8D", "white" 
            elif nv == self.my_character: bg_color, fg_color = "#2ECC71", "white" 
            else: bg_color, fg_color = ("white", "black") if self.is_day else ("#34495E", "white") 
                
            txt = nv.ten
            if nv == self.truong_lang: txt += " 👑"
            if not nv.is_alive: txt += "\n(Đã chết)"
            
            so_vote = self.danh_sach_vote.count(nv.ten.lower())
            if so_vote > 0 and nv.is_alive: txt += f"\n🗳️ {so_vote} phiếu"
                
            lbl = tk.Label(self.grid_frame, text=txt, bg=bg_color, fg=fg_color, font=("Arial", 10, "bold"), width=12, height=4, relief="raised", bd=2)
            lbl.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 3: 
                col = 0; row += 1
            temp = temp.next

    def clear_frame(self):
        if self.game_frame: self.game_frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = WerewolfGame(root)
    root.mainloop()