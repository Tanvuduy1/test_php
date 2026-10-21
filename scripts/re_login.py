# -*- coding: utf-8 -*-
import os
import sys
import json
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.browser_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print("[THONG TIN] Mo lai Chrome voi profile .browser_session de ban dang nhap...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="chrome",
        viewport={"width": 1400, "height": 900}
    )
    
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(TARGET_URL)
    
    print("Vui long dang nhap tren cua so Chrome nay...")
    print("Script dang theo doi URL lien tuc...")
    
    # Cho den khi URL khong con chua 'login' va load thanh cong vao he thong
    start = time.time()
    while time.time() - start < 300: # 5 phut
        url = page.url
        title = page.title()
        if "login" not in url.lower() and "login" not in title.lower():
            # Da vao trang he thong
            print(f"[XAC NHAN] Da dang nhap vao he thong! URL hien tai: {url} | Title: {title}")
            page.wait_for_timeout(5000) # Cho 5s luu day du cookie
            break
        time.sleep(2)
        
    context.close()
    print("[DA LUU] Session va Cookie da duoc ghi vao o dia thanh cong!")
