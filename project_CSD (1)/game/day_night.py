# game/day_night.py
import random
from player.roles import Soi, SoiCon, ThoSan, PhuThuy, BaoVe

class DayNightCycle:
    def __init__(self, game_logic):
        self.game = game_logic  # tham chiếu tới GameLogic để truy cập players, GUI
        self.night_events = []

    def start_night(self):
        self.night_events.clear()
        # reset các hành động đêm
        self.game.night_actions = {
            "soi_target": [],        # danh sách target của Sói vote
            "bao_ve_target": None,   # ai được bảo vệ
            "phu_thuy_cuu": False,   # phù thủy cứu
            "phu_thuy_doc_target": None,  # phù thủy đầu độc
            "tho_san_target": None        # thợ săn phản công
        }
        self.game.is_day = False
        self.game.time_left = 60  # ví dụ: đêm 60s
        # cập nhật UI nếu có role GUI
        if hasattr(self.game, 'role_gui'):
            self.game.role_gui.cap_nhat_ui_theo_thoi_gian(self.game.is_day)

    def start_day(self):
        self.game.is_day = True
        self.game.time_left = 60  # ví dụ: ngày 150s
        if hasattr(self.game, 'role_gui'):
            self.game.role_gui.cap_nhat_ui_theo_thoi_gian(self.game.is_day)

    def process_night(self):
        deads = []
        soi_kill = None

        # tìm phù thủy nếu có
        phu_thuy = next((p.nhan_vat for p in self.game.players.iter_nodes() if p.nhan_vat.__class__.__name__ == "PhuThuy"), None)

        # ========== 1. Sói chọn mục tiêu ==========
        s_targets = [t for t in self.game.night_actions["soi_target"] if t.is_alive and getattr(t, 'phe', '') != "Sói"]
        if s_targets:
            self.night_events.append("🐺 Sói đã chọn mục tiêu!")
            counts = {x: s_targets.count(x) for x in set(s_targets)}
            max_vote = max(counts.values())
            top_targets = [k for k, v in counts.items() if v == max_vote]
            target = random.choice(top_targets)
        else:
            candidates = [p.nhan_vat for p in self.game.players.iter_nodes() if p.nhan_vat.is_alive and getattr(p.nhan_vat, 'phe', '') != "Sói"]
            target = random.choice(candidates) if candidates else None

        # ========== 2. Kiểm tra Bảo vệ ==========
        if target and target.is_alive:
            if target == self.game.night_actions["bao_ve_target"]:
                self.night_events.append(f"🛡️ {target.ten} đã được bảo vệ!")
            else:
                target.is_alive = False
                deads.append(target)
                soi_kill = target
                self.night_events.append(f"🐺 {target.ten} bị giết bởi Sói")

# ========== 3. Phù thủy cứu ==========
        if self.game.night_actions["phu_thuy_cuu"] and soi_kill and phu_thuy and phu_thuy.binh_cuu > 0:
            phu_thuy.cuu(soi_kill) # <-- GỌI HÀM OOP Ở ĐÂY (Nó sẽ tự đổi is_alive và trừ bình)
            if soi_kill in deads:
                deads.remove(soi_kill)
            self.night_events.append(f"🧪 Phù thủy đã cứu: {soi_kill.ten}")

# ========== 4. Phù thủy đầu độc ==========
        doc = self.game.night_actions["phu_thuy_doc_target"]
        if doc and doc.is_alive and phu_thuy and phu_thuy.binh_giet > 0:
            if doc == soi_kill and self.game.night_actions["phu_thuy_cuu"]:
                self.night_events.append("⚠️ Không thể đầu độc người vừa được cứu!")
            else:
                phu_thuy.giet(doc) # <-- GỌI HÀM OOP Ở ĐÂY
                deads.append(doc)
                self.night_events.append(f"☠️ Phù thủy đã đầu độc: {doc.ten}")

# ========== 5. Thợ săn phản công ==========
        for t in self.game.players.iter_nodes():
            nv = t.nhan_vat
            if nv.__class__.__name__ == "ThoSan" and nv in deads:
                target = self.game.night_actions["tho_san_target"]
                if target and target.is_alive:
                    nv.ban(target) # <-- GỌI HÀM OOP Ở ĐÂY
                    if not target.is_alive and target not in deads:
                        deads.append(target)
                    self.night_events.append(f"🔫 Thợ săn bắn: {target.ten}")
                break

        # ========== 6. SóiCon tác động ==========
        self.game.soi_gian_du = any(n.__class__.__name__ == "SoiCon" for n in deads)

        return deads