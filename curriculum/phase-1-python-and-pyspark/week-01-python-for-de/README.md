# 📦 Week 01: Python Production Foundations for Data Engineering

> **Phase 1: Python & PySpark** · **Time Budget:** 60–90 mins/day · **Goal:** Master the exact Python patterns used in production streaming and batch pipelines (`@dataclass` control planes, closures, `try/finally` memory hygiene, OCC retries, daemon threads, and non-blocking `Popen` log streaming).

| Day | Lab | Type | Key Python Concepts |
| :---: | :--- | :---: | :--- |
| **Day 01** | [Dataclass Config Registry](day-01-dataclass-config-registry/README.md) | 🛠️ Build | `@dataclass`, `@property`, YAML validation, `Optional[T]` typing |
| **Day 02** | [Closures & Batch Processor Factory](day-02-closures-and-batch-factory/README.md) | 🛠️ Build | Closures, mutable enclosing cache, `try/except/finally` resource hygiene |
| **Day 03** | [OCC Conflict Retry & Backoff](day-03-retry-and-occ-backoff/README.md) | 🛠️ Build | Higher-order functions, selective exception classification, snapshot reload |
| **Day 04** | [Daemon Watchdog & Threading](day-04-daemon-watchdog-and-threading/README.md) | 🛠️ Build | `threading.Thread(daemon=True)`, `threading.Event`, grace period logic |
| **Day 05** | [Incident Lab: Blind Subprocess Timeout](day-05-incident-triage-log-stream-and-timeout/README.md) | 🚨 Incident | `subprocess.Popen`, concurrent stdout/stderr reader threads, timeout handling |
| **Day 06** | [Week 1 Spaced Repetition & Code-from-Memory](day-06-spaced-repetition-and-review/README.md) | 🔁 Review | Active recall & rebuild without looking at `solution/` |
