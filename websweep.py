import socket
import requests
import urllib3
from concurrent.futures import ThreadPoolExecutor
import time
import sys
import threading  # NEW: We import the threading module for the lock

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 1. THE DISCLAIMER BANNER ---
print("\033[91m" + "="*55)
print("                 WEB SWEEP v1.0")
print("         Custom Network Reconnaissance Tool")
print("="*55 + "\033[0m")
print("DISCLAIMER: This tool is for educational purposes and")
print("authorized testing only. Scanning networks without")
print("explicit permission is illegal.")
print("-" * 55)

agree = input("Do you have authorization to scan this network? (y/n): ")
if agree.lower() != 'y':
    print("\033[91m[!] Exiting...\033[0m")
    sys.exit()

# --- 2. THE SETUP ---
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

network_prefix = input("\nEnter network prefix (e.g., 192.168.56): ")
web_ports = [80, 443, 8080, 8000, 3000, 8443]
targetFullIp = [f"{network_prefix}.{i}" for i in range(1, 255)]

output_file = "web_servers_found.txt"
with open(output_file, "w") as f:
    f.write(f"--- Web Sweep Results for {network_prefix}.0/24 ---\n\n")

print(f"\n[+] Sweeping {network_prefix}.1 - 254 for Web Servers...\n")

# --- 3. THE THREAD LOCK ---
# This creates a lock. Only one thread can hold this lock at a time.
print_lock = threading.Lock()

def check_web_server(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3) 
        result = s.connect_ex((ip, port))
        s.close()

        if result == 0:
            protocol = "https" if port in [443, 8443] else "http"
            url = f"{protocol}://{ip}:{port}"
            
            response = requests.get(url, headers=headers, timeout=1, verify=False)
            
            title = "Unknown"
            if "<title>" in response.text.lower():
                start = response.text.lower().find("<title>") + 7
                end = response.text.lower().find("</title>")
                title = response.text[start:end].strip()
                if len(title) > 30: title = title[:30] + "..."

            server_header = response.headers.get("Server", "Hidden")

            # --- 4. USING THE LOCK ---
            # 'with print_lock:' means "Wait here until no one else is printing."
            with print_lock:
                print(f"\n\033[92m[+] FOUND:\033[0m {url}")
                print(f"    \033[94mTitle:\033[0m  {title}")
                print(f"    \033[94mServer:\033[0m {server_header}")
                print(f"    \033[94mStatus:\033[0m {response.status_code}")
                
                with open(output_file, "a") as f:
                    f.write(f"URL: {url}\nTitle: {title}\nServer: {server_header}\n\n")
            
    except Exception:
        pass 

start_time = time.time()

with ThreadPoolExecutor(max_workers=250) as executor:
    for ip in targetFullIp:
        for port in web_ports:
            executor.submit(check_web_server, ip, port)
        
        sys.stdout.write(".")
        sys.stdout.flush()

print(f"\n\n\033[93m[*] Sweep complete in {time.time() - start_time:.2f} seconds.\033[0m")
print(f"\033[93m[*] Results saved to {output_file}\033[0m")
