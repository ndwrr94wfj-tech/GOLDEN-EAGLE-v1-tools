#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import socket
import urllib.request
import urllib.parse
import hashlib
import base64
import random
import string
from datetime import datetime

# ANSI Colors - Gold/Black gradient theme
R = '\033[0m'
BOLD = '\033[1m'
DIM = '\033[2m'

# Gold gradient
GOLD_DARKEST = '\033[38;5;94m'
GOLD_DARK = '\033[38;5;130m'
GOLD_MED = '\033[38;5;136m'
GOLD_LIGHT = '\033[38;5;178m'
GOLD_BRIGHT = '\033[38;5;220m'
GOLD_WHITE = '\033[38;5;226m'

CYAN = '\033[38;5;51m'
RED = '\033[38;5;196m'
GREEN = '\033[38;5;82m'
GRAY = '\033[38;5;240m'
MAGENTA = '\033[38;5;201m'
BLUE = '\033[38;5;27m'

def clear():
    os.system('clear')

def gradient_text(text):
    lines = text.split('\n')
    result = []
    for i, line in enumerate(lines):
        if line.strip():
            if i % 4 == 0:
                result.append(f"{GOLD_DARKEST}{line}{R}")
            elif i % 4 == 1:
                result.append(f"{GOLD_DARK}{line}{R}")
            elif i % 4 == 2:
                result.append(f"{GOLD_MED}{line}{R}")
            else:
                result.append(f"{GOLD_LIGHT}{line}{R}")
        else:
            result.append(line)
    return '\n'.join(result)

def banner():
    clear()
    
    ascii_art = """________ ________  .____     ________  ___________ _______        ___________   _____    ________.____     ___________
 /  _____/ \\_____  \\ |    |    \\______ \\ \\_   _____/ \\      \\       \\_   _____/  /  _  \\  /  _____/|    |    \\_   _____/
/   \\  ___  /   |   \\|    |     |    |  \\ |    __)_  /   |   \\       |    __)_  /  /_\\  \\/   \\  ___|    |     |    __)_ 
\\    \\_\\  \\/    |    \\    |___  |    `   \\|        \\/    |    \\      |        \\/    |    \\    \\_\\  \\    |___  |        \\
 \\______  /\\_______  /_______ \\/_______  /_______  /\\____|__  /     /_______  /\\____|__  /\\______  /_______ \\/_______  /
        \\/         \\/        \\/        \\/        \\/         \\/              \\/         \\/        \\/        \\/        \\/"""

    print(gradient_text(ascii_art))
    
    print(f"""
{GOLD_MED}╔══════════════════════════════════════════════════════════════════════════╗{R}
{GOLD_MED}║{R}  {GOLD_BRIGHT}▓▒░ ADVANCED OSINT INTELLIGENCE SUITE ░▒▓{R}                              {GOLD_MED}║{R}
{GOLD_MED}║{R}                                                                          {GOLD_MED}║{R}
{GOLD_MED}║{R}  {CYAN}Version:{R} 3.0.0-PLATINUM                  {CYAN}Platform:{R} macOS/Unix           {GOLD_MED}║{R}
{GOLD_MED}║{R}  {CYAN}Author:{R}  {BOLD}@azerkash{R}                      {CYAN}Status:{R}   {GREEN}OPERATIONAL{R}        {GOLD_MED}║{R}
{GOLD_MED}║{R}                                                                          {GOLD_MED}║{R}
{GOLD_MED}╚══════════════════════════════════════════════════════════════════════════╝{R}
""")

def log(msg, color=GOLD_LIGHT):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"{GRAY}[{timestamp}]{R} {color}{msg}{R}")

def success(msg):
    log(f"[✓] {msg}", GREEN)

def error(msg):
    log(f"[✗] {msg}", RED)

def warn(msg):
    log(f"[!] {msg}", GOLD_MED)

def info(msg):
    log(f"[i] {msg}", CYAN)

def loading(text, duration=1):
    chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    for i in range(duration * 10):
        print(f"\r{GOLD_BRIGHT}{chars[i % len(chars)]}{R} {GOLD_LIGHT}{text}...", end='', flush=True)
        time.sleep(0.1)
    print(f" {GREEN}DONE{R}")

