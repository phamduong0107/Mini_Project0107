# logic_game.py
import random
from tkinter import messagebox, simpledialog

class GameLogic:
    def bat_dau_dem_nguoc(self):
        self.btn_boc_bai.config(state="disabled")
        self.dem_nguoc_role(5)

    def dem_nguoc_role(self, count):
        if count > 0:
            self.lbl_role_result.config(text=f"Hệ thống đang phát vai trò... {count}s")
            self.root.after(1000, self.dem_nguoc_role, count - 1)
        else:
            temp_list = [t.nhan_vat for t in self.players.iter_nodes()]
            self.my_character = random.choice(temp_list)
            self.lbl_role_result.config(text=f"Bạn là: {self.my_character.ten}\n(Vai trò: {self.my_character.__class__.__name__} - Phe: {getattr(self.my_character, 'phe', 'Dân')})")
            self.btn_vao_lang.config(state="normal")
# Trong file gui.py, hàm vao_game(self)
    def vao_game(self):
        self.show_game_screen()
        self.timer_running = True
        self.update_timer()
        # Kích hoạt luồng chat tự động của NPC ở đây 
        self.lich_trinh_chat_npc()

    def ap_dung_hieu_ung_ngay_dem(self):
        bg_main = "#ECF0F1" if self.is_day else "#2C3E50" 
        bg_panel = "white" if self.is_day else "#34495E"
        self.root.config(bg=bg_main); self.main_game_frame.config(bg=bg_main)
        self.right_frame.config(bg=bg_main); self.grid_frame.config(bg=bg_main)
        self.chat_frame.config(bg=bg_panel)
        self.time_lbl.config(text="☀️ BAN NGÀY" if self.is_day else "🌙 BAN ĐÊM", fg="#2980B9" if self.is_day else "#F1C40F", bg=bg_panel)
        self.lbl_countdown.config(bg=bg_panel)
        self.cap_nhat_giao_dien_luoi()

    def tim_nhan_vat_theo_nhap_lieu(self, nhap):
        nhap = str(nhap).strip().lower()
        temp = self.players.head
        while temp:
            ten_that = temp.nhan_vat.ten.lower() 
            if nhap == ten_that or nhap == ten_that.replace("player ", ""):
                if temp.nhan_vat.is_alive: return temp.nhan_vat
            temp = temp.next
        return None

    def toggle_time(self):
        self.is_day = not self.is_day
        self.time_left = 150 if self.is_day else 60

        if not self.is_day: 
            # === KIỂM TRA ĐIỀU KIỆN 100% PHẢI VOTE ===
            alive_count = sum(1 for p in self.players.iter_nodes() if p.nhan_vat.is_alive)
            # Chuyển tất cả tên về viết thường trước khi đưa vào set để đếm chính xác
            so_nguoi_da_vote = len(set(str(v['voter']).strip().lower() for v in self.chi_tiet_vote))
            
            if so_nguoi_da_vote < alive_count:
                messagebox.showwarning("Cảnh báo", f"Chưa đủ phiếu! ({so_nguoi_da_vote}/{alive_count} người đã vote). Tất cả phải vote mới được đi ngủ!")
                self.is_day = True; return 

            self.btn_vote.config(state="disabled"); self.btn_vote_truong_lang.config(state="disabled")
            
            # Xử lý Ngày 1 (Bầu trưởng làng)
            if self.ngay_thu == 1 and not self.truong_lang:
                if self.danh_sach_vote:
                    win = max(set(self.danh_sach_vote), key=self.danh_sach_vote.count)
                    t = self.players.head
                    while t:
                        if t.nhan_vat.ten.lower() == win and t.nhan_vat.is_alive: 
                            self.truong_lang = t.nhan_vat; break
                        t = t.next
                    self.xuat_thong_bao_chat(f"\n👑 KẾT QUẢ: {self.truong_lang.ten} là TRƯỞNG LÀNG!")
                
                self.danh_sach_vote = []; self.chi_tiet_vote = []; self.ngay_thu += 1
                self.ap_dung_hieu_ung_ngay_dem()
                self.xuat_thong_bao_chat("\n--- TRỜI TỐI, LÀNG ĐI NGỦ ---")
                if hasattr(self, 'role_gui'): self.role_gui.cap_nhat_ui_theo_thoi_gian(self.is_day)
                self.update_timer(); return

            # Xử lý Treo cổ
            if self.danh_sach_vote:
                counts = {x:self.danh_sach_vote.count(x) for x in set(self.danh_sach_vote)}
                m = max(counts.values())
                tied = [k for k,v in counts.items() if v == m]
                
                if len(tied) > 1: 
                    self.xuat_thong_bao_chat(f"\n⚖️ HÒA PHIẾU giữa {', '.join(tied)}! Vote lại ngay!")
                    self.danh_sach_vote = []; self.chi_tiet_vote = []; self.is_day = True; self.time_left = 60
                    self.kich_hoat_npc_vote(); self.update_timer(); return
                
                die_name = tied
                self.xuat_thong_bao_chat(f"\n⚖️ LÀNG TREO CỔ: {die_name.upper()}")
                t = self.players.head
                while t:
                    if t.nhan_vat.ten.lower() == die_name: 
                        t.nhan_vat.is_alive = False
                        if self.truong_lang == t.nhan_vat: self.truong_lang = None
                        break
                    t = t.next

            self.danh_sach_vote = []; self.chi_tiet_vote = []; self.ngay_thu += 1; 
            self.ap_dung_hieu_ung_ngay_dem(); self.kiem_tra_ban_than_chet()
            if self.kiem_tra_thang_thua(): return
            self.xuat_thong_bao_chat("\n--- TRỜI TỐI, LÀNG ĐI NGỦ ---")
            self.night_actions = {"soi_target":[], "bao_ve_target":None, "phu_thuy_cuu":False, "phu_thuy_doc_target":None, "tho_san_target":None}
            if hasattr(self, 'role_gui'): self.role_gui.cap_nhat_ui_theo_thoi_gian(self.is_day)
                
        else: 
            # SÁNG THỨC DẬY
            if self.my_character.is_alive and self.ngay_thu > 1: self.btn_vote.config(state="normal")
            if not self.truong_lang: self.btn_vote_truong_lang.config(state="normal")
            self.ap_dung_hieu_ung_ngay_dem()
            self.xuat_thong_bao_chat("\n--- TRỜI SÁNG, LÀNG THỨC DẬY ---")
            deads = self.ket_toan_ban_dem()
            self.xuat_thong_bao_chat(f"💀 Đêm qua chết: {', '.join([n.ten for n in deads]) if deads else 'Bình yên'}")
            if self.truong_lang in deads: 
                self.truong_lang = None
                self.xuat_thong_bao_chat("👑 Trưởng làng chết! Phải bầu lại!")
                self.btn_vote_truong_lang.config(state="normal")
            
            self.cap_nhat_giao_dien_luoi(); self.kiem_tra_ban_than_chet()
            if hasattr(self, 'role_gui'): self.role_gui.cap_nhat_ui_theo_thoi_gian(self.is_day)
            # NPC tự động chuẩn bị vote
            self.root.after(2000, self.kich_hoat_npc_vote)
            if self.kiem_tra_thang_thua(): return
        self.update_timer()
    def update_timer(self):
        if self.timer_running and self.time_left >= 0:
            self.lbl_countdown.config(text=f"Thời gian: {self.time_left//60:02d}:{self.time_left%60:02d}")
            
            # --- CƠ CHẾ TỰ GIÁC VOTE ---
            # Nếu còn 30 giây mà NPC nào chưa vote, hệ thống sẽ bắt đầu ép vote dần
            if self.is_day and self.time_left == 30:
                self.xuat_thong_bao_chat("📢 Hệ thống: Còn 30s, các NPC đang hoàn tất phiếu bầu...")
                self.ep_tat_ca_npc_vote()

            self.time_left -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running:
            # Khi hết giờ, kiểm tra cuối cùng trước khi đổi sang đêm
            if self.is_day:
                self.ep_tat_ca_npc_vote() 
            self.toggle_time()

    def ep_tat_ca_npc_vote(self):
        """Hàm đảm bảo 100% NPC còn sống phải có tên trong chi_tiet_vote"""
        if not self.is_day: return
        
        # Lấy danh sách những người còn sống
        alive_players = [p.nhan_vat for p in self.players.iter_nodes() if p.nhan_vat.is_alive]
        loai_vote = "BẦU TRƯỞNG LÀNG" if not self.truong_lang else "VOTE TREO CỔ"

        for npc in alive_players:
            if npc == self.my_character: continue
            
            # Sửa dòng kiểm tra này để không bị lỗi chữ hoa/thường
            da_vote = any(str(v['voter']).lower() == npc.ten.lower() for v in self.chi_tiet_vote)
            
            if not da_vote:
                self.npc_tu_dong_vote(npc, loai_vote)

    def kich_hoat_npc_vote(self):
        """Ép tất cả NPC còn sống thực hiện vote"""
        if not self.is_day: return
        lives = [p.nhan_vat for p in self.players.iter_nodes() if p.nhan_vat.is_alive and p.nhan_vat != self.my_character]
        loai = "BẦU TRƯỞNG LÀNG" if not self.truong_lang else "VOTE TREO CỔ"
        for i, npc in enumerate(lives):
            # Mỗi NPC vote cách nhau 1-5 giây cho tự nhiên
            self.root.after((i+1) * random.randint(1000, 3000), lambda n=npc: self.npc_tu_dong_vote(n, loai))
    def ket_toan_ban_dem(self):
        deads = []
        # Xử lý Sói cắn (Nếu không vote thì chọn ngẫu nhiên) 
        s_targets = self.night_actions["soi_target"]
        if not s_targets: 
            lives = [p.nhan_vat for p in self.players.iter_nodes() if p.nhan_vat.is_alive and getattr(p.nhan_vat, 'phe', '') != "Sói"]
            if lives: s_targets.append(random.choice(lives))
        
        for s in s_targets: 
            if s.is_alive and s != self.night_actions["bao_ve_target"]: 
                s.is_alive = False; deads.append(s)
        
        # Xử lý Phù thủy bình độc [cite: 15]
        doc = self.night_actions["phu_thuy_doc_target"] 
        if doc and doc.is_alive: doc.is_alive = False; deads.append(doc)
            
        # Xử lý súng Thợ săn [cite: 17]
        gun = self.night_actions["tho_san_target"] 
        if gun and gun.is_alive:
            gun.is_alive = False; deads.append(gun)
            if getattr(gun, 'phe', '') != "Sói": # Bắn nhầm dân, thợ săn chết theo
                t = self.players.head
                while t:
                    if t.nhan_vat.__class__.__name__ == "ThoSan": 
                        t.nhan_vat.is_alive = False; deads.append(t.nhan_vat); break
                    t = t.next
        
        # Kiểm tra Sói con chết để kích hoạt giận dữ [cite: 19]
        self.soi_gian_du = any(n.__class__.__name__ == "SoiCon" for n in deads) 
        return list(set(deads))

    def kiem_tra_ban_than_chet(self):
        if not self.my_character.is_alive and not self.has_shown_death_dialog:
            self.has_shown_death_dialog = True
            ans = messagebox.askyesno("BẠN ĐÃ CHẾT", "Bạn đã bị loại khỏi trò chơi!\n\nBạn muốn XEM TIẾP (Yes) hay CHƠI VÁN MỚI (No)?") # [cite: 21]
            if not ans: self.timer_running = False; self.show_main_menu()

    def kiem_tra_thang_thua(self):
        s = d = 0
        t = self.players.head
        while t:
            if t.nhan_vat.is_alive:
                if getattr(t.nhan_vat, 'phe', '') == "Sói": s += 1
                else: d += 1
            t = t.next
        if s >= d: 
            messagebox.showinfo("KẾT THÚC", "🐺 BẦY SÓI ĐÃ CHIẾN THẮNG!"); self.timer_running = False; self.show_main_menu(); return True
        if s == 0: 
            messagebox.showinfo("KẾT THÚC", "🌾 DÂN LÀNG ĐÃ CHIẾN THẮNG!"); self.timer_running = False; self.show_main_menu(); return True
        return False
        
    def hien_thi_khung_vote(self, loai_vote):
        if not self.is_day or not self.my_character.is_alive: return
        if self.ngay_thu == 1 and loai_vote == "VOTE TREO CỔ":
            messagebox.showwarning("Luật", "Ngày đầu tiên không được Vote treo cổ!"); return # [cite: 7]
        if loai_vote == "BẦU TRƯỞNG LÀNG" and self.truong_lang:
            messagebox.showinfo("Thông báo", "Làng đã có Trưởng Làng rồi!"); return
            
        nhap = simpledialog.askstring(loai_vote, "Nhập SỐ thứ tự người bạn chọn (Ví dụ: 3):")
        muc_tieu = self.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        
        if muc_tieu:
            # 5. TRƯỞNG LÀNG CÓ 2 PHIẾU VOTE TREO CỔ 
            so_phieu = 1
            if loai_vote == "VOTE TREO CỔ" and self.truong_lang == self.my_character:
                so_phieu = 2
            
            for _ in range(so_phieu): 
                self.danh_sach_vote.append(muc_tieu.ten.lower())
            
            self.xuat_thong_bao_chat(f"🗳️ Bạn đã vote cho: {muc_tieu.ten} ({so_phieu} phiếu)")
            
            if loai_vote == "BẦU TRƯỞNG LÀNG": self.btn_vote_truong_lang.config(state="disabled")
            else: self.btn_vote.config(state="disabled") 
            
            self.cap_nhat_giao_dien_luoi() 
            for _ in range(3): self.root.after(random.randint(1000, 3000), lambda: self.npc_tu_dong_vote(loai_vote))
        else:
            if nhap: messagebox.showerror("Lỗi", "Số không hợp lệ hoặc người đã chết!")

    def npc_tu_dong_vote(self, npc, loai_vote):
        """Logic NPC chọn mục tiêu và thực hiện vote"""
        if not npc.is_alive or not self.is_day: return
        
        # Danh sách mục tiêu có thể vote (những người còn sống)
        targets = [p.nhan_vat for p in self.players.iter_nodes() if p.nhan_vat.is_alive]
        if not targets: return
        
        target = random.choice(targets)
        
        # Trưởng làng vote 2 phiếu cho treo cổ
        so_phieu = 2 if (self.truong_lang == npc and loai_vote == "VOTE TREO CỔ") else 1
        
        for _ in range(so_phieu):
            self.danh_sach_vote.append(target.ten.lower())
        
        # Ghi nhận vào chi tiết để hệ thống biết NPC này đã xong nhiệm vụ
        self.chi_tiet_vote.append({'voter': npc.ten, 'target': target.ten})
        
        self.xuat_thong_bao_chat(f"🗳️ {npc.ten} đã tự giác vote cho {target.ten}")
        self.cap_nhat_giao_dien_luoi()