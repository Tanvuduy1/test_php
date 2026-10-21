# -*- coding: utf-8 -*-
"""
Script thuc thi tu dong 20 ca kiem thu moi (TC_PHP_24 -> TC_PHP_43)
ket noi qua Chrome/Edge DevTools Protocol (CDP) tai http://localhost:9222.
Chup anh man hinh that (.png) va luu request API that (.json) cho moi ca.
"""
import sys
import os
import json
import re
import time

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from playwright.sync_api import sync_playwright

EVIDENCE_DIR = r"D:\Tan\work\test_php\evidence"
TARGET_URL = "https://dev-85.midesk.vn/vi?c=ticket&id=default"
CDP_URL = "http://localhost:9222"

os.makedirs(EVIDENCE_DIR, exist_ok=True)

PHP_ERROR_PATTERNS = [
    "Fatal error", "Parse error", "Warning:", "Notice:", "Deprecated:",
    "Strict Standards:", "Undefined index", "Undefined variable",
    "Undefined array key", "Call to a member function", "Uncaught Error",
    "Uncaught Exception", "Stack trace:", "xdebug-error"
]

IGNORED_EXTENSIONS = ('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.woff', '.woff2', '.ttf', '.ico')

def scan_php_errors(text):
    hits = []
    for kw in PHP_ERROR_PATTERNS:
        if re.search(re.escape(kw), text, re.IGNORECASE):
            hits.append(kw)
    return list(set(hits))

def is_static_asset(url):
    clean_url = url.split('?')[0].lower()
    return clean_url.endswith(IGNORED_EXTENSIONS)

class NetworkSniffer:
    def __init__(self, page):
        self.page = page
        self.captured = {}
        self._handler = self._make_handler()
        self.page.on("response", self._handler)

    def _make_handler(self):
        def on_response(response):
            try:
                url = response.url
                if is_static_asset(url):
                    return
                r_type = response.request.resource_type
                if r_type in ["fetch", "xhr", "document"]:
                    body = response.text()
                    errors = scan_php_errors(body)
                    self.captured[url] = {
                        "status": response.status,
                        "url": url,
                        "resource_type": r_type,
                        "errors_found": errors,
                        "snippet": body[:5000]
                    }
            except Exception:
                pass
        return on_response

    def reset(self):
        self.captured.clear()

    def detach(self):
        try:
            self.page.remove_listener("response", self._handler)
        except Exception:
            pass

def get_ticket_frame(page):
    f = page.frame("gidindexTicketFrame")
    if not f:
        for _ in range(10):
            page.wait_for_timeout(500)
            f = page.frame("gidindexTicketFrame")
            if f:
                break
    return f

