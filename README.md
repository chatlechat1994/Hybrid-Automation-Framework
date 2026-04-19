[![Fintech CI Pipeline](https://github.com/chatlechat1994/Hybrid-Automation-Framework/actions/workflows/python_tests.yml/badge.svg)](https://github.com/chatlechat1994/Hybrid-Automation-Framework/actions/workflows/python_tests.yml)
# 🏦 Hybrid Automation Framework: Fintech Data Integrity

This repository demonstrates a backend automation framework focused on **database integrity** and **transaction auditing**.

> **Project Context:**  
> This is my first project in the Financial Technology (Fintech) space.  
> The goal was to apply my existing automation skills to systems that require strict data consistency and validation, such as banking applications.

---

## 🔍 Overview

The framework simulates a basic banking system where money transfers must occur without data loss.

It ensures that:
- The total balance across the system remains constant  
- Transactions fail safely hen funds are insufficient  
- System state is not corrupted during errors  

---

## ⚙️ Tech Stack

- **Language:** Python 3.13  
- **Database:** SQLite (via SQLAlchemy)  
- **Testing:** Pytest  
- **Logging:** Python Logging Module  

---

## 🚀 Key Features

- **Clean Slate Protocol**  
  Uses Pytest fixtures to reset the database before every test and clears file locks using `engine.dispose()`, ensuring consistent and repeatable results.

- **Transaction Auditing**  
  Generates an `audit.log` file with timestamps and log levels to simulate real-world audit trails.

- **Integrity Validation**  
  Ensures that total system balance remains unchanged:
  ```
  Total Balance = Account A + Account B
  ```

---

## 📁 Project Structure

```text
Hybrid-Automation-Framework/
├── db/
│   └── database_manager.py
├── tests/
│   └── test_db_integrity.py
├── audit.log
├── fintech_bank.db
├── requirements.txt
└── README.md
```

---

## ▶️ Running the Tests

### 1. Activate Virtual Environment
```powershell
.\venv\Scripts\activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Run Test Suite
```powershell
python -m pytest -v -s
```

---

## 🧾 Sample Audit Log

```text
2026-04-19 22:19:51 - INFO - STARTING AUDIT: Transferring $100.0 from ID:1 to ID:2
2026-04-19 22:19:51 - INFO - AUDIT PASSED: Balance integrity verified.
2026-04-19 22:19:51 - WARNING - SECURITY AUDIT: Attempting high-value transfer of $5000.0
2026-04-19 22:19:51 - INFO - AUDIT PASSED: System correctly blocked insufficient funds.
```

---

## 🧠 Lessons Learned

### 🪟 Windows File Locking
Resolved `WinError 32 (PermissionError)` by properly disposing database connections:
```python
engine.dispose()
```

### 🔄 ORM State Consistency
Used:
```python
session.expire_all()
```
to ensure tests validate against the actual database state rather than cached objects.

### 🛡️ Defensive Setup
Implemented a reliable setup/teardown cycle using:
- `os` for file handling  
- `time.sleep()` to handle filesystem delays  

---