# -*- coding: utf-8 -*-
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.edge_session"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

print("[KIEM TRA KHOI PHUC PHIEN] Dang mo lai Edge voi profile da luu...")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True,
        channel="msedge"
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(TARGET_URL, wait_until="networkidle")
    
    final_url = page.url
    final_title = page.title()
    
    print(f"URL sau khi dieu huong: {final_url}")
    print(f"Title sau khi dieu huong: {final_title}")
    
    is_valid_session = ("c=ticket" in final_url and "login" not in final_url.lower() and "login" not in final_title.lower())
    
    context.close()
    
    if is_valid_session:
        print("[KET QUA] KHOI PHUC PHIEN THANH CONG! Trang Ticket duoc truy cap truc tiep khong bi vang ve login.")
        sys.exit(0)
    else:
        print(f"[KET QUA] KHOI PHUC PHIEN THAT BAI! Trang bi chuyen huong ve: {final_url}")
        sys.exit(1)
