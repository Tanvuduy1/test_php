# -*- coding: utf-8 -*-
import sys
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.edge_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print("[KHOI DONG] Dang mo Microsoft Edge...")

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
    print("VUI LONG DANG NHAP TREN MICROSOFT EDGE.")
    print("Sau khi dang nhap vao duoc trang Ticket, bam F5 mot lan.")
    print("Khi nao thay bang danh sach Ticket hien thi on dinh, HAY DONG TRINH DUYET (bam dau X).")
    print("="*70 + "\n")
    
    # Cho nguoi dung chu dong dong trinh duyet bang tay
    try:
        page.wait_for_event("close", timeout=300000)
    except Exception:
        pass
        
    context.close()
    print("[XAC NHAN] Trinh duyet da dong. Session da duoc he thong Flush xuong o dia hoan toan!")
