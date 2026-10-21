# -*- coding: utf-8 -*-
import sys
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.browser_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print("Dang khoi chay Chrome...")
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="chrome",
        viewport={"width": 1400, "height": 900}
    )
    
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(TARGET_URL)
    
    print("\n" + "="*70)
    print("VUI LONG NHIN TREN CUA SO CHROME VUA HIEN LEN.")
    print("Hay nhap Username, Password va bam LOGIN.")
    print("Sau khi trang web chuyen sang man hinh ben trong (Ticket), ban hay de nguyen khoang 5 giay.")
    print("="*70 + "\n")
    
    while True:
        url = page.url
        # Kiem tra neu URL khong con o login
        if "login" not in url.lower():
            print(f"\n[DA PHAT HIEN DANG NHAP THANH CONG] URL: {url}")
            print("Dang doi 5 giay de he thong luu Cookie phien...")
            page.wait_for_timeout(5000)
            break
        time.sleep(1)
        
    context.close()
    print("[DA LUU HOAN TAT] Phien dang nhap da duoc luu vao o dia.")
