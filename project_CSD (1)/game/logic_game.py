# logic_game.py
import random
from mechanics.graph import Graph
from tkinter import messagebox, simpledialog
from .day_night import DayNightCycle
from player.LinkedList import LinkedList
from player.roles import Soi, SoiCon, Dan, PhuThuy, TienTri, BaoVe, ThoSan, TruongLang

class GameLogic:
    def __init__(self, root):
        # GUI & players
        self.root = root
        self.players = LinkedList()
        self.my_character = None
        self.truong_lang = None

        # Time & day/night
        self.is_day = True
        self.time_left = 0
        self.timer_running = False

        # Vote
        self.danh_sach_vote = []
        self.vote_graph = Graph()

        # Chat
        self.chat_frame = None
        self.main_game_frame = None
        self.right_frame = None
        self.grid_frame = None
        self.lbl_countdown = None
        self.time_lbl = None
        self.lbl_role_result = None

        # DayNight handler
        self.day_night = DayNightCycle(self)

        # Death dialog
        self.has_shown_death_dialog = False

        # Night actions
        self.night_actions = {}

    # ===== BẮT ĐẦU ĐẾM NGƯỢC PHÁT VAI TRÒ =====
    def bat_dau_dem_nguoc(self):
        self.btn_boc_bai.config(state="disabled")
        self.dem_nguoc_role(3)

    def dem_nguoc_role(self, count):
        if count > 0:
            self.lbl_role_result.config(text=f"Hệ thống đang phát vai trò... {count}s")
            self.root.after(1000, self.dem_nguoc_role, count-1)
        else:
            temp_list = [t.nhan_vat for t in self.players.iter_nodes()]
            self.my_character = random.choice(temp_list)
            self.lbl_role_result.config(
                text=f"Bạn là: {self.my_character.ten}\n(Vai trò: {self.my_character.__class__.__name__} - Phe: {getattr(self.my_character,'phe','Dân')})"
            )
            self.btn_vao_lang.config(state="normal")

    # ===== CẬP NHẬT GIAO DIỆN NGÀY/ĐÊM =====
    def ap_dung_hieu_ung_ngay_dem(self):
        bg_main = "#ECF0F1" if self.is_day else "#2C3E50"
        bg_panel = "white" if self.is_day else "#34495E"

        self.root.config(bg=bg_main)
        self.main_game_frame.config(bg=bg_main)
        self.right_frame.config(bg=bg_main)
        self.grid_frame.config(bg=bg_main)
        self.chat_frame.config(bg=bg_panel)
        self.time_lbl.config(text="☀️ BAN NGÀY" if self.is_day else "🌙 BAN ĐÊM",
                             fg="#2980B9" if self.is_day else "#F1C40F",
                             bg=bg_panel)
        self.lbl_countdown.config(bg=bg_panel)
        self.cap_nhat_giao_dien_luoi()

    # ===== TÌM NHÂN VẬT THEO NHẬP LIỆU =====
    def tim_nhan_vat_theo_nhap_lieu(self, nhap):
        nhap = str(nhap).strip().lower()
        temp = self.players.head
        while temp:
            ten_that = temp.nhan_vat.ten.lower()
            if nhap == ten_that or nhap == ten_that.replace("player ", ""):
                if temp.nhan_vat.is_alive:
                    return temp.nhan_vat
            temp = temp.next
        return None

# ===== CHUYỂN NGÀY/ĐÊM =====
    def toggle_time(self):
        if self.is_day:
            # 🌙 TỪ NGÀY CHUYỂN SANG ĐÊM
            self.day_night.start_night()
            self.xuat_thong_bao_chat("\n--- TRỜI TỐI, LÀNG ĐI NGỦ ---")
            self.xuat_thong_bao_chat("Mọi người có 60s để thực hiện chức năng đêm!")
        else:
            # ☀️ TỪ ĐÊM CHUYỂN SANG NGÀY
            deads = self.day_night.process_night()
            self.day_night.start_day()
            
            # ===== 3 DÒNG FIX LỖI Ở ĐÂY =====
            self.ngay_thu += 1
            self.btn_vote.config(state="normal")
            self.vote_graph = Graph()
            # ================================
            
            self.xuat_thong_bao_chat(f"\n--- TRỜI SÁNG, LÀNG THỨC DẬY (BẮT ĐẦU NGÀY {self.ngay_thu}) ---")
            
            for event in self.day_night.night_events:
                self.xuat_thong_bao_chat(event)

            deads_list = [p.nhan_vat for p in self.players.iter_nodes() if not p.nhan_vat.is_alive and getattr(p.nhan_vat,'phe','') != "Sói"]
            self.xuat_thong_bao_chat(f"💀 Đêm qua chết: {', '.join([n.ten for n in deads_list]) if deads_list else 'Bình yên'}")
            
            if self.truong_lang in deads_list:
                self.truong_lang = None
                self.xuat_thong_bao_chat("👑 Trưởng làng đã chết! Bầu trưởng làng mới!")
                self.btn_vote_truong_lang.config(state="normal")

        # ====== CÁC LỆNH CẬP NHẬT GIAO DIỆN ======
        self.ap_dung_hieu_ung_ngay_dem()      
        self.cap_nhat_danh_sach_hoi_thoai()   
        
        self.cap_nhat_giao_dien_luoi()
        self.kiem_tra_ban_than_chet()
        if self.kiem_tra_thang_thua():
            return
        self.update_timer()