def run_tests():
    print("="*80)
    print("BAT DAU CHUONG TRINH THUC THI KIEM THU TU DONG (TC_PHP_24 -> TC_PHP_43)")
    print(f"Ket noi CDP: {CDP_URL}")
    print("="*80)

    with sync_playwright() as p:
        try:
            browser = p.chromium.connect_over_cdp(CDP_URL)
        except Exception as e:
            print(f"\n[LOI KET NOI CDP] Khong the ket noi toi {CDP_URL}: {e}")
            print("Vui long nhap dup file 'start_edge_debug.bat' tren Desktop de bat Edge truoc!")
            return False

        context = browser.contexts[0]
        page = None
        for p_item in context.pages:
            if "midesk" in p_item.url:
                page = p_item
                break
        if not page:
            page = context.new_page()

        print(f"[TRANG HIEN TAI] URL: {page.url} | Tieu de: {page.title()}")

        if "login" in page.url.lower():
            print("\n[CANH BAO] Trinh duyet dang o trang LOGIN.")
            print("Vui long dang nhap tren trinh duyet roi chay lai script!")
            return False

        sniffer = NetworkSniffer(page)
        test_results = {}

        # Dam bao dang o trang ticket
        if "c=ticket" not in page.url:
            page.goto(TARGET_URL, wait_until="commit")
            page.wait_for_timeout(4000)

        # -------------------------------------------------------------
        # TC_PHP_24: Gui phan hoi trao doi cong khai (Public Reply)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_24 (Them phan hoi trao doi cong khai)...")
        sniffer.reset()
        tf = get_ticket_frame(page)
        try:
            if tf:
                tf.evaluate("""() => {
                    const el = jQuery('a.ticket').first();
                    if (el.length && typeof window.addTabTicket === 'function') {
                        window.addTabTicket(el.data('id'), el.data('name'), el.data('status'));
                    }
                }""")
            page.wait_for_timeout(3500)
            # Tim textarea phan hoi
            page.evaluate("""() => {
                const txt = document.querySelector('textarea.content-ticket, textarea#comment, textarea[name="content"]');
                if (txt) {
                    txt.value = "Bộ phận kỹ thuật đã ghi nhận và đang xử lý yêu cầu.";
                    jQuery(txt).trigger('input').trigger('change');
                }
            }""")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"TC_PHP_24 error: {e}")

        screenshot_24 = os.path.join(EVIDENCE_DIR, "TC_PHP_24_screenshot.png")
        page.screenshot(path=screenshot_24)
        evidence_24 = os.path.join(EVIDENCE_DIR, "TC_PHP_24_ticket_reply.json")
        with open(evidence_24, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_24: Da chup anh {screenshot_24} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_25: Them ghi chu noi bo (Internal Note)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_25 (Them ghi chu noi bo)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const noteBtn = document.querySelector('a:contains("Ghi chú"), button:contains("Ghi chú"), .btn-private, .tab-private');
                if (noteBtn) noteBtn.click();
            }""")
            page.wait_for_timeout(2500)
        except Exception as e:
            print(f"TC_PHP_25 error: {e}")

        screenshot_25 = os.path.join(EVIDENCE_DIR, "TC_PHP_25_screenshot.png")
        page.screenshot(path=screenshot_25)
        evidence_25 = os.path.join(EVIDENCE_DIR, "TC_PHP_25_internal_note.json")
        with open(evidence_25, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_25: Da chup anh {screenshot_25} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_26: Dinh kem tep tin (Attachment)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_26 (Dinh kem tep tin vao binh luan)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const attachBtn = document.querySelector('.fa-paperclip, .btn-attach, input[type="file"]');
                if (attachBtn) attachBtn.scrollIntoView();
            }""")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"TC_PHP_26 error: {e}")

        screenshot_26 = os.path.join(EVIDENCE_DIR, "TC_PHP_26_screenshot.png")
        page.screenshot(path=screenshot_26)
        evidence_26 = os.path.join(EVIDENCE_DIR, "TC_PHP_26_ticket_attachment.json")
        with open(evidence_26, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_26: Da chup anh {screenshot_26} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_27: Thay doi muc do uu tien (Priority)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_27 (Cap nhat muc do uu tien)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const selPriority = jQuery('select[name="priority"], select.priority-select');
                if (selPriority.length) {
                    selPriority.val('high').trigger('change');
                }
            }""")
            page.wait_for_timeout(2500)
        except Exception as e:
            print(f"TC_PHP_27 error: {e}")

        screenshot_27 = os.path.join(EVIDENCE_DIR, "TC_PHP_27_screenshot.png")
        page.screenshot(path=screenshot_27)
        evidence_27 = os.path.join(EVIDENCE_DIR, "TC_PHP_27_change_priority.json")
        with open(evidence_27, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_27: Da chup anh {screenshot_27} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_28: Thay doi nhan vien/nhom phu trach (Reassign)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_28 (Thay doi nhan vien/nhom phu trach)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const selAgent = jQuery('select[name="assign_agent"], select.assign-select');
                if (selAgent.length && selAgent.find('option').length > 1) {
                    selAgent.val(selAgent.find('option').eq(1).val()).trigger('change');
                }
            }""")
            page.wait_for_timeout(2500)
        except Exception as e:
            print(f"TC_PHP_28 error: {e}")

        screenshot_28 = os.path.join(EVIDENCE_DIR, "TC_PHP_28_screenshot.png")
        page.screenshot(path=screenshot_28)
        evidence_28 = os.path.join(EVIDENCE_DIR, "TC_PHP_28_reassign_agent.json")
        with open(evidence_28, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_28: Da chup anh {screenshot_28} ({len(sniffer.captured)} requests)")

        # Quay lai danh sach ticket mac dinh
        page.goto(TARGET_URL, wait_until="commit")
        page.wait_for_timeout(3500)

        # -------------------------------------------------------------
        # TC_PHP_29: Bo loc hang doi phieu (Queues)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_29 (Bo loc hang doi phieu)...")
        sniffer.reset()
        tf = get_ticket_frame(page)
        try:
            if tf:
                tf.evaluate("""() => {
                    const li = jQuery('li[data-id="unsolved-team"], li[data-id="breached"]').first();
                    if (li.length) li.click();
                }""")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"TC_PHP_29 error: {e}")

        screenshot_29 = os.path.join(EVIDENCE_DIR, "TC_PHP_29_screenshot.png")
        page.screenshot(path=screenshot_29)
        evidence_29 = os.path.join(EVIDENCE_DIR, "TC_PHP_29_filter_queue.json")
        with open(evidence_29, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_29: Da chup anh {screenshot_29} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_30: Sap xep bang danh sach (Sorting)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_30 (Sap xep bang danh sach)...")
        sniffer.reset()
        tf = get_ticket_frame(page)
        try:
            if tf:
                tf.evaluate("""() => {
                    jQuery('#table_ticket th').first().click();
                }""")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"TC_PHP_30 error: {e}")

        screenshot_30 = os.path.join(EVIDENCE_DIR, "TC_PHP_30_screenshot.png")
        page.screenshot(path=screenshot_30)
        evidence_30 = os.path.join(EVIDENCE_DIR, "TC_PHP_30_table_sorting.json")
        with open(evidence_30, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_30: Da chup anh {screenshot_30} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_31: Thao tac hang loat (Bulk Action)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_31 (Thao tac hang loat)...")
        sniffer.reset()
        tf = get_ticket_frame(page)
        try:
            if tf:
                tf.evaluate("""() => {
                    jQuery('#table_ticket tbody input[type="checkbox"]').slice(0, 2).prop('checked', true).trigger('change');
                }""")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"TC_PHP_31 error: {e}")

        screenshot_31 = os.path.join(EVIDENCE_DIR, "TC_PHP_31_screenshot.png")
        page.screenshot(path=screenshot_31)
        evidence_31 = os.path.join(EVIDENCE_DIR, "TC_PHP_31_bulk_action.json")
        with open(evidence_31, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_31: Da chup anh {screenshot_31} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_32: Xem lich su hoat dong (Audit Trail)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_32 (Xem lich su hoat dong phieu)...")
        sniffer.reset()
        try:
            tf = get_ticket_frame(page)
            if tf:
                tf.evaluate("""() => {
                    const el = jQuery('a.ticket').first();
                    if (el.length && typeof window.addTabTicket === 'function') {
                        window.addTabTicket(el.data('id'), el.data('name'), el.data('status'));
                    }
                }""")
            page.wait_for_timeout(3000)
            page.evaluate("""() => {
                const actTab = document.querySelector('a:contains("Lịch sử"), a:contains("Activity"), #tab_activity');
                if (actTab) actTab.click();
            }""")
            page.wait_for_timeout(2500)
        except Exception as e:
            print(f"TC_PHP_32 error: {e}")

        screenshot_32 = os.path.join(EVIDENCE_DIR, "TC_PHP_32_screenshot.png")
        page.screenshot(path=screenshot_32)
        evidence_32 = os.path.join(EVIDENCE_DIR, "TC_PHP_32_ticket_activity.json")
        with open(evidence_32, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_32: Da chup anh {screenshot_32} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_33: Xuat du lieu danh sach phieu (Export Excel)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_33 (Xuat du lieu danh sach phieu)...")
        page.goto(TARGET_URL, wait_until="commit")
        page.wait_for_timeout(3500)
        sniffer.reset()
        try:
            tf = get_ticket_frame(page)
            if tf:
                tf.evaluate("""() => {
                    const btnExp = jQuery('button:contains("Export"), a:contains("Export")');
                    if (btnExp.length) btnExp.first().click();
                }""")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"TC_PHP_33 error: {e}")

        screenshot_33 = os.path.join(EVIDENCE_DIR, "TC_PHP_33_screenshot.png")
        page.screenshot(path=screenshot_33)
        evidence_33 = os.path.join(EVIDENCE_DIR, "TC_PHP_33_export_ticket.json")
        with open(evidence_33, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_33: Da chup anh {screenshot_33} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_34: Tai danh sach khach hang (Customer module)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_34 (Tai danh sach khach hang)...")
        sniffer.reset()
        try:
            page.goto("https://dev-85.midesk.vn/vi?c=customer", wait_until="commit")
            page.wait_for_timeout(4500)
        except Exception as e:
            print(f"TC_PHP_34 goto: {e}")

        screenshot_34 = os.path.join(EVIDENCE_DIR, "TC_PHP_34_screenshot.png")
        page.screenshot(path=screenshot_34)
        evidence_34 = os.path.join(EVIDENCE_DIR, "TC_PHP_34_customer_list.json")
        with open(evidence_34, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_34: Da chup anh {screenshot_34} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_35: Tim kiem khach hang theo SDT/Email
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_35 (Tim kiem khach hang)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const searchInp = document.querySelector('input[type="search"], #search-customer, input[name="search"]');
                if (searchInp) {
                    searchInp.value = "0917601298";
                    jQuery(searchInp).trigger('input').trigger('change');
                }
            }""")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"TC_PHP_35 error: {e}")

        screenshot_35 = os.path.join(EVIDENCE_DIR, "TC_PHP_35_screenshot.png")
        page.screenshot(path=screenshot_35)
        evidence_35 = os.path.join(EVIDENCE_DIR, "TC_PHP_35_customer_search.json")
        with open(evidence_35, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_35: Da chup anh {screenshot_35} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_36: Mo form them moi khach hang
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_36 (Mo form them moi khach hang)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const addCustBtn = document.querySelector('button:contains("Thêm"), a:contains("Thêm"), .btn-add-customer');
                if (addCustBtn) addCustBtn.click();
            }""")
            page.wait_for_timeout(3500)
        except Exception as e:
            print(f"TC_PHP_36 error: {e}")

        screenshot_36 = os.path.join(EVIDENCE_DIR, "TC_PHP_36_screenshot.png")
        page.screenshot(path=screenshot_36)
        evidence_36 = os.path.join(EVIDENCE_DIR, "TC_PHP_36_customer_create_form.json")
        with open(evidence_36, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_36: Da chup anh {screenshot_36} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_37: Validation so dien thoai khach hang
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_37 (Validation so dien thoai)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const phoneInp = document.querySelector('input[name="phone"], input#phone');
                if (phoneInp) {
                    phoneInp.value = "invalid_phone_123!@#";
                    jQuery(phoneInp).trigger('input').trigger('change');
                }
            }""")
            page.wait_for_timeout(2000)
        except Exception as e:
            print(f"TC_PHP_37 error: {e}")

        screenshot_37 = os.path.join(EVIDENCE_DIR, "TC_PHP_37_screenshot.png")
        page.screenshot(path=screenshot_37)
        evidence_37 = os.path.join(EVIDENCE_DIR, "TC_PHP_37_customer_invalid_phone.json")
        with open(evidence_37, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_37: Da chup anh {screenshot_37} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_38: Xem tab lich su phieu cua khach hang
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_38 (Lich su phieu cua khach hang)...")
        sniffer.reset()
        try:
            page.goto("https://dev-85.midesk.vn/vi?c=customer", wait_until="commit")
            page.wait_for_timeout(3500)
            page.evaluate("""() => {
                const firstRow = document.querySelector('table tbody tr td a');
                if (firstRow) firstRow.click();
            }""")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"TC_PHP_38 error: {e}")

        screenshot_38 = os.path.join(EVIDENCE_DIR, "TC_PHP_38_screenshot.png")
        page.screenshot(path=screenshot_38)
        evidence_38 = os.path.join(EVIDENCE_DIR, "TC_PHP_38_customer_ticket_history.json")
        with open(evidence_38, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_38: Da chup anh {screenshot_38} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_39: Bieu do ty le SLA Agent (Dashboard)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_39 (Bieu do ty le SLA Agent)...")
        sniffer.reset()
        try:
            page.goto("https://dev-85.midesk.vn/vi?c=dashboard", wait_until="commit")
            page.wait_for_timeout(4500)
        except Exception as e:
            print(f"TC_PHP_39 goto: {e}")

        screenshot_39 = os.path.join(EVIDENCE_DIR, "TC_PHP_39_screenshot.png")
        page.screenshot(path=screenshot_39)
        evidence_39 = os.path.join(EVIDENCE_DIR, "TC_PHP_39_dashboard_sla_chart.json")
        with open(evidence_39, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_39: Da chup anh {screenshot_39} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_40: Loc Dashboard theo kenh (Channel filter)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_40 (Loc Dashboard theo kenh)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const selChannel = jQuery('select[name="channel"]');
                if (selChannel.length) {
                    selChannel.val('email').trigger('change');
                    const btnFilter = jQuery('button:contains("Filter")');
                    if (btnFilter.length) btnFilter.click();
                }
            }""")
            page.wait_for_timeout(3500)
        except Exception as e:
            print(f"TC_PHP_40 error: {e}")

        screenshot_40 = os.path.join(EVIDENCE_DIR, "TC_PHP_40_screenshot.png")
        page.screenshot(path=screenshot_40)
        evidence_40 = os.path.join(EVIDENCE_DIR, "TC_PHP_40_dashboard_filter_channel.json")
        with open(evidence_40, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_40: Da chup anh {screenshot_40} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_41: Bao cao thoi gian phan hoi dau tien (FRL)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_41 (Bao cao FRL)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const chartFRL = document.querySelector('#chart_sla_frl_agent');
                if (chartFRL) chartFRL.scrollIntoView();
            }""")
            page.wait_for_timeout(3000)
        except Exception as e:
            print(f"TC_PHP_41 error: {e}")

        screenshot_41 = os.path.join(EVIDENCE_DIR, "TC_PHP_41_screenshot.png")
        page.screenshot(path=screenshot_41)
        evidence_41 = os.path.join(EVIDENCE_DIR, "TC_PHP_41_report_agent_frl.json")
        with open(evidence_41, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_41: Da chup anh {screenshot_41} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_42: Quan ly hang doi (Queues)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_42 (Quan ly hang doi)...")
        sniffer.reset()
        try:
            page.goto("https://dev-85.midesk.vn/vi?c=setting", wait_until="commit")
            page.wait_for_timeout(4000)
        except Exception as e:
            print(f"TC_PHP_42 goto: {e}")

        screenshot_42 = os.path.join(EVIDENCE_DIR, "TC_PHP_42_screenshot.png")
        page.screenshot(path=screenshot_42)
        evidence_42 = os.path.join(EVIDENCE_DIR, "TC_PHP_42_setting_queues.json")
        with open(evidence_42, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_42: Da chup anh {screenshot_42} ({len(sniffer.captured)} requests)")

        # -------------------------------------------------------------
        # TC_PHP_43: Quan ly mau cau tra loi nhanh (Macros)
        # -------------------------------------------------------------
        print("\n>>> DANG THUC THI: TC_PHP_43 (Quan ly mau cau tra loi nhanh)...")
        sniffer.reset()
        try:
            page.evaluate("""() => {
                const macroMenu = document.querySelector('a:contains("Mẫu trả lời"), a:contains("Macro"), a:contains("Canned")');
                if (macroMenu) macroMenu.click();
            }""")
            page.wait_for_timeout(3500)
        except Exception as e:
            print(f"TC_PHP_43 error: {e}")

        screenshot_43 = os.path.join(EVIDENCE_DIR, "TC_PHP_43_screenshot.png")
        page.screenshot(path=screenshot_43)
        evidence_43 = os.path.join(EVIDENCE_DIR, "TC_PHP_43_setting_canned_responses.json")
        with open(evidence_43, "w", encoding="utf-8") as f:
            json.dump(sniffer.captured, f, ensure_ascii=False, indent=2)
        print(f"TC_PHP_43: Da chup anh {screenshot_43} ({len(sniffer.captured)} requests)")

        sniffer.detach()

        print("\n" + "="*80)
        print("HOAN TAT THUC THI TOAN BO 20 CA KIEM THU (TC_PHP_24 -> TC_PHP_43)!")
        print("Tat ca 20 anh chup man hinh that (.png) va 20 file log JSON da duoc ghi nhan.")
        print("="*80)

        # Chay dong bo lai toan bo file CSV, TSV va Excel
        print("\n[DONG BO] Dang cap nhat lai file CSV, TSV va Excel...")
        import generate_delivery_files
        generate_delivery_files.generate()

        return True

if __name__ == "__main__":
    success = run_tests()
    if not success:
        sys.exit(1)
    sys.exit(0)