def progress_bar(current, total, prefix='Progress'):
    percent = 100 * (current / float(total))
    filled = int(30 * current // total)
    bar = '█' * filled + '░' * (30 - filled)
    print(f'\r{GOLD_MED}{prefix}:{R} |{GOLD_BRIGHT}{bar}{R}| {CYAN}{percent:.1f}%{R}', end='', flush=True)
    if current == total:
        print()

# ==================== OSINT MODULES ====================

class IPModule:
    """Advanced IP Intelligence"""
    def menu(self):
        print(f"\n{GOLD_MED}╔══════════════════ IP INTELLIGENCE ═══════════════════╗{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[1]{R} Standard IP Lookup (Geolocation)                    {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[2]{R} Advanced Port Scan (Top 100 ports)                    {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[3]{R} IP Reputation Check                                 {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[4]{R} My IP Information                                   {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[0]{R} Back to Main Menu                                   {GOLD_MED}║{R}")
        print(f"{GOLD_MED}╚══════════════════════════════════════════════════════╝{R}")
        
        choice = input(f"\n{GOLD_BRIGHT}[IP_MODULE]{R} Select: ").strip()
        
        if choice == '1':
            self.standard_lookup()
        elif choice == '2':
            self.port_scan()
        elif choice == '3':
            self.reputation_check()
        elif choice == '4':
            self.my_ip()
    
    def standard_lookup(self, ip=None):
        if not ip:
            ip = input(f"{CYAN}[TARGET IP]{R}> ").strip()
        if not ip:
            return {}
        
        log(f"Querying databases for: {ip}")
        loading("Connecting to ip-api.com", 2)
        
        try:
            req = urllib.request.Request(
                f"http://ip-api.com/json/{ip}?fields=status,message,continent,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,isp,org,as,asname,reverse,mobile,proxy,hosting",
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                
                if data.get('status') == 'success':
                    self.display_ip_results(data)
                    return data
                else:
                    error(f"API Error: {data.get('message', 'Unknown')}")
        except Exception as e:
            error(f"Connection failed: {e}")
        return {}
    
    def display_ip_results(self, data):
        print(f"\n{GOLD_BRIGHT}╔══════════════════════════════════════════════════════════╗{R}")
        print(f"{GOLD_BRIGHT}║{R}              {BOLD}IP INTELLIGENCE REPORT{R}                     {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}╠══════════════════════════════════════════════════════════╣{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} IP Address:    {CYAN}{data.get('query', 'N/A'):<45}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} Country:       {CYAN}{data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')}){'':<32}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} Region:        {CYAN}{data.get('regionName', 'N/A')} ({data.get('region', 'N/A')}){'':<29}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} City:          {CYAN}{data.get('city', 'N/A')}{'':<44}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} Coordinates:   {CYAN}{data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}{'':<36}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} Timezone:      {CYAN}{data.get('timezone', 'N/A'):<44}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}╠══════════════════════════════════════════════════════════╣{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} ISP:           {CYAN}{data.get('isp', 'N/A'):<44}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} Organization:  {CYAN}{data.get('org', 'N/A'):<44}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}▸{R} AS:            {CYAN}{data.get('as', 'N/A'):<44}{GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}╚══════════════════════════════════════════════════════════╝{R}")
        
        flags = []
        if data.get('mobile'): flags.append(f"{GOLD_MED}[📱 MOBILE]{R}")
        if data.get('proxy'): flags.append(f"{RED}[🛡️ PROXY/VPN]{R}")
        if data.get('hosting'): flags.append(f"{RED}[☁️ HOSTING]{R}")
        
        if flags:
            print(f"\nRisk Assessment: {' '.join(flags)}")
        
        print(f"\n{GOLD_MED}External Tools:{R}")
        print(f"  {GRAY}•{R} https://www.abuseipdb.com/check/{data.get('query')}")
        print(f"  {GRAY}•{R} https://ipinfo.io/{data.get('query')}")
    
    def port_scan(self):
        target = input(f"{CYAN}[TARGET IP]{R}> ").strip()
        if not target:
            return
        
        log(f"Starting port scan on: {target}")
        
        ports = {
            21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP', 53: 'DNS',
            80: 'HTTP', 110: 'POP3', 143: 'IMAP', 443: 'HTTPS', 445: 'SMB',
            3306: 'MySQL', 3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC',
            8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 9200: 'Elasticsearch'
        }
        
        open_ports = []
        print(f"\n{GOLD_MED}Scanning {len(ports)} ports...{R}\n")
        
        total = len(ports)
        for i, (port, service) in enumerate(ports.items(), 1):
            progress_bar(i, total, 'Scanning')
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.3)
                if sock.connect_ex((target, port)) == 0:
                    open_ports.append((port, service))
                sock.close()
            except:
                pass
        
        print()
        if open_ports:
            print(f"\n{GREEN}[✓] Found {len(open_ports)} open ports:{R}")
            for port, service in open_ports:
                print(f"  {GREEN}●{R} Port {port}/{service}")
        else:
            warn("No open ports found")
    
    def reputation_check(self):
        ip = input(f"{CYAN}[IP TO CHECK]{R}> ").strip()
        if ip:
            print(f"\n{GOLD_MED}Reputation Check Links:{R}")
            print(f"  {GRAY}•{R} https://www.abuseipdb.com/check/{ip}")
            print(f"  {GRAY}•{R} https://www.virustotal.com/gui/ip-address/{ip}")
    
    def my_ip(self):
        log("Detecting your IP...")
        try:
            req = urllib.request.Request('http://ip-api.com/json/?fields=query')
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode('utf-8'))
                print(f"\n{GREEN}Your IP: {data.get('query')}{R}")
                self.standard_lookup(data.get('query'))
        except:
            error("Could not detect IP")