# ===== TIMER =====
    def update_timer(self):
        if self.timer_running and self.time_left >= 0:
            self.lbl_countdown.config(text=f"Thời gian: {self.time_left//60:02d}:{self.time_left%60:02d}")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer) # <--- GÁN ID VÀO ĐÂY
        elif self.timer_running:
            if self.timer_id:                                        # <--- THÊM KIỂM TRA
                self.root.after_cancel(self.timer_id)                # <--- THÊM LỆNH HỦY
            self.toggle_time()

    # ===== KIỂM TRA NGƯỜI CHƠI CHẾT =====
    def kiem_tra_ban_than_chet(self):
        if not self.my_character.is_alive and not self.has_shown_death_dialog:
            self.has_shown_death_dialog = True
            ans = messagebox.askyesno("BẠN ĐÃ CHẾT", "Bạn đã bị loại khỏi trò chơi!\n\nXem tiếp (Yes) hay Chơi ván mới (No)?")
            if not ans:
                self.timer_running = False
                self.show_main_menu()

    # ===== KIỂM TRA THẮNG THUA =====
    def kiem_tra_thang_thua(self):
        s = d = 0
        t = self.players.head
        while t:
            if t.nhan_vat.is_alive:
                if getattr(t.nhan_vat,'phe','') == "Sói": s+=1
                else: d+=1
            t = t.next
        if s>=d:
            messagebox.showinfo("KẾT THÚC", "🐺 BÀY SÓI CHIẾN THẮNG!")
            self.timer_running = False
            self.show_main_menu()
            return True
        if s==0:
            messagebox.showinfo("KẾT THÚC", "🌾 DÂN LÀNG CHIẾN THẮNG!")
            self.timer_running = False
            self.show_main_menu()
            return True
        return False

    # ===== HIỂN THỊ KHUNG VOTE =====
    def hien_thi_khung_vote(self, loai_vote):
        if not self.is_day or not self.my_character.is_alive:
            return
        if self.ngay_thu==1 and loai_vote=="VOTE TREO CỔ":
            messagebox.showwarning("Luật", "Ngày đầu tiên không được Vote treo cổ!")
            return
        if loai_vote=="BẦU TRƯỞNG LÀNG" and self.truong_lang:
            messagebox.showinfo("Thông báo", "Làng đã có Trưởng Làng rồi!")
            return

        nhap = simpledialog.askstring(loai_vote, "Nhập số thứ tự người bạn chọn:")
        muc_tieu = self.tim_nhan_vat_theo_nhap_lieu(nhap) if nhap else None
        if muc_tieu:
            so_phieu = 2 if self.truong_lang==self.my_character and loai_vote=="VOTE TREO CỔ" else 1
            voter = self.my_character.ten

            # ===== GRAPH VOTE =====
            self.vote_graph.add_edge(voter, muc_tieu.ten)

            for _ in range(so_phieu):
                self.danh_sach_vote.append(muc_tieu.ten.lower())
            self.xuat_thong_bao_chat(f"🗳️ Bạn đã vote cho: {muc_tieu.ten} ({so_phieu} phiếu)")

            if loai_vote=="BẦU TRƯỞNG LÀNG":
                self.btn_vote_truong_lang.config(state="disabled")
            else:
                self.btn_vote.config(state="disabled")

            self.cap_nhat_giao_dien_luoi()
            self.root.after(random.randint(1000,3000), lambda: self.npc_tu_dong_vote(loai_vote))
        else:
            if nhap:
                messagebox.showerror("Lỗi", "Số không hợp lệ hoặc người đã chết!")

    def npc_tu_dong_vote(self, loai_vote):
        song_list = self.get_alive_players()
        npc_list = [p for p in song_list if p != self.my_character]
        
        # Tạo 2 biến đếm để theo dõi tiến độ
        self.tong_so_npc_can_vote = len(npc_list)
        self.so_npc_da_vote = 0

        # Nếu chỉ còn mỗi người chơi sống (không có NPC nào), chốt kết quả luôn
        if self.tong_so_npc_can_vote == 0:
            self.tong_ket_vote(loai_vote)
            return

        for npc in npc_list:
            # Hẹn giờ ngẫu nhiên từ 1 đến 7 giây
            delay = random.randint(1000, 7000)
            
            # Lưu ý kiến thức: Phải dùng 'v=npc' trong lambda để tránh lỗi Late Binding 
            # (nếu không, tất cả các khoảng hẹn giờ sẽ chỉ lấy tên của NPC cuối cùng trong danh sách)
            self.root.after(delay, lambda v=npc: self.mot_npc_thuc_hien_vote(v, loai_vote))

    def mot_npc_thuc_hien_vote(self, voter, loai_vote):
        song_list = self.get_alive_players()
        target_list = [p for p in song_list if p != voter]
        
        if target_list:
            # Chọn mục tiêu vote hoàn toàn ngẫu nhiên
            target = random.choice(target_list)

            so_phieu = 2 if self.truong_lang == voter and loai_vote == "VOTE TREO CỔ" else 1
            
            # Lưu vào Đồ thị Graph
            self.vote_graph.add_edge(voter.ten, target.ten)

            # Bỏ phiếu vào hòm
            for _ in range(so_phieu):
                self.danh_sach_vote.append(target.ten.lower())

            self.xuat_thong_bao_chat(f"🗳️ {voter.ten} đã vote cho {target.ten}")
            self.cap_nhat_giao_dien_luoi()

        # Dù có vote được hay không, vẫn phải tăng biến đếm để báo cáo là NPC này đã xử lý xong
        self.so_npc_da_vote += 1
        
        # Nếu số người đã vote bằng với tổng số NPC, tiến hành đếm phiếu
        if self.so_npc_da_vote >= self.tong_so_npc_can_vote:
            self.root.after(1500, lambda: self.tong_ket_vote(loai_vote)) # Chờ 1.5s cho người chơi đọc chat rồi mới chốt sổ

    def tong_ket_vote(self, loai_vote):
        if not self.danh_sach_vote:
            self.xuat_thong_bao_chat("⚖️ Không có ai bị vote.")
            return

        # Đếm phiếu tìm ra người cao nhất
        counts = {x: self.danh_sach_vote.count(x) for x in set(self.danh_sach_vote)}
        max_vote = max(counts.values())
        top_targets = [k for k, v in counts.items() if v == max_vote]

        if len(top_targets) > 1:
            self.xuat_thong_bao_chat("⚖️ Kết quả hòa! Thùng phiếu đã dọn sạch, hãy vote lại đi làng ơi!")
            
            # Mở khóa lại nút bấm để người chơi được quyền mở cuộc vote mới
            if loai_vote == "BẦU TRƯỞNG LÀNG":
                self.btn_vote_truong_lang.config(state="normal")
            else:
                self.btn_vote.config(state="normal")
        else:
            target_name = top_targets[0]
            # Tìm object nhân vật tương ứng với tên
            target = next((p.nhan_vat for p in self.players.iter_nodes() if p.nhan_vat.ten.lower() == target_name), None)
            
            if target:
                if loai_vote == "BẦU TRƯỞNG LÀNG":
                    self.truong_lang = target
                    self.xuat_thong_bao_chat(f"👑 {target.ten} đã đắc cử Trưởng Làng!")
                    self.xuat_thong_bao_chat("⏰ Bầu cử xong! Làng chuẩn bị đi ngủ...")
                    self.time_left = 0
                else:
                    target.is_alive = False
                    self.xuat_thong_bao_chat(f"💀 {target.ten} đã bị dân làng treo cổ!")

        # Đổ thùng phiếu đi để chuẩn bị cho ngày hôm sau
        self.danh_sach_vote.clear()
        
        # Cập nhật lại giao diện và kiểm tra xem Sói/Dân đã thắng chưa
        self.cap_nhat_giao_dien_luoi()
        if loai_vote == "VOTE TREO CỔ":
            self.kiem_tra_thang_thua()

    # ===== LẤY DANH SÁCH NGƯỜI CHƠI CÒN SỐNG =====
    def get_alive_players(self):
        return [p.nhan_vat for p in self.players.iter_nodes() if p.nhan_vat.is_alive]

    def cap_nhat_giao_dien_luoi(self):
        # Cập nhật giao diện lưới (placeholder)
        pass

    def show_main_menu(self):
        # Placeholder menu chính
        print("Về menu chính")