# 🛠️ Day 02: Closures, Enclosing Cache & `try/finally` Resource Hygiene

> **Phase:** 1 · **Week:** W01 · **Time Budget:** 60–90 mins · **Type:** Build Lab  
> **Skills:** Higher-Order Functions, Closures, Mutable Enclosing State, `try/except/finally` Memory Cleanup

---

## 1. 🎯 Bối cảnh Production (15 phút)

Trong PySpark Structured Streaming, API `writeStream.foreachBatch(fn)` ép buộc hàm callback `fn` chỉ được nhận đúng 2 tham số: `(micro_batch_df, batch_id)`. Tuy nhiên, bên trong mỗi micro-batch ta lại cần:
- Tên bảng đích (`table_name`) và hàm mở handle bảng (`open_table_fn`) — được **cache** giữa các micro-batch để tránh gọi S3 metadata lặp lại.
- Gọi `.persist()` trước khi xử lý, và **bắt buộc gọi `.unpersist()` trong `finally:`** dù batch thành công hay ném lỗi, tránh rò rỉ Executor RAM.
- Khi ghi lỗi (`except:`), phải **xóa cache handle** bị stale để batch sau nạp lại snapshot mới.

---

## 2. 📋 Yêu cầu kỹ thuật (Acceptance Criteria)

Mở [`starter/batch_factory.py`](starter/batch_factory.py) và hoàn thiện `create_batch_processor(...)`:
1. Trả về một closure `process_batch(batch_df, batch_id)`.
2. Gọi `batch_df.persist()` đầu hàm và **luôn gọi `batch_df.unpersist()`** trong `finally:` (kể cả khi batch rỗng hoặc khi `write_fn` raise exception).
3. Nếu `batch_df.is_empty()` là `True`, return sớm và **không** gọi `open_table_fn` hay `write_fn`.
4. Cache kết quả `open_table_fn(table_name)` trong dict nội bộ của closure để chỉ mở handle **1 lần** cho nhiều micro-batch liên tiếp.
5. Nếu `write_fn(handle, batch_df, batch_id)` raise exception: **evict (xóa)** handle khỏi cache rồi re-raise exception.
6. Chạy test kiểm tra:
   ```bash
   pytest curriculum/phase-1-python-and-pyspark/week-01-python-for-de/day-02-closures-and-batch-factory/tests -v
   ```

---

## 3. 🧠 Active Recall (15 phút sau khi code xong)
1. **Tại sao dict `_handle_cache = {}` bên ngoài `process_batch` có thể bị sửa đổi bên trong `process_batch` mà không cần từ khóa `nonlocal`?**
2. **Nếu quên đặt `unpersist()` trong `finally:` (chỉ đặt cuối khối `try:`), điều gì sẽ xảy ra với cụm Spark sau vài giờ bị lỗi mạng S3?**
