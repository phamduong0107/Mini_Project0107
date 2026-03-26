# game/setup_game.py
import random
from player.LinkedList import LinkedList
from player.roles import Soi, SoiCon, Dan, PhuThuy, TienTri, BaoVe, ThoSan, TruongLang

def setup_game(so_luong, ten_nguoi_choi=None):
    """
    Thiết lập game: tạo LinkedList người chơi với role ngẫu nhiên
    """
    # ===== CHỌN BỘ ROLE =====
    if so_luong == 8:
        danh_sach_vai_tro = [
            Soi, Soi,
            PhuThuy, TienTri, BaoVe,
            Dan, Dan, Dan
        ]
    elif so_luong == 15:
        danh_sach_vai_tro = (
            [Soi]*4 +
            [SoiCon] +
            [PhuThuy, TienTri, BaoVe] +
            [Dan]*7
        )
    elif so_luong == 20:
        danh_sach_vai_tro = (
            [Soi]*5 +
            [SoiCon]*2 +
            [PhuThuy, TienTri, BaoVe] +
            [Dan]*10
        )
    else:
        raise ValueError("Số lượng người chơi không hợp lệ!")

    # ===== RANDOM ROLE =====
    random.shuffle(danh_sach_vai_tro)

    # ===== TẠO LINKED LIST NGƯỜI CHƠI =====
    nguoi_choi = LinkedList()

    for i in range(so_luong):
        # Nếu có tên truyền vào, dùng tên đó; nếu không, auto tên Player 1,2,3...
        if ten_nguoi_choi and i < len(ten_nguoi_choi):
            ten = ten_nguoi_choi[i]
        else:
            ten = f"Player {i+1}"

        nhan_vat = danh_sach_vai_tro[i](ten)
        nguoi_choi.append(nhan_vat)

    return nguoi_choi

# ===== HELPER DEBUG =====
def display_players(nguoi_choi):
    temp = nguoi_choi.head
    print("=== DANH SÁCH NGƯỜI CHƠI ===")
    while temp:
        print(f"{temp.nhan_vat.ten} | Role: {temp.nhan_vat.__class__.__name__} | {'Sống' if temp.nhan_vat.is_alive else 'Chết'}")
        temp = temp.next