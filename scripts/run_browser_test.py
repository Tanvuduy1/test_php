# -*- coding: utf-8 -*-
import os
import sys
import json
import re

# Set UTF-8 encoding cho console
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.browser_session"
EVIDENCE_DIR = r"D:\Tan\work\test_php\evidence"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

os.makedirs(EVIDENCE_DIR, exist_ok=True)

print("=== BAT DAU TU DONG CHAY KIEM THU QUA PLAYWRIGHT ===")

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=False,
        channel="chrome",
        viewport={"width": 1400, "height": 900}
    )
    
    page = context.pages[0] if context.pages else context.new_page()
    
    # -------------------------------------------------------------
    # TC_PHP_14: Tải danh sách mặc định & bắt request khởi tạo
    # -------------------------------------------------------------
    print("[1/3] THUC THI TC_PHP_14: Tai man hinh danh sach Ticket mac dinh...")
    captured_responses = {}

    def on_response(response):
        try:
            r_type = response.request.resource_type
            if r_type in ["fetch", "xhr"]:
                url = response.url
                # Bat tat ca cac request lien quan den api/data/ticket
                body = response.text()
                captured_responses[url] = {
                    "status": response.status,
                    "url": url,
                    "headers": dict(response.headers),
                    "body": body[:50000]
                }
        except Exception:
            pass

    page.on("response", on_response)
    page.goto(TARGET_URL, wait_until="networkidle")
    page.wait_for_timeout(3000)
    
    # Chụp ảnh màn hình làm bằng chứng
    screenshot_14 = os.path.join(EVIDENCE_DIR, "TC_PHP_14_screenshot.png")
    page.screenshot(path=screenshot_14)
    
    ev_file_14 = os.path.join(EVIDENCE_DIR, "TC_PHP_14_default_load.json")
    with open(ev_file_14, "w", encoding="utf-8") as f:
        json.dump(captured_responses, f, ensure_ascii=False, indent=2)
    print(f"-> TC_PHP_14 thanh cong! Bat duoc {len(captured_responses)} requests. Luu tai: {ev_file_14}")

    # -------------------------------------------------------------
    # TC_PHP_19: Kiểm tra tham số ID không tồn tại (?c=ticket&id=-99999)
    # -------------------------------------------------------------
    print("\n[2/3] THUC THI TC_PHP_19: Kiem tra tham so ID khong ton tai (?c=ticket&id=-99999)...")
    url_invalid = "https://dev-85.midesk.vn/vi?c=ticket&id=-99999"
    resp = page.goto(url_invalid, wait_until="networkidle")
    page.wait_for_timeout(2000)
    html_content = page.content()
    
    screenshot_19 = os.path.join(EVIDENCE_DIR, "TC_PHP_19_screenshot.png")
    page.screenshot(path=screenshot_19)
    
    ev_file_19 = os.path.join(EVIDENCE_DIR, "TC_PHP_19_param_id_not_found.json")
    with open(ev_file_19, "w", encoding="utf-8") as f:
        json.dump({
            "status": resp.status if resp else 0,
            "url": url_invalid,
            "content_snippet": html_content[:50000]
        }, f, ensure_ascii=False, indent=2)
    print(f"-> TC_PHP_19 thanh cong! Luu tai: {ev_file_19}")

    # -------------------------------------------------------------
    # TC_PHP_20: Kiểm tra tham số ID rỗng (?c=ticket&id=)
    # -------------------------------------------------------------
    print("\n[3/3] THUC THI TC_PHP_20: Kiem tra tham so ID rong (?c=ticket&id=)...")
    url_empty = "https://dev-85.midesk.vn/vi?c=ticket&id="
    resp2 = page.goto(url_empty, wait_until="networkidle")
    page.wait_for_timeout(2000)
    html_content2 = page.content()
    
    screenshot_20 = os.path.join(EVIDENCE_DIR, "TC_PHP_20_screenshot.png")
    page.screenshot(path=screenshot_20)
    
    ev_file_20 = os.path.join(EVIDENCE_DIR, "TC_PHP_20_param_id_empty.json")
    with open(ev_file_20, "w", encoding="utf-8") as f:
        json.dump({
            "status": resp2.status if resp2 else 0,
            "url": url_empty,
            "content_snippet": html_content2[:50000]
        }, f, ensure_ascii=False, indent=2)
    print(f"-> TC_PHP_20 thanh cong! Luu tai: {ev_file_20}")

    context.close()
    print("\n=== HOAN THANH KIEM THU TU DONG VA THU THAP BANG CHUNG ===")
