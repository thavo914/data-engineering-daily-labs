# Day 01 Notes & Active Recall Quiz: Declarative Dataclass Config Registry

> **Date:** 2026-11-26 · **Track:** Phase 1 – Week 01 – Day 01

---

## 1. Tổng hợp kiến thức trọng tâm

### 1.1. Class thường vs. `@dataclass` & Boilerplate
- **Boilerplate** là các đoạn code khuôn mẫu lặp đi lặp lại (`self.x = x`, `__repr__`, `__eq__`) không chứa logic nghiệp vụ mới.
- **Class thường** kế thừa mặc định từ `object`:
  - `print(obj)` in ra tên class và địa chỉ ô nhớ RAM (`<... object at 0x...>`).
  - `obj1 == obj2` mặc định kiểm tra `obj1 is obj2` (so sánh địa chỉ RAM) → trả về `False` dù dữ liệu giống hệt nhau.
- **`@dataclass`** tự động sinh `__init__`, `__repr__`, `__eq__` (và hỗ trợ các tham số mở rộng trong `dataclasses.py` như `frozen=True`, `slots=True`, `kw_only=True`, `order=True`).
  - `@dataclass(frozen=True)` khóa object thành **immutable**, bảo vệ config không bị ghi đè ngoài ý muốn khi pipeline đang chạy.

### 1.2. Dunder Methods (`__init__`, `__repr__`, `__eq__`, `__post_init__`) & `self`
- **`__init__(self, ...)`**: Hàm khởi tạo (constructor) chạy tự động khi tạo object. Không bắt buộc nếu dùng `@dataclass` hoặc class không nhận tham số.
- **`self`**: Đại diện cho chính object cụ thể đang gọi hàm (`id(self) == id(obj)`). Python ngầm dịch `t1.describe()` thành `TableDemo.describe(t1)`. Biến không gắn `self.` là biến cục bộ, sẽ biến mất sau khi `__init__` kết thúc (`AttributeError` nếu truy cập từ ngoài).
- **`__repr__`** (*representation*): Chuỗi biểu diễn chính thức của object dùng cho debug/log.
- **`__eq__`** (*equal*): Định nghĩa phép so sánh `==` theo giá trị các field.
- **`__post_init__`**: Hook của `@dataclass` tự động chạy ngay sau `__init__`, dùng để **Fail-Fast validation** (bắt lỗi YAML ngay lúc khởi động trước khi bật SparkSession).

### 1.3. Decorator trong Python & thực tế repo `etl-streaming`
- **Production:**
  - `@dataclass`: Tự sinh boilerplate cho class dữ liệu.
  - `@staticmethod`: Hàm tiện ích đặt trong class, không dùng `self` hay `cls`.
  - `@property`: Biến method thành thuộc tính chỉ đọc (`cfg.bronze_path`), giữ *Single Source of Truth* và tránh lỗi gõ tay S3 path trong `pipeline.yml`.
  - `@classmethod`: Nhận `cls`, thường dùng làm factory method.
  - `@abstractmethod`: Ép class con bắt buộc phải override.
- **Tests:** `@pytest.mark.parametrize`, `@pytest.fixture`, `@patch`, `@pytest.mark.skipif`, `@unittest.skipUnless`.

---

## 2. Bộ câu hỏi ôn tập (Active Recall)

1. Tại sao với class thường không viết `__eq__`, hai object `p1 = TablePlain("orders", "tier1")` và `p2 = TablePlain("orders", "tier1")` lại cho kết quả `p1 == p2` là `False`?
2. Nếu trong `__init__` bạn viết `name = name` thay vì `self.name = name`, điều gì sẽ xảy ra khi gọi `obj.name` ở bên ngoài?
3. Khi viết hàm nằm trong `class` nhưng không cần truy cập `self` hay `cls`, ta nên gắn decorator nào? Nếu không gắn decorator đó mà cũng bỏ `self` thì gọi qua object sẽ bị lỗi gì?
4. Trong `@dataclass`, option nào giúp khóa object thành *immutable* (không cho phép sửa field sau khi khởi tạo) và tại sao nó hữu ích cho Config?
5. Tại sao nên dùng `@property` cho `bronze_path` và `silver_path` trong `TableConfig` thay vì để người vận hành tự nhập tay trong `pipeline.yml`?
6. Tại sao nên đặt logic validate (`primary_key`, `stream_source`, `tier`) trong `__post_init__` (Fail-Fast) thay vì đợi tới lúc Spark micro-batch chạy rồi mới kiểm tra?

---

<details>
<summary>Đáp án gợi ý</summary>

1. Vì class thường kế thừa `__eq__` mặc định của `object`, vốn kiểm tra `p1 is p2` (cùng địa chỉ RAM) chứ không so sánh dữ liệu bên trong.
2. `name` chỉ là biến cục bộ trong `__init__`, sẽ biến mất khi hàm kết thúc; gọi `obj.name` sẽ ném `AttributeError`.
3. Gắn `@staticmethod`. Nếu bỏ cả `@staticmethod` lẫn `self`, gọi `obj.func()` sẽ bị `TypeError: ... takes 0 positional arguments but 1 was given`.
4. `@dataclass(frozen=True)`. Giúp bảo vệ cấu hình không bị code khác vô tình ghi đè giữa chừng khi pipeline đang chạy.
5. Đảm bảo *Single Source of Truth*, tránh lỗi gõ tay sai tên bucket/hoa-thường, và dễ đổi quy ước đường dẫn hàng loạt ở 1 chỗ duy nhất.
6. Bắt lỗi ngay trong vài mili-giây lúc load YAML trước khi tốn thời gian/tài nguyên khởi tạo `SparkSession`, tránh ghi dữ liệu lỗi nửa vời, và có stacktrace rõ ràng chỉ thẳng vào field sai.

</details>
