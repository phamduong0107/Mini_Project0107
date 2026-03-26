# gui_roles.py
import tkinter as tk
from tkinter import simpledialog, messagebox

class BaseGameGUI:
    def __init__(self, parent_frame, game_engine):
        # Lưu tham chiếu đến class WerewolfGame để lấy data và gọi hàm chat
        self.game = game_engine  
        
        # Dọn dẹp khay chứa trước khi lắp giao diện của nhân vật mới vào
        for widget in parent_frame.winfo_children():
            widget.destroy()
            
        self.action_frame = tk.Frame(parent_frame, bg="white", relief="groove", bd=2)
        self.action_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.build_role_ui()

    def build_role_ui(self):
        """Sẽ được class con ghi đè để vẽ nút bấm riêng"""
        pass

    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        """Tự động bật/tắt nút khi chuyển Ngày/Đêm"""
        pass

# ================= CLASS DÂN LÀNG =================
class GuiDan(BaseGameGUI):
    def build_role_ui(self):
        self.lbl = tk.Label(self.action_frame, text="🌾 BẠN LÀ DÂN LÀNG 🌾\nKhông có kỹ năng đêm. Hãy thảo luận tìm Sói!", 
                            font=("Arial", 11, "bold"), fg="green", bg="white")
        self.lbl.pack(pady=15)
        
    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        if not self.game.my_character.is_alive:
            self.lbl.config(text="👻 BẠN ĐÃ CHẾT 👻", fg="gray"); return
        if is_day: 
            self.lbl.config(text="☀️ TRỜI SÁNG ☀️\nHãy tích cực thảo luận!", fg="green")
        else: 
            self.lbl.config(text="🌙 TRỜI TỐI 🌙\nTrùm chăn đi ngủ thôi...", fg="gray")

# ================= CLASS MA SÓI =================
class GuiSoi(BaseGameGUI):
    def build_role_ui(self):
        role_name = self.game.my_character.__class__.__name__
        self.is_soi_con = (role_name == "SoiCon") #
        
        txt = "🐺 BẠN LÀ SÓI CON 🐺\n(Chỉ bàn mưu, không được chọn cắn)" if self.is_soi_con else "🐺 BẠN LÀ SÓI 🐺\nBan đêm hãy đi săn!"
        self.lbl = tk.Label(self.action_frame, text=txt, font=("Arial", 11, "bold"), fg="red", bg="white")
        self.lbl.pack(pady=5)
        
        self.btn = tk.Button(self.action_frame, text="🔪 Chọn con mồi", bg="red", fg="white", state="disabled", command=self.hanh_dong)
        if not self.is_soi_con: self.btn.pack(pady=5)
        
    def hanh_dong(self):
        nhap = simpledialog.askstring("Sói đi săn", "Nhập SỐ kẻ bạn muốn cắn (VD: 3):")
        muc_tieu = self.game.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None #
        
        if muc_tieu:
            limit = 2 if getattr(self.game, 'soi_gian_du', False) else 1 # Luật Sói con chết
            if len(self.game.night_actions["soi_target"]) < limit:
                self.game.night_actions["soi_target"].append(muc_tieu)
                self.game.xuat_thong_bao_chat(f"🔪 Bầy sói đã cắn: {muc_tieu.ten}") #
            if len(self.game.night_actions["soi_target"]) >= limit: 
                self.btn.config(state="disabled")
        else:
            if nhap: messagebox.showerror("Lỗi", "Sai số hoặc người đã chết!")
            
    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        if not self.game.my_character.is_alive:
            self.lbl.config(text="👻 BẠN ĐÃ CHẾT 👻", fg="gray"); self.btn.config(state="disabled"); return
        if is_day:
            self.lbl.config(text="☀️ TRỜI SÁNG ☀️\nGiả vờ làm dân đi!", fg="green")
            self.btn.config(state="disabled")
        else:
            self.lbl.config(text="🌙 TRỜI TỐI 🌙\nĐến giờ đi săn!", fg="red")
            if not self.is_soi_con: self.btn.config(state="normal")

