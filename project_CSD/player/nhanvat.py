class NhanVat:
    def __init__(self, ten):
        self.ten = ten
        self.phe = None          # Không set cứng
        self.vote = 1
        self.is_alive = True

    def __str__(self):
        trang_thai = "Sống" if self.is_alive else "Chết"
        return f"{self.ten} - {self.phe} - {trang_thai}"


# ================= DÂN =================
class Dan(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"


# ================= SÓI =================
class Soi(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Sói"

    def can(self, muc_tieu):
        if self.is_alive and muc_tieu.is_alive:
            muc_tieu.is_alive = False


# ================= THỢ SĂN =================
class ThoSan(Dan):
    def __init__(self, ten):
        super().__init__(ten)
        self.quyen_tan_cong = 1

    def ban(self, muc_tieu):
        if self.is_alive and self.quyen_tan_cong > 0 and muc_tieu.is_alive:
            muc_tieu.is_alive = False
            self.quyen_tan_cong -= 1


# ================= TRƯỞNG LÀNG =================
class TruongLang(Dan):
    def __init__(self, ten):
        super().__init__(ten)
        self.vote = 2


# ================= PHÙ THỦY =================
class PhuThuy(Dan):
    def __init__(self, ten):
        super().__init__(ten)
        self.binh_cuu = 1
        self.binh_giet = 1

    def cuu(self, muc_tieu):
        if self.is_alive and self.binh_cuu > 0:
            muc_tieu.is_alive = True
            self.binh_cuu -= 1

    def giet(self, muc_tieu):
        if self.is_alive and self.binh_giet > 0 and muc_tieu.is_alive:
            muc_tieu.is_alive = False
            self.binh_giet -= 1


# ================= TIÊN TRI =================
class TienTri(Dan):
    def soi(self, muc_tieu):
        if self.is_alive:
            return muc_tieu.phe


# ================= BẢO VỆ =================
class BaoVe(Dan):
    def __init__(self, ten):
        super().__init__(ten)
        self.da_bao_ve_dem_truoc = None

    def bao_ve(self, muc_tieu):
        if not self.is_alive:
            return False

        if self.da_bao_ve_dem_truoc == muc_tieu.ten:
            print("Không thể bảo vệ 2 đêm liên tiếp!")
            return False

        self.da_bao_ve_dem_truoc = muc_tieu.ten
        return True


# ================= SÓI CON =================
class SoiCon(Soi):
    def __init__(self, ten):
        super().__init__(ten)
        self.duoc_can_dem = False

    def can(self, muc_tieu, dem):
        if not self.is_alive:
            return

        if dem == 1:
            print(f"{self.ten} không thể cắn đêm đầu")
            return

        super().can(muc_tieu)