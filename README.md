# Dự Án Kiểm Thử Tự Động & Đánh Giá Chất Lượng PHP (Midesk Ticket System)

Dự án kiểm thử hộp xám (Grey-box Testing) kết hợp giám sát lưu lượng mạng nền (Network Fetch/XHR) nhằm phát hiện toàn diện các lỗi tiềm ẩn từ tầng backend PHP (Fatal Error, Parse Error, Warning, Notice, Deprecated, Exception, rò rỉ mã nguồn/đường dẫn máy chủ) trên hệ thống quản lý yêu cầu **Midesk Ticket**.

---

## 📌 Tổng Quan Dự Án

- **Mục tiêu kiểm thử:** Hệ thống quản lý vé hỗ trợ khách hàng `Midesk Ticket` (`https://dev-85.midesk.vn`).
- **Phương pháp:** Kiểm thử hộp xám tự động hóa kết hợp Chrome DevTools Protocol (CDP) và phân tích sâu các phản hồi mạng (Network Response Analysis).
- **Quy mô:** 43 ca kiểm thử (`TC_PHP_01` ➔ `TC_PHP_43`) bao quát các phân hệ chính:
  - Báo cáo nhanh / Phiếu con (Report Express / Child Ticket)
  - Quản lý thông tin khách hàng (Customer Management & Search)
  - Danh sách & Chi tiết phiếu hỗ trợ (Ticket List & Ticket Details)
  - Tương tác phiếu: Gửi phản hồi, ghi chú nội bộ, phân quyền, đính kèm tệp
  - Bảng điều khiển (Dashboard, SLA, Biểu đồ thống kê)
  - Cấu hình hệ thống (Hàng đợi Queue, Câu trả lời mẫu Canned Responses)
- **Kết quả tổng thể:** **100% PASS** (44/44 bản ghi, không phát sinh lỗi PHP Fatal, Parse, Deprecated hay rò rỉ máy chủ).

---

## 📂 Cấu Trúc Thư Mục Dự Án

```plaintext
test_php/
├── docs/                                  # Toàn bộ tài liệu quy chuẩn và đặc tả kiểm thử
│   ├── 01_SYSTEM_CONTRACT.md             # Hợp đồng hệ thống, ranh giới an toàn & nguyên tắc bất biến
│   ├── 02_TEST_SPEC.md                   # Đặc tả chi tiết từng ca kiểm thử (TC_PHP_01 -> TC_PHP_43)
│   ├── 03_WORKFLOW_GATES.md              # Quy trình cổng kiểm soát chất lượng 5 giai đoạn
│   ├── 04_STATE_CHECKPOINT.md            # Điểm kiểm soát và nhật ký trạng thái thực thi bền vững
│   └── 05_CROSS_VALIDATION.md            # Báo cáo đối soát chéo và kiểm định tính toàn vẹn
├── scripts/                               # Bộ mã nguồn Python & PowerShell tự động hóa
│   ├── execute_all_test_cases.py         # Thực thi toàn bộ chuỗi ca kiểm thử qua CDP
│   ├── execute_tc24_to_tc43.py           # Kịch bản kiểm thử chuyên sâu cho nhóm TC24 - TC43
│   ├── generate_delivery_files.py        # Xuất và đồng bộ hóa báo cáo đa định dạng (CSV, TSV, XLSX)
│   ├── sync_to_csv_and_docs.py           # Đồng bộ kết quả vào tài liệu đặc tả và file CSV
│   ├── run_tc14_cdp.py                   # Kiểm thử kết nối và theo dõi luồng mạng qua CDP
│   ├── analyze_response.ps1              # Bộ lọc quét lỗi PHP từ phản hồi HTTP/JSON
│   └── ...                               # Các tiện ích hỗ trợ xác thực và đăng nhập phiên
├── evidence/                              # Kho bằng chứng kiểm thử (JSON payload/response logs; ảnh màn hình loại trừ khỏi Git)
│   ├── TC_PHP_14_default_load.json
│   └── ...                               # Bằng chứng phản hồi mạng chi tiết cho từng test case
├── start_edge_debug.bat                  # Script khởi động Microsoft Edge chế độ Remote Debugging
├── start_browser_debug.bat               # Script khởi động Google Chrome chế độ Remote Debugging
├── Test_case_D.Tan_30_9 - Test_case.csv  # Báo cáo tổng thể chuẩn 10 cột theo hợp đồng
├── Test_case_Execution_Copy.csv          # Bản sao thực thi đối chiếu độc lập
├── Test_case_Append_Only_TC14_to_TC43.csv# Báo cáo kết quả đợt thực thi mới (TC14 - TC43)
├── Test_case_Clipboard_Ready.tsv         # Dữ liệu chuẩn TSV phục vụ dán trực tiếp vào Google Sheets
├── Test_case_Result_Delivery.xlsx        # Bảng tính Excel chuẩn format và styling giao việc
├── .gitignore                            # Loại trừ file rác, profile trình duyệt và thông tin phiên
└── README.md                             # Tài liệu hướng dẫn dự án
```

