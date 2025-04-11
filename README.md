# 📡 Network Scanner Tool

## 📝 Overview

This is a multi-threaded **network scanner tool** written in Python that can:

- 🔍 Ping a range of IPs to check if they're reachable.
- 🌐 Resolve hostnames of reachable IPs.
- 🛡️ Scan for open TCP ports (common ports or full range).
- 📄 Optionally export results to a CSV file.

It is fast, user-friendly, and works across Windows, Linux, and macOS.

---

## 🚀 Features

✅ Fast, concurrent ping sweep using threads  
✅ Hostname resolution  
✅ Optional port scanning (common or full 1–65535 range)  
✅ Real-time colored terminal output using `colorama`  
✅ Export results to a `.csv` file  
✅ Cross-platform compatibility

---

## ▶️ How to Run

Follow these steps to use the tool:

### 1. Install Requirements

Make sure you have Python 3.6+ installed. Then install `colorama`:

```bash
pip install colorama
```

---

### 2. Run the Script

```bash
python network_scanner.py
```

---

### 3. Choose Scan Type

You'll be prompted to choose a scan mode:

```
1. Ping & Hostname Test
2. Ping, Hostname & Port Scan Test
```

- Choose `1` for a quick scan.
- Choose `2` for full scan including port scanning.

If you select option 2, you will also be asked:

```
Scan ALL ports (1-65535)? [y/N]
```

- Type `y` to scan all ports (longer scan).
- Press Enter or type `n` to scan only common ports (faster).

---

### 4. Enter Base IP

Example prompt:
```
Enter base IP (e.g., 192.168.1) or press Enter for default [172.16.172]:
```

- Enter `192.168.1`, or
- Press Enter to use the default `172.16.172`.

---

### 5. Enter Start and End Range

You'll then enter the last octets for the range:

```
Enter start IP (last octet, 0-255): 10
Enter end IP (last octet, 0-255): 20
```

This scans from `192.168.1.10` to `192.168.1.20`.

---

### 6. View Live Results

As the scan runs, you'll see:

- ✅ Reachable IPs
- 🌐 Hostnames
- 🔓 Open ports found (if any)

---

### 7. Export Results (Optional)

At the end, you’ll be asked:

```
Do you want to export results to CSV? (y/n)
```

- Type `y` to save results as `scan_result_1.csv`, `scan_result_2.csv`, etc.
- Type `n` to skip exporting.

---

## 📂 Sample CSV Output

| IP Address     | Hostname          | Open Ports       |
|----------------|-------------------|------------------|
| 192.168.1.11   | my-printer.local  | 80, 9100         |
| 192.168.1.13   | Hostname not found| None             |

---


## 🛡️ Disclaimer

Use this tool **only on networks you own or have permission to scan.** Unauthorized scanning may be illegal in your jurisdiction.

---

## 📜 License

This project is open-source. Feel free to modify and use with proper credit.

---