class UsernameModule:
    """Username Intelligence"""
    def menu(self):
        print(f"\n{GOLD_MED}╔════════════════ USERNAME INTELLIGENCE ═══════════════╗{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[1]{R} Single Username Check                              {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[2]{R} Username Variations Generator                      {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[3]{R} Email Pattern Generator                            {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[0]{R} Back to Main Menu                                  {GOLD_MED}║{R}")
        print(f"{GOLD_MED}╚══════════════════════════════════════════════════════╝{R}")
        
        choice = input(f"\n{GOLD_BRIGHT}[USER_MODULE]{R} Select: ").strip()
        
        if choice == '1':
            self.single_check()
        elif choice == '2':
            self.variations()
        elif choice == '3':
            self.email_patterns()
    
    def single_check(self):
        username = input(f"{CYAN}[USERNAME]{R}> ").strip().lower()
        if not username:
            return
        
        log(f"Analyzing username: {username}")
        loading("Generating links", 2)
        
        platforms = {
            "Instagram": f"https://www.instagram.com/{username}/",
            "Twitter/X": f"https://twitter.com/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "GitHub": f"https://github.com/{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "YouTube": f"https://www.youtube.com/@{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
        }
        
        print(f"\n{GOLD_BRIGHT}╔═══════════════ USERNAME: @{username} ═══════════════╗{R}")
        for name, url in platforms.items():
            print(f"{GOLD_BRIGHT}║{R} {GRAY}•{R} {name:<12} {CYAN}{url}{R}")
        print(f"{GOLD_BRIGHT}╚══════════════════════════════════════════════════════╝{R}")
        
        print(f"\n{GOLD_MED}Check Tools:{R}")
        print(f"  {GRAY}•{R} https://namechk.com/{username}")
        print(f"  {GRAY}•{R} https://whatsmyname.app/?username={username}")
    
    def variations(self):
        username = input(f"{CYAN}[BASE USERNAME]{R}> ").strip()
        if not username:
            return
        
        variations = [
            username, username.lower(), username.upper(),
            f"{username}123", f"{username}2024", f"{username}official",
            f"{username}_official", f"real{username}", f"_{username}",
            f"{username}_", f"{username}.{username}",
        ]
        
        print(f"\n{GOLD_BRIGHT}Variations:{R}")
        for v in variations:
            print(f"  {GRAY}•{R} {v}")

    def email_patterns(self):
        username = input(f"{CYAN}[USERNAME]{R}> ").strip()
        if not username:
            return
        
        domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com"]
        print(f"\n{GOLD_BRIGHT}Possible Emails:{R}")
        for domain in domains:
            print(f"  {GRAY}•{R} {username}@{domain}")

