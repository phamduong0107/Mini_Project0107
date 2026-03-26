

class NhanVat:
    def __init__(self, ten):
        self.ten = ten
        self.is_alive = True
        self.mang = 1      # máu hoặc lượt sống
        self.vote = 1      # phiếu vote (tùy game)
        self.phe = "Dân"   # mặc định phe Dân

    def __repr__(self):
        return f"{self.ten} ({self.__class__.__name__})"


# ==== CLASS ROLE ====
class Soi(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Sói"


class SoiCon(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Sói"


class Dan(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"


class PhuThuy(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"


class TienTri(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"


class BaoVe(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"


class ThoSan(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"


class TruongLang(NhanVat):
    def __init__(self, ten):
        super().__init__(ten)
        self.phe = "Dân"