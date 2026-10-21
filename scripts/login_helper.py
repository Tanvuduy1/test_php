import os
import json
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.browser_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print(f"[THONG TIN] Khoi chay Chrome Playwright tai profile: {USER_DATA_DIR}")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="chrome",
        viewport={"width": 1400, "height": 900},
        args=["--disable-blink-features=AutomationControlled"]


        
    )
    
    page = context.pages[0] if context.pages else context.new_page()
    print(f"[DANG DIEU HUONG] Mo trang: {TARGET_URL}")
    page.goto(TARGET_URL)
    
    print("\n" + "="*70)
    print("CHROME DA HIEN THI TREN MAN HINH CUA BAN.")
    print("Vui long dang nhap tren trinh duyet.")
    print("Script dang tu dong lang nghe cho den khi ban vao trang Ticket thanh cong...")
    print("="*70 + "\n")
    
    # Cho nguoi dung dang nhap trong toi da 3 phut (180 giay)
    start_time = time.time()
    logged_in = False
    
    while time.time() - start_time < 180:
        current_url = page.url
        # Kiem tra neu URL chua c=ticket va co phan tu dac trung cua trang Ticket (bang danh sach hoac menu)
        if "c=ticket" in current_url:
            # Kiem tra xem co the tim thay phan tu sau dang nhap khong
            try:
                # Neu khong con o trang login nua
                if "login" not in current_url.lower():
                    # Cho 3 giay de session on dinh
                    page.wait_for_timeout(3000)
                    logged_in = True
                    print(f"\n[THANH CONG] Phat hien da dang nhap thanh cong vao URL: {current_url}")
                    break
            except Exception:
                pass
        time.sleep(2)
        
    if logged_in:
        print("[LUNG PHIEN] Dang luu cookie va session vao profile...")
        page.wait_for_timeout(2000)
        context.close()
        print("[HOAN TAT] Da luu phien dang nhap thanh cong! San sang chay kiem thu tu dong.")
    else:
        print("\n[TIMEOUT] Da qua 3 phut ma chua hoan tat dang nhap. Vui long thu lai.")
        context.close()
