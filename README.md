# WebSweep

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20Termux-lightgrey)
![Status](https://img.shields.io/badge/Status-Active-success)

A custom, multithreaded Python-based network scanner designed to sweep subnets, identify open web ports, and extract HTTP server banners and HTML titles.

<img width="776" height="183" alt="Screenshot 2026-11-20 140556" src="https://github.com/user-attachments/assets/e202d5bc-78b4-47dc-b8d8-aae400c566a7" />


## 📖 Description
WebSweep is a lightweight reconnaissance tool built from scratch for authorized penetration testing and educational purposes. It allows security researchers to quickly map out web services running on a network by checking multiple common web ports and scraping metadata directly from the HTTP responses.

## ✨ Features
* **⚡ Multithreaded Engine:** Utilizes `ThreadPoolExecutor` to scan multiple IPs and ports simultaneously, making network sweeps incredibly fast.
* **🌐 Multi-Port Scanning:** Automatically checks common web ports (80, 443, 3000, 8000, 8080, 8443) rather than relying on a single default port.
* **🥷 Stealth Mode:** Injects a standard Windows Chrome `User-Agent` header to bypass basic firewall blocks and avoid easy detection.
* **🔍 Deep Recon:** Extracts the HTML `<title>`, the `Server` header (e.g., Apache, Nginx), and bypasses SSL certificate warnings for HTTPS.
* **💾 Automated Logging:** Automatically saves all discovered web servers and their headers to a `web_servers_found.txt` file for easy reporting.

## 🚀 Installation & Usage
1. Clone the repo: `git clone https://github.com/B1i1-95CHIB/websweep.git`
2. Install dependencies: `pip install requests beautifulsoup4`
3. Run the tool: `python3 websweep.py`

## ⚠️ Disclaimer
This tool is provided for educational purposes and authorized security testing only. Do not use this tool against networks you do not own or have explicit permission to test. The author is not responsible for any misuse or damage caused by this program.
