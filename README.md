# NetPulse - Cyber Defense & Load Simulator

![NetPulse](https://img.shields.io/badge/status-educational-red?style=flat-square)
![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

> ⚠️ **WARNING:** This tool is strictly for educational and internal network stress-testing purposes only. Misuse of this software may be illegal in your country. Always have proper authorization before scanning or simulating traffic to any target.

---

## 🌀 What is NetPulse?

NetPulse is a terminal-based CLI simulation tool that can:
- Perform traffic stress simulations (UDP, TCP, HTTP flood, SYN flood)
- Provide basic reconnaissance (open ports, PTR lookup, VPN flagging)
- Run in **English** or **Bahasa Melayu**

It’s ideal for:
- Cybersecurity students & educators
- Pentesters in a lab environment
- Red team simulation under proper authorization

---

## ✨ Features

- [x] Language Selection: English / Bahasa Melayu
- [x] Bilingual CLI banner
- [x] Port Scanner
- [x] Reverse DNS (PTR lookup)
- [x] UDP flood simulation
- [x] TCP flood simulation
- [x] HTTP flood simulation
- [x] SYN flood simulation (requires root)
- [x] VPN flag (offline logic placeholder)
- [x] Basic GeoIP stub
- [x] Report generation before attack
- [x] Multi-threaded simulation
- [x] Works offline (no API required)
- [x] Supports Linux and other UNIX systems
- [ ] Windows support planned

---

## 🚀 Usage

### 📦 Requirements

- Python 3.6+
- `scapy` library

Install with:

```bash
pip install scapy
```
---
To start the program use
```bash
sudo python3 netpulse.py
```
---
### 🧾 Command-line Flags

| Flag         | Description                                | Default     |
|--------------|--------------------------------------------|-------------|
| `--target`   | Target IP address                          | **Required**|
| `--port`     | Target port                                | `80`        |
| `--method`   | Attack method: `udp`, `tcp`, `http`, `syn` | `udp`       |
| `--time`     | Duration of attack in seconds              | `30`        |
| `--threads`  | Number of parallel threads                 | `10`        |

