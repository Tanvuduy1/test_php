# -*- coding: utf-8 -*-
import sys
import time
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.edge_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print("[KHOI DONG] Dang mo Microsoft Edge qua Playwright...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="msedge",
        viewport={"width": 1400, "height": 900}
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(TARGET_URL)
    
    print("\n" + "="*70)
    print("CUA SO MICROSOFT EDGE DANG CHO BAN DANG NHAP.")
    print("Vui long nhap thong tin tai khoan truc tiep tren trinh duyet.")
    print("Sau khi vao duoc trang Ticket, he thong se tu dong ghi nhan URL va luu phien.")
    print("="*70 + "\n")
    
    start = time.time()
    success = False
    while time.time() - start < 300: # Cho toi da 5 phut
        try:
            url = page.url
            title = page.title()
            if "c=ticket" in url and "login" not in url.lower() and "login" not in title.lower():
                print(f"[XAC NHAN THANH CONG] Da nhan dien vao trang Ticket: {url}")
                page.wait_for_timeout(4000)
                success = True
                break
        except Exception:
            pass
        time.sleep(1)
        
    context.close()
    if success:
        print("[HOAN TAT] Session state da duoc luu an toan vao profile!")
        sys.exit(0)
    else:
        print("[LOI] Het thoi gian cho hoac chua hoan tat dang nhap.")
        sys.exit(1)
