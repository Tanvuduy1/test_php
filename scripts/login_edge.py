# -*- coding: utf-8 -*-
import os
import sys
import json
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.edge_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print("[KHOI CHAY] Dang mo Microsoft Edge de dang nhap...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="msedge",
        viewport={"width": 1400, "height": 900}
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(TARGET_URL)
    
    print("Vui long dang nhap tren cua so Microsoft Edge...")
    
    start = time.time()
    while time.time() - start < 180:
        url = page.url
        title = page.title()
        if "login" not in url.lower() and "login" not in title.lower():
            print(f"[XAC NHAN DANG NHAP THANH CONG] URL: {url} | Title: {title}")
            page.wait_for_timeout(4000)
            break
        time.sleep(1)
        
    context.close()
    print("[DA LUU SESSION] Session Edge da luu thanh cong!")
