# hoithoai_game.py
import tkinter as tk
import random

KHO_HOI_THOAI = {
    "dan_ngay": ["Tôi nghi ngờ số {n} là Sói!", "Đêm qua số {n} đi đâu?", "Đừng vote tôi!", "Tiên Tri soi số {n} chưa?", "Làng ơi tập trung vote số {n} đi!"],
    "soi_ngay": ["Tôi là dân, tin tôi đi!", "Số {n} diễn sâu quá.", "Vote nhầm dân là thua đấy.", "Tôi theo số đông nhé.", "Đừng cãi nhau nữa."],
    "soi_dem": ["Thịt số {n} đi!", "Cắn đứa ít nói nhất.", "Xử Tiên Tri đi!", "Tránh số {n} ra, có bảo vệ đấy.", "Giết nhanh gọn nào."],
    "npc_chu_dong": ["Số {n} im lặng nãy giờ, anh em thấy sao?", "Hôm nay vote số {n} nhé?", "Làng nguy rồi!", "Trưởng làng cho ý kiến đi."],
    "npc_phan_hoi": ["Chuẩn luôn!", "Vớ vẩn, ông mới là Sói.", "Bằng chứng đâu?", "Tôi sẽ vote theo.", "Đừng đổ thừa!"]
}

class GameChat:
    def cap_nhat_danh_sach_hoi_thoai(self):
        if not getattr(self, 'my_character', None) or not self.my_character.is_alive: 
            self.chat_combobox['values'] = ["(Đã chết)"]
        else:
            p = getattr(self.my_character, 'phe', '')
            if self.is_day: 
                self.chat_combobox['values'] = self.dialogues["soi_ngay"] if p == "Sói" else self.dialogues["dan_ngay"]
            else: 
                self.chat_combobox['values'] = self.dialogues["soi_dem"] if p == "Sói" else ["(Đang ngủ...)"]
        if self.chat_combobox['values']: self.chat_combobox.current(0)

    def xu_ly_gui_tin(self):
        c = self.chat_combobox.get()
        if not c or c.startswith("("): return
        msg = c.replace("{n}", str(random.randint(1, 8)))
        pre = "[Sói] " if not self.is_day else ""
        self.xuat_thong_bao_chat(f"{pre}BẠN: {msg}")
        self.root.after(1500, lambda: self.npc_tu_dong_tra_loi(self.my_character))

    def npc_tu_dong_tra_loi(self, nguoi_boc_phot=None):
        lives = [t.nhan_vat for t in self.players.iter_nodes() if t.nhan_vat.is_alive and t.nhan_vat != self.my_character]
        if lives:
            n = random.choice(lives)
            pre = "[Sói] " if not self.is_day and getattr(n, 'phe', '') == 'Sói' else ""
            if self.is_day or getattr(n, 'phe', '') == 'Sói':
                self.xuat_thong_bao_chat(f"{pre}{n.ten}: {random.choice(self.dialogues['npc_phan_hoi'])}")

    def lich_trinh_chat_npc(self):
        if self.timer_running:
            if self.is_day:                                          # <--- THÊM DÒNG NÀY
                self.npc_tu_tao_hoi_thoai()
            self.root.after(random.randint(8000, 15000), self.lich_trinh_chat_npc)

    def npc_tu_tao_hoi_thoai(self):
        lives = [t.nhan_vat for t in self.players.iter_nodes() if t.nhan_vat.is_alive and t.nhan_vat != self.my_character]
        if lives:
            n = random.choice(lives)
            pre = "[Sói] " if not self.is_day and getattr(n, 'phe', '') == 'Sói' else ""
            if self.is_day or getattr(n, 'phe', '') == 'Sói':
                kho = self.dialogues["npc_chu_dong"] + self.dialogues["dan_ngay"] if self.is_day else self.dialogues["soi_dem"]
                msg = random.choice(kho).replace('{n}', str(random.randint(1, 8)))
                self.xuat_thong_bao_chat(f"{pre}{n.ten}: {msg}")

    def xuat_thong_bao_chat(self, msg):
        self.chat_text.config(state="normal")
        self.chat_text.insert(tk.END, msg + "\n")
        self.chat_text.see(tk.END) 
        self.chat_text.config(state="disabled")