# ================= CLASS PHÙ THỦY =================
class GuiPhuThuy(BaseGameGUI):
    def build_role_ui(self):
        self.binh_cuu = 1; self.binh_doc = 1 #
        self.lbl = tk.Label(self.action_frame, text="🧪 BẠN LÀ PHÙ THỦY 🧪\nBạn có 1 bình cứu và 1 bình độc.", 
                            font=("Arial", 11, "bold"), fg="#FF1493", bg="white")
        self.lbl.pack(pady=5)
        
        btn_frame = tk.Frame(self.action_frame, bg="white")
        btn_frame.pack(pady=5)
        
        self.btn_cuu = tk.Button(btn_frame, text="❤️ Dùng Bình Cứu", bg="lightgreen", state="disabled", command=self.dung_binh_cuu)
        self.btn_cuu.pack(side=tk.LEFT, padx=10)
        
        self.btn_doc = tk.Button(btn_frame, text="☠️ Dùng Bình Độc", bg="black", fg="white", state="disabled", command=self.dung_binh_doc)
        self.btn_doc.pack(side=tk.LEFT, padx=10)

    def dung_binh_cuu(self):
        nhap = simpledialog.askstring("Bình Cứu", "Nhập SỐ người bạn muốn CỨU (VD: 1):")
        muc_tieu = self.game.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        if muc_tieu:
            self.game.night_actions["bao_ve_target"] = muc_tieu # Mượn cơ chế bảo vệ để miễn tử
            self.binh_cuu -= 1
            self.game.xuat_thong_bao_chat(f"💊 Phù thủy đã rải thuốc cứu cho: {muc_tieu.ten}")
            self.btn_cuu.config(state="disabled", text="❤️ Hết cứu")

    def dung_binh_doc(self):
        nhap = simpledialog.askstring("Bình Độc", "Nhập SỐ người bạn muốn NÉM ĐỘC:")
        muc_tieu = self.game.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        if muc_tieu:
            self.game.night_actions["phu_thuy_doc_target"] = muc_tieu #
            self.binh_doc -= 1
            self.game.xuat_thong_bao_chat(f"🧪 Phù thủy đã ném bình độc vào: {muc_tieu.ten}")
            self.btn_doc.config(state="disabled", text="☠️ Hết độc")

    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        if not self.game.my_character.is_alive:
            self.lbl.config(text="👻 BẠN ĐÃ CHẾT 👻", fg="gray")
            self.btn_cuu.config(state="disabled"); self.btn_doc.config(state="disabled"); return
        if is_day:
            self.lbl.config(text="☀️ TRỜI SÁNG ☀️", fg="green")
            self.btn_cuu.config(state="disabled"); self.btn_doc.config(state="disabled")
        else:
            self.lbl.config(text="🌙 TRỜI TỐI 🌙", fg="#FF1493")
            if self.binh_cuu > 0: self.btn_cuu.config(state="normal")
            if self.binh_doc > 0: self.btn_doc.config(state="normal")

# ================= CLASS TIÊN TRI =================
class GuiTienTri(BaseGameGUI):
    def build_role_ui(self):
        self.lbl = tk.Label(self.action_frame, text="👁️ BẠN LÀ TIÊN TRI 👁️\nMỗi đêm chọn một người để soi phe.", 
                            font=("Arial", 11, "bold"), fg="purple", bg="white")
        self.lbl.pack(pady=5)
        self.btn = tk.Button(self.action_frame, text="🔮 Soi người chơi", bg="purple", fg="white", state="disabled", command=self.hanh_dong)
        self.btn.pack(pady=5)

    def hanh_dong(self):
        nhap = simpledialog.askstring("Tiên tri", "Nhập SỐ người bạn muốn soi phe:")
        muc_tieu = self.game.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        if muc_tieu:
            phe = getattr(muc_tieu, 'phe', 'Dân') #
            messagebox.showinfo("Kết quả Tiên Tri", f"Quả cầu pha lê cho thấy:\n{muc_tieu.ten} thuộc phe: {phe}")
            self.game.xuat_thong_bao_chat(f"🔮 Tiên tri đã soi phe của một người.")
            self.btn.config(state="disabled") 

    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        if not self.game.my_character.is_alive:
            self.lbl.config(text="👻 BẠN ĐÃ CHẾT 👻", fg="gray"); self.btn.config(state="disabled"); return
        if is_day:
            self.lbl.config(text="☀️ TRỜI SÁNG ☀️", fg="green"); self.btn.config(state="disabled")
        else:
            self.lbl.config(text="🌙 TRỜI TỐI 🌙\nChọn người để soi!", fg="purple"); self.btn.config(state="normal")

