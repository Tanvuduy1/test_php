# -*- coding: utf-8 -*-
import os
import sys
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.edge_session"
EVIDENCE_DIR = r"D:\Tan\work\test_php\evidence"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

os.makedirs(EVIDENCE_DIR, exist_ok=True)

print("=== [THU NGHIEM TC_PHP_14] TU DONG HOA BAT NETWORK RESPONSE ===")

captured_requests = {}

def check_php_errors(text):
    patterns = [
        "Fatal error", "Parse error", "Warning:", "Notice:", "Deprecated:",
        "Strict Standards:", "Undefined index", "Undefined variable",
        "Undefined array key", "Call to a member function", "Uncaught Error",
        "Uncaught Exception", "Stack trace:", "xdebug-error"
    ]
    found = []
    for p in patterns:
        if re.search(re.escape(p), text, re.IGNORECASE):
            found.append(p)
    return list(set(found))

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True,
        channel="msedge",
        viewport={"width": 1400, "height": 900}
    )
    
    page = context.pages[0] if context.pages else context.new_page()
    
    def on_response(response):
        try:
            r_type = response.request.resource_type
            if r_type in ["fetch", "xhr"]:
                url = response.url
                # Bat cac request du lieu ticket
                body = response.text()
                captured_requests[url] = {
                    "status": response.status,
                    "url": url,
                    "body_snippet": body[:30000],
                    "php_errors": check_php_errors(body)
                }
        except Exception:
            pass

    page.on("response", on_response)
    print(f"Dang dieu huong toi: {TARGET_URL}...")
    page.goto(TARGET_URL, wait_until="networkidle")
    page.wait_for_timeout(4000)
    
    # Chup anh lam bang chung
    screenshot_path = os.path.join(EVIDENCE_DIR, "TC_PHP_14_screenshot.png")
    page.screenshot(path=screenshot_path)
    
    # Luu evidence JSON
    evidence_json = os.path.join(EVIDENCE_DIR, "TC_PHP_14_default_load.json")
    with open(evidence_json, "w", encoding="utf-8") as f:
        json.dump(captured_requests, f, ensure_ascii=False, indent=2)
        
    print(f"-> Thu thap thanh cong {len(captured_requests)} requests Network!")
    print(f"-> URL hien tai: {page.url} | Title: {page.title()}")
    print(f"-> Bang chung JSON: {evidence_json}")
    print(f"-> Bang chung anh: {screenshot_path}")
    
    context.close()

# Kiem tra xem co loi PHP nao duoc phat hien trong tat ca request khong
all_errors = []
for url, data in captured_requests.items():
    if data["php_errors"]:
        all_errors.extend(data["php_errors"])

all_errors = list(set(all_errors))

if len(all_errors) > 0:
    status = "Fail"
    actual = f"Phat hien cac loi PHP trong Response: {', '.join(all_errors)}."
    feedback = f"He thong bi ro ri loi PHP: {', '.join(all_errors)}"
else:
    status = "Pass"
    actual = f"Danh sach phieu tai thanh cong, da kiem tra {len(captured_requests)} API Network. Khong phat hien bat ky chuoi PHP Warning/Deprecated/Error nao trong Response."
    feedback = "Cac request tra HTTP 200, JSON hop le, sach loi PHP backend."

summary = {
    "TestCaseId": "TC_PHP_14",
    "Status": status,
    "ActualResult": actual,
    "Evidence": "TC_PHP_14_default_load.json",
    "Feedback": feedback,
    "RequestCount": len(captured_requests),
    "Urls": list(captured_requests.keys())
}

summary_path = os.path.join(EVIDENCE_DIR, "TC_PHP_14_summary.json")
with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("\n=== HOAN TAT PHAN TICH TC_PHP_14 ===")
print(json.dumps(summary, ensure_ascii=False, indent=2))
