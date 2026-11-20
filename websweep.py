#!/usr/bin/env python3
import socket
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

# --- CONFIGURATION ---
ip_prefix = input("Enter the network prefix (e.g., 192.168.1): ")
start = int(input("Enter starting IP: "))
stop = int(input("Enter ending IP: "))

# The most common web ports
web_ports = [80, 443, 3000, 8000, 8080, 8443]

ips = [f"{ip_prefix}.{i}" for i in range(start, stop + 1)]
nos = len(ips)

found_websites = []

def scan_ip(ip):
    # Loop through EVERY port in our list for this IP
    for port in web_ports:
        phone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        phone.settimeout(1.0) # 1 second timeout per port
        result = phone.connect_ex((ip, port))
        phone.close()
        
        # If the port is closed, skip to the next port
        if result != 0:
            continue 

        # Determine protocol based on port
        protocol = "https" if port in [443, 8443] else "http"
        url = f"{protocol}://{ip}:{port}"

        try:
            # Add a fake Chrome browser header (Stealth)
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, timeout=3, verify=False, headers=headers)
            
            server_header = response.headers.get('Server', 'Unknown')
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string.strip() if soup.title else "No Title"
            
            output = f"URL: {url} | Server: {server_header} | Title: {title}"
            
            print(f"[+] Found: {output}")
            found_websites.append(output)
                
        except requests.exceptions.RequestException:
            # Sometimes a port is open but it's not a website (like an SSH port or a database)
            # We just ignore it and move on
            pass 

print(f"[*] Starting MULTITHREADED scan on {nos} hosts across {len(web_ports)} ports...")

with ThreadPoolExecutor(max_workers=30) as executor: # Increased workers to 30 for speed
    executor.map(scan_ip, ips)

# --- SAVE TO FILE ---
print(f"\n[*] Scan complete. Found {len(found_websites)} web servers.")

if len(found_websites) > 0:
    filename = "web_servers_found.txt"
    with open(filename, "w") as file:
        for site in found_websites:
            file.write(site + "\n")
    print(f"[+] Results successfully saved to {filename}")
else:
    print("[-] No web servers found.")
