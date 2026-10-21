# -*- coding: utf-8 -*-
"""
Script dong bo ket qua kiem thu tu evidence/all_test_results.json
vao:
1. Test_case_D.Tan_30_9 - Test_case.csv
2. Test_case_Execution_Copy.csv
3. docs/04_STATE_CHECKPOINT.md
"""
import os
import sys
import json
import csv
import re
from datetime import datetime

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CSV_MAIN = r"D:\Tan\work\test_php\Test_case_D.Tan_30_9 - Test_case.csv"
CSV_COPY = r"D:\Tan\work\test_php\Test_case_Execution_Copy.csv"
SPEC_FILE = r"D:\Tan\work\test_php\docs\02_TEST_SPEC.md"
CHECKPOINT_FILE = r"D:\Tan\work\test_php\docs\04_STATE_CHECKPOINT.md"
RESULTS_FILE = r"D:\Tan\work\test_php\evidence\all_test_results.json"

def load_spec_items():
    with open(SPEC_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"### (TC_PHP_\d+):\s*(.*?)\r?\n- \*\*Module / Chức năng:\*\*\s*(.*?)\s*/\s*(.*?)\r?\n- \*\*Mô tả:\*\*\s*(.*?)\r?\n- \*\*Các bước thực hiện:\*\*\s*(.*?)\r?\n- \*\*Expected Result:\*\*\s*(.*?)\r?\n"
    items = {}
    for m in re.finditer(pattern, content, re.DOTALL):
        tc_id = m.group(1).strip()
        items[tc_id] = {
            "title": m.group(2).strip(),
            "module": m.group(3).strip(),
            "chuc_nang": m.group(4).strip(),
            "mo_ta": m.group(5).strip(),
            "cac_buoc": m.group(6).strip(),
            "expected": m.group(7).strip()
        }
    return items

def sync():
    if not os.path.exists(RESULTS_FILE):
        print(f"[LOI] Khong tim thay file ket qua: {RESULTS_FILE}")
        return False

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        results = json.load(f)

    spec_items = load_spec_items()

    # Doc file CSV goc
    with open(CSV_MAIN, "r", encoding="utf-8", errors="replace") as f:
        reader = list(csv.reader(f))

    # Loai bo cac dong cu neu da co TC_PHP_14 tro di de tranh trung lap
    filtered_rows = []
    for row in reader:
        if len(row) > 0 and row[0].startswith("TC_PHP_") and int(row[0].replace("TC_PHP_", "")) >= 14:
            continue
        filtered_rows.append(row)

    # Them cac ban ghi moi tu TC_PHP_14 den TC_PHP_23
    pass_count = 0
    fail_count = 0
    blocked_count = 0

    for i in range(14, 24):
        tc_id = f"TC_PHP_{i}"
        res = results.get(tc_id, {
            "status": "Blocked",
            "actual": "Chua co du lieu thuc thi thuc te.",
            "feedback": "Thieu phien hoac chua thuc thi.",
            "evidence": "-"
        })
        spec = spec_items.get(tc_id, {
            "module": "Ticket",
            "chuc_nang": "Chuc nang Ticket",
            "mo_ta": "Kiem tra khong phat sinh loi PHP.",
            "cac_buoc": "Thuc hien kiem thu qua DevTools Network.",
            "expected": "HTTP 200, sach loi PHP."
        })

        st = res["status"]
        if st == "Pass":
            pass_count += 1
        elif st == "Fail":
            fail_count += 1
        else:
            blocked_count += 1

        new_row = [
            tc_id,
            spec["module"],
            spec["chuc_nang"],
            spec["mo_ta"],
            spec["cac_buoc"],
            spec["expected"],
            res["actual"],
            res["evidence"],
            "-",
            st,
            res["feedback"],
            "", "", "", ""
        ]
        filtered_rows.append(new_row)

    # Ghi lai vao ca 2 file CSV
    for target_csv in [CSV_MAIN, CSV_COPY]:
        with open(target_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(filtered_rows)
        print(f"[DONG BO] Da cap nhat: {target_csv} ({len(filtered_rows)} dong)")

    # Cap nhat docs/04_STATE_CHECKPOINT.md
    now_str = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
        chk = f.read()

    # Cap nhat thoi gian
    chk = re.sub(r"> \*\*CẬP NHẬT LẦN CUỐI:\*\*.*", f"> **CẬP NHẬT LẦN CUỐI:** {now_str}", chk)

    # Cap nhat bang trang thai
    old_row = r"\| \*\*TC_PHP_14 ➔ TC_PHP_23\*\* \| \*\*Ticket \(`c=ticket&id=default`\)\*\* \| \*\*10\*\* \| \d+ \| \d+ \| \d+ \| \*\*?\d+\*? \| .*"
    new_status_line = f"| **TC_PHP_14 ➔ TC_PHP_23** | **Ticket (`c=ticket&id=default`)** | **10** | **{pass_count}** | **{fail_count}** | **{blocked_count}** | **0** | **ĐÃ HOÀN TẤT THỰC THI VÀ XUẤT BẰNG CHỨNG.** |"
    chk = re.sub(old_row, new_status_line, chk)

    # Cap nhat Giai doan
    chk = chk.replace("`STAGE_B_COMPLETED` ➔ Chuyển sang `STAGE_C_EXECUTION` (Thực thi kiểm thử).",
                      "`STAGE_E_REPORT_COMPLETED` (Đã hoàn tất toàn bộ quy trình kiểm thử và xuất báo cáo).")

    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        f.write(chk)

    print(f"[DONG BO] Da cap nhat checkpoint tai: {CHECKPOINT_FILE}")
    print(f"[KET QUA] Pass: {pass_count} | Fail: {fail_count} | Blocked: {blocked_count}")
    return True

if __name__ == "__main__":
    sync()
