import subprocess
import sys
import re
import time
import os
import webbrowser

required_packages = ["browser-cookie3", "selenium", "pyperclip", "tkinter"]
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        print(f"[!] Installing missing package: {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])


import browser_cookie3
import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox


# ---------------- CONFIG ----------------
token_file = "token.txt"
chrome_link = "https://c.mi.com/global"  
script_path = "script.py"
firefox = webbrowser.get(r'"C:\Program Files\Mozilla Firefox\firefox.exe" %s')
# ----------------------------------------

def extract_firefox_token():
    cj = browser_cookie3.firefox()
    for cookie in cj:
        if "new_bbs_serviceToken" in cookie.name:
            return cookie.value
    return None

def extract_chrome_token(link):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    root = tk.Tk()
    root.withdraw()  
    messagebox.showinfo(
        "Login required",
        f"Please login on c.mi.com/global.\n"
        "Then, press OK AFTER logging in."
    )
    root.destroy()


    token = driver.execute_script("""
        var match = document.cookie.match(/popRunToken=([^;]+)/);
        return match ? match[1] : null;
    """)
    driver.quit()

    if token:
      
        print(f"[✔] Token found!")
    else:
        print("[✖] Token not found!")

    return token  

#Update token.txt
def update_token_file(firefox_token, chrome_token):
    lines = [
        firefox_token or "N/A",
        chrome_token or "N/A",
        firefox_token or "N/A",
        chrome_token or "N/A"
    ]
    with open(token_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("[✔] token.txt updated with all tokens!")

def prompt_login_firefox():
    firefox.open("https://c.mi.com/global")
    root = tk.Tk()
    root.withdraw() 
    messagebox.showinfo(
        "Login required",
        f"Please login on c.mi.com/global in firefox.\n"
        "Press OK after logging in."
    )
    root.destroy()
    

if __name__ == "__main__":
    print("GetTokens by bybestix on xdaforums")
    prompt_login_firefox()
    firefox_token = extract_firefox_token()
    if not firefox_token:
        print("[✖] Firefox token not found!")
    
    chrome_token = extract_chrome_token(chrome_link)
    if not chrome_token:
        print("[✖] Chrome token not found!")

    update_token_file(firefox_token, chrome_token)

    for i in range(1, 5):
        subprocess.Popen(
        f'start cmd /k "echo {i} | py {script_path}"',
        shell=True
    )
    time.sleep(0.5)

    
