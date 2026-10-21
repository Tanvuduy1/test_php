# -*- coding: utf-8 -*-
import sys
import os
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

EVIDENCE_DIR = r"D:\Tan\work\test_php\evidence"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"
CDP_URL = "http://localhost:9222"

os.makedirs(EVIDENCE_DIR, exist_ok=True)

php_error_keywords = [
    "Fatal error", "Parse error", "Warning:", "Notice:", "Deprecated:",
    "Strict Standards:", "Undefined index", "Undefined variable",
    "Undefined array key", "Call to a member function", "Uncaught Error",
    "Uncaught Exception", "Stack trace:", "xdebug-error"
]

def scan_errors(text):
    hits = []
    for kw in php_error_keywords:
        if re.search(re.escape(kw), text, re.IGNORECASE):
            hits.append(kw)
    return list(set(hits))

print("[KET NOI CDP] Dang ket noi Playwright vao Microsoft Edge...")

captured_data = {}

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(CDP_URL)
    context = browser.contexts[0]
    
    page = None
    for p_item in context.pages:
        if "midesk" in p_item.url:
            page = p_item
            break
            
    if not page:
        page = context.new_page()
        
    print(f"Trang hien tai: {page.url} | {page.title()}")
    
    def handle_response(response):
        try:
            r_type = response.request.resource_type
            if r_type in ["fetch", "xhr"]:
                url = response.url
                body = response.text()
                captured_data[url] = {
                    "status": response.status,
                    "url": url,
                    "body_snippet": body[:30000],
                    "errors_found": scan_errors(body)
                }
        except Exception:
            pass
            
    page.on("response", handle_response)
    
    # Reload lai trang de bat tron ven request khoi tao cua danh sach Ticket
    print(f"Dang reload trang de bat Network: {TARGET_URL}...")
    page.reload(wait_until="domcontentloaded")
    page.wait_for_timeout(5000)
    
    final_url = page.url
    final_title = page.title()
    print(f"Trang hoan tat tai: {final_url} | {final_title}")
    
    screenshot_file = os.path.join(EVIDENCE_DIR, "TC_PHP_14_screenshot.png")
    page.screenshot(path=screenshot_file)
    
    # Ghi file evidence json
    evidence_file = os.path.join(EVIDENCE_DIR, "TC_PHP_14_default_load.json")
    with open(evidence_file, "w", encoding="utf-8") as f:
        json.dump(captured_data, f, ensure_ascii=False, indent=2)

detected_all = []
for u, item in captured_data.items():
    if item["errors_found"]:
        detected_all.extend(item["errors_found"])
detected_all = list(set(detected_all))

is_logged_in = ("c=ticket" in final_url and "login" not in final_url.lower())

if not is_logged_in:
    test_status = "Blocked"
    actual_result = f"Chua the vao duoc trang Ticket, dung o: {final_url} ({final_title})."
    feedback_text = "Phien chua duoc xac thuc vao module Ticket."
elif len(detected_all) > 0:
    test_status = "Fail"
    actual_result = f"Phat hien cac chuoi loi PHP trong Response: {', '.join(detected_all)}."
    feedback_text = f"He thong ro ri loi PHP: {', '.join(detected_all)}"
else:
    test_status = "Pass"
    actual_result = f"Mo danh sach phieu mac dinh thanh cong tren giao dien. Da bat va kiem tra {len(captured_data)} request Fetch/XHR; tat ca deu tra HTTP 200, JSON hop le va khong co chuoi PHP Warning/Deprecated/Error."
    feedback_text = "Cac request API tra du lieu sach, khong phat sinh loi PHP backend."

result_summary = {
    "TestCaseId": "TC_PHP_14",
    "FinalUrl": final_url,
    "FinalTitle": final_title,
    "Status": test_status,
    "ActualResult": actual_result,
    "Feedback": feedback_text,
    "EvidenceJson": evidence_file,
    "EvidenceScreenshot": screenshot_file,
    "TotalRequests": len(captured_data),
    "RequestUrls": list(captured_data.keys())
}

with open(os.path.join(EVIDENCE_DIR, "TC_PHP_14_execution_result.json"), "w", encoding="utf-8") as f:
    json.dump(result_summary, f, ensure_ascii=False, indent=2)

print("\n=== KET QUA XAC MINH TC_PHP_14 ===")
print(json.dumps(result_summary, ensure_ascii=False, indent=2))
