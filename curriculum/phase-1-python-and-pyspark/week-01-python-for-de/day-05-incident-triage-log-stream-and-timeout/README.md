# 🚨 Day 05 (Incident Triage Lab): Fixing Blind `subprocess.run` Timeouts

> **Phase:** 1 · **Week:** W01 · **Time Budget:** 60–90 mins · **Type:** Incident Triage & Refactor Lab  
> **Skills:** `subprocess.Popen`, Concurrent Stdout/Stderr Reader Threads, Timeout Cleanup, Observability

---

## 1. 🔥 Sự cố Production giả lập (15 phút)

Một DAG Airflow chạy `dbt run` bằng `subprocess.run(..., capture_output=True, timeout=3600)`. Sau đúng 60 phút, task chết với lỗi `TimeoutExpired` — nhưng **Airflow log trắng trơn, không in ra dù chỉ 1 dòng output từ `dbt`**! Đội ngũ trực on-call hoàn toàn mù thông tin, không biết model nào đã chạy xong và model nào đang bị treo.

**Nhiệm vụ của bạn**: Refactor [`starter/command_runner.py`](starter/command_runner.py) từ `subprocess.run(capture_output=True)` sang **`subprocess.Popen` + 2 reader threads** để:
1. Gọi callback `on_line(stream_name, line)` **ngay lập tức** mỗi khi tiến trình con in ra 1 dòng (`stdout` hoặc `stderr`).
2. Nếu tiến trình chạy quá `timeout_sec`, kill tiến trình con (`process.kill()`), đợi reader threads đọc nốt phần log đã kịp in ra, và trả về `CommandResult(timed_out=True, ...)` chứa đầy đủ log đã thu được trước khi timeout!

---

## 2. 📋 Yêu cầu kỹ thuật (Acceptance Criteria)

Mở [`starter/command_runner.py`](starter/command_runner.py) và sửa hàm `run_streaming_command(...)`:
1. Dùng `subprocess.Popen(..., stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)`.
2. Tạo 2 daemon thread đọc đồng thời `process.stdout` và `process.stderr` (tránh OS pipe buffer deadlock!), gọi `on_line("stdout" | "stderr", stripped_line)` ngay khi đọc được.
3. Dùng `process.wait(timeout=timeout_sec)`; nếu dính `subprocess.TimeoutExpired`, gọi `process.kill()`, `process.wait()`, join 2 reader threads, và trả về `CommandResult(returncode=-1, stdout=..., stderr=..., timed_out=True)`.
4. Chạy test kiểm tra:
   ```bash
   pytest curriculum/phase-1-python-and-pyspark/week-01-python-for-de/day-05-incident-triage-log-stream-and-timeout/tests -v
   ```

---

## 3. 🧠 Active Recall (15 phút sau khi code xong)
1. **Tại sao dùng 1 thread đọc tuần tự `stdout` xong mới đọc `stderr` trên `Popen` có thể gây treo chết (pipe deadlock)?**
2. **Khi `dbt run` bị kill giữa chừng trên SQL Server, tại sao `materialized='table'` có thể làm mất sạch dữ liệu bảng đích nếu Airflow tự retry?**