class CryptoModule:
    """Cryptography & Hashing Tools"""
    def menu(self):
        print(f"\n{GOLD_MED}╔══════════════════ CRYPTO TOOLS ══════════════════════╗{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[1]{R} Hash Generator (MD5, SHA1, SHA256)                 {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[2]{R} Base64 Encode/Decode                              {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[3]{R} Password Generator                                {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[4]{R} JWT Token Decoder                                 {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[0]{R} Back to Main Menu                                 {GOLD_MED}║{R}")
        print(f"{GOLD_MED}╚══════════════════════════════════════════════════════╝{R}")
        
        choice = input(f"\n{GOLD_BRIGHT}[CRYPTO]{R} Select: ").strip()
        
        if choice == '1':
            self.hash_gen()
        elif choice == '2':
            self.base64_tool()
        elif choice == '3':
            self.pass_gen()
        elif choice == '4':
            self.jwt_decode()
    
    def hash_gen(self):
        text = input(f"{CYAN}[TEXT TO HASH]{R}> ").strip()
        if not text:
            return
        
        print(f"\n{GOLD_BRIGHT}╔══════════════════ HASH RESULTS ═══════════════════╗{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}MD5:{R}    {CYAN}{hashlib.md5(text.encode()).hexdigest()}{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}SHA1:{R}   {CYAN}{hashlib.sha1(text.encode()).hexdigest()}{R}")
        print(f"{GOLD_BRIGHT}║{R} {GOLD_MED}SHA256:{R} {CYAN}{hashlib.sha256(text.encode()).hexdigest()}{R}")
        print(f"{GOLD_BRIGHT}╚═══════════════════════════════════════════════════╝{R}")
    
    def base64_tool(self):
        print(f"\n{GOLD_MED}[1] Encode | [2] Decode{R}")
        choice = input(f"{CYAN}[SELECT]{R}> ").strip()
        text = input(f"{CYAN}[TEXT]{R}> ").strip()
        
        if choice == '1':
            encoded = base64.b64encode(text.encode()).decode()
            print(f"\n{GREEN}Encoded:{R} {encoded}")
        elif choice == '2':
            try:
                decoded = base64.b64decode(text).decode()
                print(f"\n{GREEN}Decoded:{R} {decoded}")
            except:
                error("Invalid Base64")
    
    def pass_gen(self):
        length = int(input(f"{CYAN}[LENGTH]{R}> ") or "16")
        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))
        print(f"\n{GOLD_BRIGHT}Generated Password:{R} {CYAN}{password}{R}")
    
    def jwt_decode(self):
        token = input(f"{CYAN}[JWT TOKEN]{R}> ").strip()
        if not token:
            return
        try:
            parts = token.split('.')
            if len(parts) == 3:
                header = json.loads(base64.b64decode(parts[0] + '==').decode())
                payload = json.loads(base64.b64decode(parts[1] + '==').decode())
                print(f"\n{GOLD_BRIGHT}Header:{R}\n{json.dumps(header, indent=2)}")
                print(f"\n{GOLD_BRIGHT}Payload:{R}\n{json.dumps(payload, indent=2)}")
        except Exception as e:
            error(f"Invalid JWT: {e}")

