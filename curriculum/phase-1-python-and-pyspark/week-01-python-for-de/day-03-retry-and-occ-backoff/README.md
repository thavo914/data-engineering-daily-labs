# 🛠️ Day 03: Delta OCC Concurrency Retry & Snapshot Reload

> **Phase:** 1 · **Week:** W01 · **Time Budget:** 60–90 mins · **Type:** Build Lab  
> **Skills:** Higher-Order Functions, Selective Exception Classification, Backoff Strategy, Idempotent Retries

---

## 1. 🎯 Bối cảnh Production (15 phút)

Trong Delta Lake (và nhiều hệ thống ACID dùng Optimistic Concurrency Control — OCC), hai writer đồng thời (ví dụ: job **Streaming Silver MERGE** và job **Hourly Compaction**) đều đọc cùng một snapshot rồi cùng cố ghi commit tiếp theo. Writer đến sau sẽ nhận exception như `ConcurrentAppendException` hoặc `MetadataChangedException`.

Nếu code không retry có chọn lọc:
- **Retry mù quáng mọi lỗi** (như `SyntaxError` hay `SchemaMismatch`) sẽ chỉ làm tốn thời gian vô ích.
- **Retry mà không reload snapshot mới** (`on_retry_reload`) sẽ lại đâm vào đúng phiên bản cũ và fail tiếp.

---

## 2. 📋 Yêu cầu kỹ thuật (Acceptance Criteria)

Mở [`starter/occ_retry.py`](starter/occ_retry.py) và hoàn thiện `execute_with_occ_retry(...)`:
1. Thực thi `operation_fn()` tối đa `max_attempts` lần.
2. Chỉ retry khi `str(exc)` chứa ít nhất 1 từ khóa trong `CONCURRENCY_KEYWORDS`. Mọi exception khác phải **re-raise ngay lập tức ở attempt 1**.
3. Trước mỗi lần retry (khi `attempt < max_attempts`):
   - Gọi `sleep_fn(base_backoff_sec * attempt)` (linear backoff: `2s`, `4s`, ...).
   - Nếu `on_retry_reload` được truyền vào, gọi `on_retry_reload()` để nạp lại table snapshot mới.
4. Nếu hết `max_attempts` mà vẫn lỗi OCC → re-raise exception cuối cùng.
5. Chạy test kiểm tra:
   ```bash
   pytest curriculum/phase-1-python-and-pyspark/week-01-python-for-de/day-03-retry-and-occ-backoff/tests -v
   ```

---

## 3. 🧠 Active Recall (15 phút sau khi code xong)
1. **Tại sao nên truyền `sleep_fn` như một tham số (Dependency Injection) thay vì gọi thẳng `time.sleep` bên trong hàm?**
2. **Sự khác biệt giữa lỗi tạm thời (transient OCC conflict) và lỗi logic vĩnh viễn (permanent error) là gì? Tại sao không nên retry permanent error?**