# ================= CLASS BẢO VỆ =================
class GuiBaoVe(BaseGameGUI):
    def build_role_ui(self):
        self.lbl = tk.Label(self.action_frame, text="🛡️ BẠN LÀ BẢO VỆ 🛡️\nBảo vệ một người đêm nay (trừ đêm trước).", 
                            font=("Arial", 11, "bold"), fg="blue", bg="white")
        self.lbl.pack(pady=5)
        self.btn = tk.Button(self.action_frame, text="🛡️ Chọn người bảo vệ", bg="blue", fg="white", state="disabled", command=self.hanh_dong)
        self.btn.pack(pady=5)

    def hanh_dong(self):
        nhap = simpledialog.askstring("Bảo Vệ", "Nhập SỐ người muốn bảo vệ:")
        muc_tieu = self.game.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        if muc_tieu:
            cu = getattr(self.game.my_character, 'da_bao_ve_dem_truoc', None) # Luật bảo vệ
            if cu == muc_tieu.ten:
                messagebox.showwarning("Luật", f"Bạn đã bảo vệ {muc_tieu.ten} đêm qua rồi!"); return
            
            self.game.night_actions["bao_ve_target"] = muc_tieu
            self.game.my_character.da_bao_ve_dem_truoc = muc_tieu.ten
            self.game.xuat_thong_bao_chat(f"🛡️ Bảo vệ đang canh gác tại nhà: {muc_tieu.ten}")
            self.btn.config(state="disabled") 

    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        if not self.game.my_character.is_alive:
            self.lbl.config(text="👻 BẠN ĐÃ CHẾT 👻", fg="gray"); self.btn.config(state="disabled"); return
        if is_day:
            self.lbl.config(text="☀️ TRỜI SÁNG ☀️", fg="green"); self.btn.config(state="disabled")
        else:
            self.lbl.config(text="🌙 TRỜI TỐI 🌙", fg="blue"); self.btn.config(state="normal")

# ================= CLASS THỢ SĂN =================
class GuiThoSan(BaseGameGUI):
    def build_role_ui(self):
        self.lbl = tk.Label(self.action_frame, text="🔫 BẠN LÀ THỢ SĂN 🔫\nBắn nhầm Dân/Role, cả hai sẽ chết!", 
                            font=("Arial", 11, "bold"), fg="#8B4513", bg="white")
        self.lbl.pack(pady=5)
        self.btn = tk.Button(self.action_frame, text="🔫 Bắn mục tiêu", bg="#8B4513", fg="white", state="disabled", command=self.hanh_dong)
        self.btn.pack(pady=5)

    def hanh_dong(self):
        nhap = simpledialog.askstring("Thợ Săn", "Nhập SỐ người bạn muốn bắn đêm nay:")
        muc_tieu = self.game.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        if muc_tieu:
            self.game.night_actions["tho_san_target"] = muc_tieu # Luật súng thợ săn
            self.game.xuat_thong_bao_chat(f"🔫 Thợ săn đã nhắm súng vào: {muc_tieu.ten}")
            self.btn.config(state="disabled") 

    def cap_nhat_ui_theo_thoi_gian(self, is_day):
        if not self.game.my_character.is_alive:
            self.lbl.config(text="👻 BẠN ĐÃ CHẾT 👻", fg="gray"); self.btn.config(state="disabled"); return
        if is_day:
            self.lbl.config(text="☀️ TRỜI SÁNG ☀️", fg="green"); self.btn.config(state="disabled")
        else:
            self.lbl.config(text="🌙 TRỜI TỐI 🌙", fg="#8B4513"); self.btn.config(state="normal")

# ================= FACTORY TỰ ĐỘNG CẤP PHÁT =================
def get_role_gui_class(role_name):
    """Bốc đúng bảng điều khiển dựa trên class của nhân vật"""
    mapping = {
        "Soi": GuiSoi, 
        "SoiCon": GuiSoi, 
        "PhuThuy": GuiPhuThuy, 
        "TienTri": GuiTienTri, 
        "BaoVe": GuiBaoVe, 
        "ThoSan": GuiThoSan,
        "Dan": GuiDan,
        "TruongLang": GuiDan # Trưởng làng ban đêm như Dân
    }
    return mapping.get(role_name, GuiDan)