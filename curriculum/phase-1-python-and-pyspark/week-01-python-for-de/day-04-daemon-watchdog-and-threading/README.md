# 🛠️ Day 04: Daemon Watchdog & Thread-Safe Grace Period

> **Phase:** 1 · **Week:** W01 · **Time Budget:** 60–90 mins · **Type:** Build Lab  
> **Skills:** `threading.Thread(daemon=True)`, `threading.Event`, Monotonic Clocks, Self-Healing Process Design

---

## 1. 🎯 Bối cảnh Production (15 phút)

Trên cụm Spark Standalone, đôi khi toàn bộ Worker/Executor bị mất kết nối mạng hoặc OOM, nhưng tiến trình **Python Driver vẫn sống** (trạng thái Zombie Driver — không xử lý bản ghi nào nhưng Docker Swarm vẫn thấy container `running` nên không restart).

Giải pháp là chạy một **Background Daemon Watchdog**:
- Cứ mỗi `check_interval_sec`, gọi `get_active_cores_fn()`.
- Nếu `cores < min_cores` liên tục vượt quá `grace_period_sec`, gọi `on_unhealthy()` (trên prod sẽ thoát tiến trình để Docker Swarm tự restart sạch).
- Nếu `cores` phục hồi kịp trong `grace_period_sec`, bộ đếm unhealthy phải được **reset về `None`**.
- Sử dụng `threading.Event` thay vì `time.sleep()` thô để có thể tắt thread ngay lập tức khi shutdown.

---

## 2. 📋 Yêu cầu kỹ thuật (Acceptance Criteria)

Mở [`starter/watchdog.py`](starter/watchdog.py) và hoàn thiện class `ExecutorWatchdog`:
1. `evaluate_once(now: float) -> bool`:
   - Kiểm tra `cores = self._get_active_cores()`.
   - Nếu `cores >= self._min_cores`: reset `self._unhealthy_since = None`, trả về `True` (healthy).
   - Nếu `cores < self._min_cores`:
     - Nếu `self._unhealthy_since is None`: gán `self._unhealthy_since = now`.
     - Nếu `now - self._unhealthy_since >= self._grace_period_sec`: gọi `self._on_unhealthy()` đúng 1 lần và đánh dấu dừng (`self._stop_event.set()`), trả về `False`.
2. `start()` và `stop()`:
   - Chạy vòng lặp nền trong `threading.Thread(daemon=True)` dùng `self._stop_event.wait(self._check_interval_sec)`.
3. Chạy test kiểm tra:
   ```bash
   pytest curriculum/phase-1-python-and-pyspark/week-01-python-for-de/day-04-daemon-watchdog-and-threading/tests -v
   ```

---

## 3. 🧠 Active Recall (15 phút sau khi code xong)
1. **Tại sao nên dùng `time.monotonic()` thay vì `time.time()` để đo khoảng thời gian `grace_period`?**
2. **Tại sao `stop_event.wait(interval)` tốt hơn `time.sleep(interval)` trong vòng lặp daemon thread?**
