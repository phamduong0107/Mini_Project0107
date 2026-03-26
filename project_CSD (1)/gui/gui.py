import tkinter as tk
from tkinter import ttk, messagebox
from game.setup_game import setup_game
from game.logic_game import GameLogic
from mechanics.graph import Graph
# Import từ cùng package gui
from .gui_chat import GameChat, KHO_HOI_THOAI
from .gui_roles import get_role_gui_class
from .gui_base import BaseGameGUI
from PIL import Image, ImageTk
import os
import pygame

pygame.mixer.init()

class WerewolfGame(GameLogic, GameChat):
    def __init__(self, root):
        GameLogic.__init__(self, root)
        self.root = root
        self.root.title("Ma Sói Pro")
        self.root.geometry("950x750")
        self.vote_graph = Graph()     
        self.danh_sach_vote = [] 

        self.game_frame = None
        self.chat_text = None
        self.grid_frame = None
        self.dialogues = KHO_HOI_THOAI

        
        self.show_main_menu()
    def resize_bg(self, event):
        resized = self.original_img.resize((event.width, event.height))
        self.menu_img = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.menu_img)
    def resize_game_bg(self, event):
        resized = self.original_game_img.resize((event.width, event.height))
        self.vao_game_img = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.vao_game_img)
    def aresize_game_bg(self, event):
        resized = self.original_game_img.resize((event.width, event.height))
        self.game_bg_img = ImageTk.PhotoImage(resized)
        self.bg_label.config(image=self.game_bg_img)
    def show_main_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")

        # ===== Phát nhạc sảnh =====
        try:
            pygame.mixer.music.load("source/nhacsanh.mp3")  # file nhạc sảnh
            pygame.mixer.music.play(-1)  # lặp vô hạn
            self.lobby_music_playing = True
        except Exception as e:
            print("Không thể phát nhạc sảnh:", e)
            self.lobby_music_playing = False
        
        # ===== Load ảnh menu.jpg =====
        import os
        from PIL import Image, ImageTk

        base_dir = os.path.dirname(__file__)
        project_dir = os.path.dirname(base_dir)
        path = os.path.join(project_dir, "source", "menu.jpg")

        self.original_img = Image.open(path)
        self.bg_label = tk.Label(frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        frame.bind("<Configure>", self.resize_bg)

        # ===== Các nút menu hiển thị trên ảnh =====
        content = tk.Frame(frame, bg="#2C3E50")
        content.pack(expand=True)

        tk.Label(content, text="🐺 Làng Tày 🐺", font=("Arial", 32, "bold"),
                fg="#ECF0F1", bg="#2C3E50").pack(pady=20)

        tk.Label(content, text="CHỌN CHẾ ĐỘ CHƠI", font=("Arial", 16),
                fg="#BDC3C7", bg="#2C3E50").pack(pady=10)

        for num in [8, 15, 20]:
            tk.Button(content, text=f"▶ PLAY ({num} Người)", font=("Arial", 16, "bold"),
                    width=20, height=2,
                    bg="#E74C3C", fg="white",
                    command=lambda n=num: self.start_game(n)).pack(pady=10)

        tk.Button(content, text="❓ Hướng dẫn", font=("Arial", 12),
                bg="#34495E", fg="white",
                command=lambda: messagebox.showinfo("Hướng dẫn", "...")).pack(pady=20)

        # ===== Nút bật/tắt nhạc sảnh =====
        def toggle_lobby_music():
            if self.lobby_music_playing:
                pygame.mixer.music.stop()
                self.lobby_music_playing = False
                btn_music.config(text="Bật nhạc sảnh")
            else:
                pygame.mixer.music.play(-1)
                self.lobby_music_playing = True
                btn_music.config(text="Tắt nhạc sảnh")

        btn_music = tk.Button(content, text="Tắt nhạc sảnh",
                            font=("Arial", 10), width=12, height=1,
                            bg="#34495E", fg="white",
                            command=toggle_lobby_music)
        btn_music.pack(pady=5)

        self.game_frame = frame

    def start_game(self, so_luong):
        self.players = setup_game(so_luong)  
        self.is_day = True 
        self.time_left = 60
        self.timer_running = False
        self.timer_id = None
        
        self.ngay_thu = 1
        self.truong_lang = None
        self.soi_gian_du = False  
        self.has_shown_death_dialog = False
        self.night_actions = {"soi_target": [], "bao_ve_target": None, "phu_thuy_cuu": False, "phu_thuy_doc_target": None, "tho_san_target": None}
        self.danh_sach_vote = [] 
        self.show_role_reveal_screen()

    def show_role_reveal_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both")



        import os
        from PIL import Image, ImageTk

        base_dir = os.path.dirname(__file__)
        project_dir = os.path.dirname(base_dir)
        path = os.path.join(project_dir, "source", "anhvaogame.jpg")
        # Lưu ảnh gốc
        self.original_game_img = Image.open(path)

        # Label chứa ảnh nền
        self.bg_label = tk.Label(frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Gắn sự kiện resize để ảnh co giãn theo cửa sổ
        frame.bind("<Configure>", self.resize_game_bg)


    



        # Các nút hiển thị trên ảnh
        tk.Label(frame, text="CHUẨN BỊ VÀO LÀNG", font=("Arial", 24, "bold"), fg="white", bg="#2C3E50").pack(pady=20)
        self.btn_boc_bai = tk.Button(frame, text="Nhận Thân Phận", font=("Arial", 16, "bold"),
                                    bg="#F1C40F", fg="black", command=self.bat_dau_dem_nguoc)
        self.btn_boc_bai.pack(pady=20)

        self.lbl_role_result = tk.Label(frame, text="", font=("Arial", 20, "bold"), fg="#1ABC9C", bg="#2C3E50")
        self.lbl_role_result.pack(pady=10)

        self.btn_vao_lang = tk.Button(frame, text="Vào Game", font=("Arial", 16), bg="#2ECC71", fg="white",
                                    state="disabled", command=self.vao_game)
        self.btn_vao_lang.pack(pady=20)

        self.game_frame = frame

    def vao_game(self):
        self.show_game_screen()
        self.timer_running = True
        self.update_timer()
        self.lich_trinh_chat_npc()

    def show_game_screen(self):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)
        try:
            pygame.mixer.music.load("source/nhacnen.mp3")  # đường dẫn tới file nhạc
            pygame.mixer.music.play(-1)  # -1 nghĩa là lặp vô hạn
        except Exception as e:
            print("Không thể phát nhạc:", e)
        # Nút bật/tắt nhạc duy nhất
    # Nút bật/tắt nhạc duy nhất
        def toggle_music():
            if self.music_playing:
                pygame.mixer.music.stop()
                self.music_playing = False
                btn_music.config(text="Bật nhạc")
            else:
                pygame.mixer.music.play(-1)
                self.music_playing = True
                btn_music.config(text="Tắt nhạc")

        # Khung chứa nút (nhỏ gọn như nút hướng dẫn)
        music_frame = tk.Frame(self.chat_frame)
        music_frame.pack(pady=5)

        # Nút Tắt nhạc (nhỏ gọn)
        btn_stop = tk.Button(music_frame, text="Tắt nhạc",
                            font=("Arial", 10), width=12, height=1,
                            command=lambda: pygame.mixer.music.stop())
        btn_stop.pack(side=tk.LEFT, padx=5)

        # Nút Bật nhạc (nhỏ gọn)
        btn_play = tk.Button(music_frame, text="Bật nhạc",
                            font=("Arial", 10), width=12, height=1,
                            command=lambda: pygame.mixer.music.play(-1))
        btn_play.pack(side=tk.LEFT, padx=5)


        import os
        from PIL import Image, ImageTk

        base_dir = os.path.dirname(__file__)
        project_dir = os.path.dirname(base_dir)

        # Chọn ảnh theo trạng thái ngày/đêm
        if self.is_day:
            path = os.path.join(project_dir, "source", "backgroundvotesang.png")
        else:
            path = os.path.join(project_dir, "source", "buoitoi.png")

        # Lưu ảnh gốc
        self.original_game_img = Image.open(path)

        # Label chứa ảnh nền
        self.bg_label = tk.Label(frame)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Gắn sự kiện resize để ảnh co giãn theo cửa sổ
        frame.bind("<Configure>", self.resize_game_bg)

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
    # Xóa các widget cũ trong lưới
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        temp = self.players.head
        row, col = 0, 0
        while temp:
            nv = temp.nhan_vat

            # Màu nền/ chữ theo trạng thái
            if not nv.is_alive:
                bg_color, fg_color = "#7F8C8D", "white"
            elif nv == self.my_character:
                bg_color, fg_color = "#2ECC71", "white"
            else:
                bg_color, fg_color = ("white", "black") if self.is_day else ("#34495E", "white")

            # Nội dung text hiển thị
            txt = nv.ten
            if nv == self.truong_lang:
                txt += " 👑"
            if not nv.is_alive:
                txt += "\n(Đã chết)"

            so_vote = self.danh_sach_vote.count(nv.ten.lower())
            if so_vote > 0 and nv.is_alive:
                txt += f"\n🗳️ {so_vote} phiếu"

            # Ánh xạ class -> file ảnh
            ROLE_ICON_MAP = {
                "PhuThuy": "witch.png",
                "TienTri": "seer.png",
                "Dan": "villager.png",
                "Soi": "wolf.png",
                "BaoVe": "protector.png"
            }

            role_class_name = nv.__class__.__name__
            icon_file = ROLE_ICON_MAP.get(role_class_name, None)

            # Chỉ hiện icon nếu là nhân vật của mình hoặc nv đã chết
            show_icon = (nv == self.my_character) or (not nv.is_alive)

            if show_icon and icon_file:
                base_dir = os.path.dirname(__file__)
                project_dir = os.path.dirname(base_dir)
                role_icon_path = os.path.join(project_dir, "source", icon_file)
                if os.path.exists(role_icon_path):
                    img = Image.open(role_icon_path).resize((48, 48))  # icon to hơn
                    nv.role_icon = ImageTk.PhotoImage(img)
                else:
                    nv.role_icon = None
            else:
                nv.role_icon = None

            # Tạo Label với icon hoặc chỉ text
            if nv.role_icon:
                lbl = tk.Label(self.grid_frame, text=txt, image=nv.role_icon,
                            compound="top", bg=bg_color, fg=fg_color,
                            font=("Arial", 10, "bold"), width=90, height=90,
                            relief="raised", bd=2)
            else:
                lbl = tk.Label(self.grid_frame, text=txt,
                            bg=bg_color, fg=fg_color,
                            font=("Arial", 10, "bold"), width=12, height=4,
                            relief="raised", bd=2)

            lbl.grid(row=row, column=col, padx=5, pady=5)

            # Chia lưới 2x4
            col += 1
            if col > 3:
                col = 0
                row += 1
            temp = temp.next

    def clear_frame(self):
        if self.game_frame: self.game_frame.destroy()