class WebTools:
    """Web Analysis Tools"""
    def menu(self):
        print(f"\n{GOLD_MED}╔══════════════════ WEB TOOLS ═════════════════════════╗{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[1]{R} HTTP Headers Checker                               {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[2]{R} URL Encoder/Decoder                              {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[3]{R} Website Screenshot (URL)                         {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[4]{R} SSL Certificate Checker                          {GOLD_MED}║{R}")
        print(f"{GOLD_MED}║{R} {CYAN}[0]{R} Back to Main Menu                                  {GOLD_MED}║{R}")
        print(f"{GOLD_MED}╚══════════════════════════════════════════════════════╝{R}")
        
        choice = input(f"\n{GOLD_BRIGHT}[WEB]{R} Select: ").strip()
        
        if choice == '1':
            self.headers_check()
        elif choice == '2':
            self.url_encode()
        elif choice == '3':
            self.screenshot()
        elif choice == '4':
            self.ssl_check()
    
    def headers_check(self):
        url = input(f"{CYAN}[URL]{R}> ").strip()
        if not url.startswith('http'):
            url = 'https://' + url
        
        print(f"\n{GOLD_MED}Header Check Links:{R}")
        print(f"  {GRAY}•{R} https://httpstatus.io/?url={urllib.parse.quote(url)}")
        print(f"  {GRAY}•{R} https://www.securityheaders.com/?q={urllib.parse.quote(url)}")
    
    def url_encode(self):
        text = input(f"{CYAN}[TEXT]{R}> ").strip()
        print(f"\n{GOLD_BRIGHT}Encoded:{R} {CYAN}{urllib.parse.quote(text)}{R}")
        print(f"{GOLD_BRIGHT}Decoded:{R} {CYAN}{urllib.parse.unquote(text)}{R}")
    
    def screenshot(self):
        url = input(f"{CYAN}[URL]{R}> ").strip()
        if url:
            print(f"\n{GOLD_MED}Screenshot Tools:{R}")
            print(f"  {GRAY}•{R} https://screenshot.guru/?url={urllib.parse.quote(url)}")
            print(f"  {GRAY}•{R} https://www.screenshotmachine.com/")
    
    def ssl_check(self):
        domain = input(f"{CYAN}[DOMAIN]{R}> ").strip()
        if domain:
            print(f"\n{GOLD_MED}SSL Check:{R}")
            print(f"  {GRAY}•{R} https://www.ssllabs.com/ssltest/analyze.html?d={domain}")
            print(f"  {GRAY}•{R} https://crt.sh/?q={domain}")

# ==================== MAIN ====================

def main():
    banner()
    
    print(f"\n{GOLD_MED}Initializing GOLDEN EAGLE OSINT Suite...{R}\n")
    modules = [
        "IP Intelligence Module",
        "Username Tracker Module",
        "Email Analyzer Module",
        "Cryptography Tools",
        "Web Analysis Tools",
        "Network Scanner",
    ]
    for mod in modules:
        print(f"  {GREEN}[✓]{R} {GOLD_LIGHT}{mod}{R}")
        time.sleep(0.1)
    print()
    
    ip_mod = IPModule()
    user_mod = UsernameModule()
    crypto_mod = CryptoModule()
    web_mod = WebTools()
    
    while True:
        print(f"\n{GOLD_BRIGHT}╔══════════════════════ MAIN MENU ═══════════════════════╗{R}")
        print(f"{GOLD_BRIGHT}║{R}                                                        {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[01]{R} {GOLD_LIGHT}IP Intelligence{R}          {GRAY}Geolocation & Scanning{R}    {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[02]{R} {GOLD_LIGHT}Username Tracker{R}         {GRAY}Social Media OSINT{R}        {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[03]{R} {GOLD_LIGHT}Email Intelligence{R}       {GRAY}Validation & Analysis{R}     {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[04]{R} {GOLD_LIGHT}Crypto Tools{R}             {GRAY}Hash & Encode{R}             {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[05]{R} {GOLD_LIGHT}Web Tools{R}                {GRAY}Headers & SSL{R}             {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}                                                        {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[99]{R} {GOLD_LIGHT}Clear Screen{R}                                       {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}   {CYAN}[00]{R} {RED}Exit{R}                                               {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}║{R}                                                        {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}╠════════════════════════════════════════════════════════╣{R}")
        print(f"{GOLD_BRIGHT}║{R}  {GRAY}Made by @azerkash | For Educational Purposes Only{R}     {GOLD_BRIGHT}║{R}")
        print(f"{GOLD_BRIGHT}╚════════════════════════════════════════════════════════╝{R}")
        
        choice = input(f"\n{GOLD_BRIGHT}[GOLDEN_EAGLE]{R} Select: ").strip()
        
        if choice in ['1', '01']:
            ip_mod.menu()
        elif choice in ['2', '02']:
            user_mod.menu()
        elif choice in ['3', '03']:
            user_mod.email_patterns()
        elif choice in ['4', '04']:
            crypto_mod.menu()
        elif choice in ['5', '05']:
            web_mod.menu()
        elif choice in ['99']:
            banner()
        elif choice in ['0', '00', 'exit']:
            print(f"\n{GOLD_MED}[*] Made by @azerkash{R}")
            sys.exit(0)
        
        input(f"\n{GRAY}Press Enter...{R}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GOLD_MED}[*] Made by @azerkash{R}")
        sys.exit(0)
