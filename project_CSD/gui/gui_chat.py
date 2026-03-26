# gui_chat.py
import tkinter as tk
import random

KHO_HOI_THOAI = {
    "dan_ngay": [
        "Tôi nghi ngờ số {n} là Sói!", "Đêm qua số {n} đi đâu thế?", 
        "Đừng vote tôi, tôi là dân mà!", "Tiên Tri ơi, soi số {n} chưa?", 
        "Làng ơi tập trung vote số {n} đi!", "Số {n} nãy giờ im lặng đáng nghi quá.",
        "Tôi tin số {n} là người tốt.", "Trưởng làng cho ý kiến về số {n} đi!"
    ],
    "soi_ngay": [
        "Tôi là dân, tin tôi đi!", "Số {n} đang diễn sâu quá đấy.", 
        "Vote nhầm dân là làng thua đấy nhé.", "Tôi sẽ vote theo số đông.", 
        "Đừng đổ thừa cho tôi!", "Tiên Tri giả đấy, đừng tin!",
        "Số {n} mới là Sói thật kìa.", "Tôi thề tôi phe dân làng!"
    ],
    "soi_dem": [
        "Thịt số {n} đi, nó nói nhiều quá!", "Cắn đứa ít nói nhất là số {n} ấy.", 
        "Xử số {n} đi, nghi nó là Tiên Tri.", "Tránh số {n} ra, có bảo vệ gác đấy.", 
        "Giết nhanh gọn số {n} nào.", "Đêm nay anh em mình cắn số {n} nhé?",
        "Số {n} có vẻ là Thợ Săn đấy, cẩn thận.", "Cắn số {n} để gây hoang mang cho làng!"
    ],
    "npc_tu_tao": [
        "Mọi người thấy sao về số {n}?", "Tôi thấy số {n} cứ lạ lạ kiểu gì ấy.",
        "Ai có thông tin gì về số {n} không?", "Hình như số {n} đang rung cây nhát khỉ.",
        "Tôi vừa nằm mơ thấy số {n} là Sói.", "Đừng để số {n} dắt mũi nhé làng.",
        "Số {n} ơi, giải thích đi chứ?", "Cẩn thận kẻo số {n} lừa đấy!"
    ],
    "npc_phan_hoi": [
        "Chuẩn luôn!", "Vớ vẩn thật sự!", "Bằng chứng đâu mà nói thế?", 
        "Tôi cũng thấy thế.", "Đừng đổ thừa lung tung.", "Cũng hợp lý đấy.",
        "Tôi không tin lắm.", "Để xem số {n} nói gì đã."
    ]
}

class GameChat:
    def lich_trinh_chat_npc(self):
        """Hàm duy trì luồng chat tự động của NPC """
        if self.timer_running:
            # NPC tự khởi xướng hội thoại sau 8-15 giây random
            self.npc_tu_khoi_xuong()
            self.root.after(random.randint(8000, 15000), self.lich_trinh_chat_npc)

    def npc_tu_khoi_xuong(self):
        """NPC chủ động 'bóc phốt' một người chơi khác """
        # Lấy danh sách những người còn sống (không bao gồm chính người chơi)
        lives = [t.nhan_vat for t in self.players.iter_nodes() if t.nhan_vat.is_alive and t.nhan_vat != self.my_character]
        if not lives: return

        nguoi_noi = random.choice(lives)
        phe_nguoi_noi = getattr(nguoi_noi, 'phe', 'Dân')
        target_num = random.randint(1, 8)

        # Chỉ chat nếu là Ban ngày hoặc (Ban đêm + người nói là Sói)
        if self.is_day or (not self.is_day and phe_nguoi_noi == 'Sói'):
            kho = self.dialogues["npc_tu_tao"] if self.is_day else self.dialogues["soi_dem"]
            msg = random.choice(kho).replace('{n}', str(target_num))
            pre = "[Sói] " if not self.is_day else ""
            
            self.xuat_thong_bao_chat(f"{pre}{nguoi_noi.ten}: {msg}")
            
            # Sau khi NPC 1 nói, NPC 2 sẽ phản hồi sau 2-4 giây
            self.root.after(random.randint(2000, 4000), self.npc_phan_hoi_lan_nhau, nguoi_noi)

    def npc_phan_hoi_lan_nhau(self, nguoi_vừa_nói):
        """NPC khác nhảy vào hưởng ứng hoặc phản bác """
        lives = [t.nhan_vat for t in self.players.iter_nodes() if t.nhan_vat.is_alive and t.nhan_vat != self.my_character and t.nhan_vat != nguoi_vừa_nói]
        if not lives: return

        nguoi_rep = random.choice(lives)
        phe_rep = getattr(nguoi_rep, 'phe', 'Dân')

        if self.is_day or (not self.is_day and phe_rep == 'Sói'):
            msg = random.choice(self.dialogues["npc_phan_hoi"])
            pre = "[Sói] " if not self.is_day else ""
            self.xuat_thong_bao_chat(f"{pre}{nguoi_rep.ten}: {msg}")

    def xuat_thong_bao_chat(self, msg):
        """Hiển thị tin nhắn và phân quyền người xem """
        if "[Sói]" in msg and getattr(self.my_character, 'phe', '') != "Sói":
            return 
        self.chat_text.config(state="normal")
        self.chat_text.insert(tk.END, msg + "\n")
        self.chat_text.see(tk.END) 
        self.chat_text.config(state="disabled")

    def cap_nhat_danh_sach_hoi_thoai(self):
        if not getattr(self, 'my_character', None) or not self.my_character.is_alive: 
            self.chat_combobox['values'] = ["(Đã chết)"]
            return

        p = getattr(self.my_character, 'phe', 'Dân')
        if self.is_day:
            # Ban ngày: Sói giả vờ làm dân, Dân nói chuyện dân [cite: 6]
            self.chat_combobox['values'] = self.dialogues["soi_ngay"] if p == "Sói" else self.dialogues["dan_ngay"]
        else:
            # Ban đêm: Chỉ Sói mới được chat bàn mưu 
            if p == "Sói":
                self.chat_combobox['values'] = self.dialogues["soi_dem"]
            else:
                self.chat_combobox['values'] = ["(Đang ngủ...)"]
        
        if self.chat_combobox['values']: self.chat_combobox.current(0)

    def xu_ly_gui_tin(self):
        c = self.chat_combobox.get()
        if not c or c.startswith("("): return
        
        msg = c.replace("{n}", str(random.randint(1, 8)))
        # Thêm tiền tố [Sói] nếu đang là đêm và bạn là Sói [cite: 14]
        pre = "[Sói] " if not self.is_day and getattr(self.my_character, 'phe', '') == 'Sói' else ""
        self.xuat_thong_bao_chat(f"{pre}BẠN: {msg}")
        self.root.after(1000, lambda: self.npc_tu_dong_tra_loi())
        