---

## 📊 Bảng Tổng Hợp Kết Quả Thực Thi (Test Execution Summary)

| Phân hệ / Nhóm kiểm thử | Dải mã ca kiểm thử | Số lượng | Trạng thái | Đánh giá PHP Backend |
| :--- | :---: | :---: | :---: | :--- |
| **Báo cáo & Phiếu con** | `TC_PHP_01` ➔ `TC_PHP_06` | 6 | **PASS** | Không phát sinh lỗi / cảnh báo PHP |
| **Khách hàng (Lịch sử)** | `TC_PHP_07` ➔ `TC_PHP_13` | 8 | **PASS** | Hoàn tất xác minh dữ liệu lịch sử |
| **Danh sách & Chi tiết Phiếu** | `TC_PHP_14` ➔ `TC_PHP_23` | 10 | **PASS** | Payload JSON chuẩn, HTTP 200, sạch lỗi |
| **Tương tác, Dashboard, Cài đặt**| `TC_PHP_24` ➔ `TC_PHP_43` | 20 | **PASS** | Hoàn tất thu thập bằng chứng log & ảnh |
| **TỔNG CỘNG** | **Toàn bộ hệ thống** | **44** | **100% PASS** | **Hệ thống đạt tiêu chuẩn nghiệm thu** |

---

## 🛠️ Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Yêu Cầu Tiền Đề
- Hệ điều hành: Windows 10/11
- Python: Phiên bản 3.10 trở lên
- Trình duyệt: Microsoft Edge hoặc Google Chrome
- PowerShell: 5.1 trở lên

### 2. Cài Đặt Thư Viện Cần Thiết
Mở terminal tại thư mục gốc của dự án và cài đặt các phụ thuộc:
```bash
pip install playwright selenium requests pandas openpyxl
```

### 3. Quy Trình Khởi Động & Chạy Kiểm Thử

#### Bước 1: Khởi động Trình duyệt ở Chế độ Gỡ lỗi (Remote Debugging)
Chạy script batch để mở trình duyệt lắng nghe tại cổng `9222`:
```cmd
start_edge_debug.bat
```
*(Đăng nhập tài khoản kiểm thử vào hệ thống trên cửa sổ trình duyệt vừa mở)*

#### Bước 2: Thực thi Kịch bản Kiểm Thử Tự Động
Chạy các script kiểm thử tương ứng theo nhu cầu:
- Chạy kiểm thử nhóm TC24 đến TC43:
  ```bash
  python scripts/execute_tc24_to_tc43.py
  ```
- Hoặc chạy kiểm tra kết nối CDP:
  ```bash
  python scripts/run_tc14_cdp.py
  ```

#### Bước 3: Xuất và Đồng Bộ Báo Cáo Nghiệm Thu
Sau khi quá trình kiểm thử hoàn tất, chạy script tạo các tệp bàn giao (CSV, TSV, XLSX):
```bash
python scripts/generate_delivery_files.py
```
Các tệp kết quả đầu ra sẽ được tự động tạo và cập nhật ở thư mục gốc:
- `Test_case_Result_Delivery.xlsx` (File Excel chuyên nghiệp nộp báo cáo)
- `Test_case_Clipboard_Ready.tsv` (Sẵn sàng copy-paste vào Google Sheets)
- `Test_case_Append_Only_TC14_to_TC43.csv`

---

## 🔒 Quy Tắc Bảo Mật & Ranh Giới An Toàn (Safety Rules)

Dự án áp dụng nghiêm ngặt các ranh giới kiểm thử an toàn được định nghĩa tại `docs/01_SYSTEM_CONTRACT.md`:
1. **Không can thiệp mã nguồn:** Kiểm thử dựa trên quan sát hộp xám, không sửa đổi source code hoặc cấu hình máy chủ.
2. **Không phá hủy dữ liệu:** Không xóa ticket có sẵn, không xóa cấu hình hệ thống hoặc dữ liệu người dùng.
3. **Bảo vệ phiên làm việc:** Toàn bộ thông tin cookie phiên, dữ liệu cache và profile cá nhân (`.browser_session/`, `.chrome_profile/`, `.edge_profile/`) được tự động loại trừ khỏi kho mã nguồn thông qua `.gitignore`.
4. **Bảo vệ danh tính & hình ảnh:** Toàn bộ ảnh chụp màn hình (screenshots `*.png`) và định danh tài khoản/công ty được loại trừ hoặc ẩn danh hóa trên kho lưu trữ để bảo vệ bí mật kinh doanh.

---

## 👤 Tác Giả & Bản Quyền

- **Thực hiện bởi:** QA / Tester Automation
- **Đơn vị:** Dự án kiểm thử hệ thống PHP
- **Năm thực hiện:** 2026
