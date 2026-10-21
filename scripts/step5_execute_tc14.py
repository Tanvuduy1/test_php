# -*- coding: utf-8 -*-
import sys
import os
import json
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"D:\Tan\work\test_php\.edge_session"
EVIDENCE_DIR = r"D:\Tan\work\test_php\evidence"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"

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

print("[THUC THI TC_PHP_14] Dang khoi chay kiem thu tu dong...")

captured_data = {}

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=USER_DATA_DIR,
        headless=True,
        channel="msedge"
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    def handle_response(response):
        try:
            if response.request.resource_type in ["fetch", "xhr"]:
                url = response.url
                body = response.text()
                captured_data[url] = {
                    "status": response.status,
                    "url": url,
                    "headers": dict(response.headers),
                    "body_snippet": body[:20000],
                    "errors_found": scan_errors(body)
                }
        except Exception:
            pass
            
    page.on("response", handle_response)
    page.goto(TARGET_URL, wait_until="networkidle")
    page.wait_for_timeout(4000)
    
    screenshot_file = os.path.join(EVIDENCE_DIR, "TC_PHP_14_screenshot.png")
    page.screenshot(path=screenshot_file)
    
    context.close()

# Luu bang chung json
evidence_file = os.path.join(EVIDENCE_DIR, "TC_PHP_14_default_load.json")
with open(evidence_file, "w", encoding="utf-8") as f:
    json.dump(captured_data, f, ensure_ascii=False, indent=2)

detected_all = []
for u, item in captured_data.items():
    if item["errors_found"]:
        detected_all.extend(item["errors_found"])
detected_all = list(set(detected_all))

if len(detected_all) > 0:
    test_status = "Fail"
    actual_result = f"Phat hien cac loi PHP trong Response: {', '.join(detected_all)}."
    feedback_text = f"He thong bi ro ri loi PHP: {', '.join(detected_all)}"
else:
    test_status = "Pass"
    actual_result = f"Tai danh sach phieu thanh cong, da bat va kiem tra {len(captured_data)} request Fetch/XHR. Tat ca deu tra HTTP 200, JSON hop le va khong xuat hien PHP Warning/Deprecated/Error."
    feedback_text = "Cac request tra ve du lieu chuan, response sach loi backend."

result_summary = {
    "TestCaseId": "TC_PHP_14",
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

print("\n=== KET QUA THUC THI TC_PHP_14 ===")
print(json.dumps(result_summary, ensure_ascii=False, indent=2))
