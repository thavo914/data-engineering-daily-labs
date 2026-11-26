"""Demo: So sánh class thường, class viết tay boilerplate, và @dataclass."""

from dataclasses import dataclass


# 1. Class thường: chỉ có __init__ (không có __repr__, __eq__)
class TablePlain:
    def __init__(self, name: str, tier: str) -> None:
        self.name = name
        self.tier = tier


# 2. Class viết tay đầy đủ boilerplate (__init__, __repr__, __eq__)
class TableManual:
    def __init__(self, name: str, tier: str) -> None:
        self.name = name
        self.tier = tier

    def __repr__(self) -> str:
        return f"TableManual(name={self.name!r}, tier={self.tier!r})"
        
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TableManual):
            return NotImplemented
        return (self.name, self.tier) == (other.name, other.tier)


# 3. @dataclass: Python tự sinh __init__, __repr__, __eq__
@dataclass
class TableDataclass:
    name: str
    tier: str


if __name__ == "__main__":
    print("=== 1. Class thường (không có __repr__, __eq__) ===")
    p1 = TablePlain("orders", "tier1")
    p2 = TablePlain("orders", "tier1")
    print("p1.name:", p1.name)
    print("print(p1):", p1)
    print("p1 == p2:", p1 == p2)

    print("\n=== 2. Class viết tay boilerplate ===")
    m1 = TableManual("orders", "tier1")
    m2 = TableManual("orders", "tier1")
    print("m1.name:", m1.name)
    print("print(m1):", m1)
    print("m1 == m2:", m1 == m2)

    print("\n=== 3. @dataclass (ngắn gọn, kết quả tương đương) ===")
    d1 = TableDataclass("orders", "tier1")
    d2 = TableDataclass("orders", "tier1")
    print("d1.name:", d1.name)
    print("print(d1):", d1)
    print("d1 == d2:", d1 == d2)
