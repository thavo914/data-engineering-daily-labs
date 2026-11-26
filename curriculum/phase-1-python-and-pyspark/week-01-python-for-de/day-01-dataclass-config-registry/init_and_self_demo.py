"""Demo: Hiểu rõ __init__ và self trong Python."""


class TableDemo:
    def __init__(self, name: str, tier: str) -> None:
        print(f"  [__init__] Đang khởi tạo object tại id={id(self)}")
        self.name = name  # Gắn vào object (sống lâu dài cùng object)
        self.tier = tier
        temp_note = "biến tạm"  # Không có self -> biến mất khi __init__ xong
        _ = temp_note

    def describe(self) -> str:
        return f"Bảng '{self.name}' thuộc {self.tier} (id={id(self)})"


class BrokenTable:
    def __init__(self, name: str) -> None:
        # Lỗi thường gặp: quên `self.name = name`, chỉ gán biến cục bộ
        name = name  # noqa: PLW0127


if __name__ == "__main__":
    print("=== 1. self chính là object vừa tạo (id giống hệt nhau) ===")
    t1 = TableDemo("orders", "tier1")
    print(f"  [bên ngoài] t1 có id={id(t1)}")

    t2 = TableDemo("bookings", "tier2")
    print(f"  [bên ngoài] t2 có id={id(t2)}")

    print("\n=== 2. t1 và t2 dùng chung hàm describe(), nhưng self tách biệt dữ liệu ===")
    print("  t1.describe()         ->", t1.describe())
    print("  t2.describe()         ->", t2.describe())

    print("\n=== 3. Python ngầm dịch t1.describe() thành TableDemo.describe(t1) ===")
    print("  TableDemo.describe(t1) ->", TableDemo.describe(t1))

    print("\n=== 4. Nếu quên `self.name = name` trong __init__ ===")
    broken = BrokenTable("ghost_table")
    try:
        print(broken.name)
    except AttributeError as err:
        print("  Lỗi AttributeError:", err)
