# 🔁 Day 06: Week 1 Spaced Repetition & Code-from-Memory

> **Phase:** 1 · **Week:** W01 · **Time Budget:** 60–90 mins · **Type:** Spaced Repetition Review

---

## 1. 🧠 Code-from-Memory Challenge (45 phút)
Chọn **2 trong 5 bài** bạn thấy khó nhất trong Tuần 1, reset file `starter/` về ban đầu (không nhìn `solution/`), và tự viết lại sạch sẽ cho đến khi `pytest` xanh 100%:
- [ ] Day 01: `TableConfig` + `load_table_registry`
- [ ] Day 02: `create_batch_processor` closure + `try/finally`
- [ ] Day 03: `execute_with_occ_retry` + reload hook
- [ ] Day 04: `ExecutorWatchdog` + `threading.Event`
- [ ] Day 05: `run_streaming_command` (`Popen` + concurrent reader threads)

---

## 2. 🗣️ Explain-Out-Loud Drill (English Practice — 20 phút)
Tự nói thành tiếng bằng tiếng Anh (30–60 giây mỗi câu) như đang trả lời trong một buổi architecture review:
1. *"Why do we use a closure factory with `try/finally: unpersist()` inside Spark's `foreachBatch`?"*
2. *"Why did our batch runner lose all dbt logs on timeout, and how does `subprocess.Popen` with two reader threads fix it?"*
3. *"What happens if an OCC retry loop doesn't reload the table snapshot before retrying?"*

---

## 3. 📝 Cập nhật Progress Log (5 phút)
Đánh dấu hoàn thành Tuần 1 và lên lịch ôn `+7d` / `+21d` trong [`progress/spaced_repetition_log.md`](../../../progress/spaced_repetition_log.md).
