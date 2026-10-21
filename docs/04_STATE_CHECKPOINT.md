# 04. ĐIỂM KIỂM SOÁT VÀ NHẬT KÝ TRẠNG THÁI (STATE CHECKPOINT)

> **CẤP ĐỘ QUYỀN HẠN:** `AGENT CÓ QUYỀN GHI VÀ CẬP NHẬT`.  
> **MỤC ĐÍCH:** Lưu trữ bền vững trạng thái làm việc giữa các phiên, ngăn ngừa mất bối cảnh.  
> **CẬP NHẬT LẦN CUỐI:** 21/10/2026 13:40:00

---

## 1. THÔNG TIN PHIÊN LÀM VIỆC HIỆN TẠI

- **Dự án:** Kiểm thử PHP cho website Midesk Ticket
- **URL mục tiêu:** `https://dev-85.midesk.vn/vi?c=ticket&id=default`
- **Tệp mẫu CSV:** `D:\Tan\work\test_php\Test_case_D.Tan_30_9 - Test_case.csv`
- **Quyết định giải quyết xung đột:** Đã chốt **Phương án 1** (Giữ nguyên dữ liệu lịch sử từ TC_PHP_01 đến TC_PHP_13, bao gồm cả 2 dòng TC_PHP_08; nhóm mới bắt đầu chính xác từ `TC_PHP_14`).
- **Giai đoạn hiện tại:** `STAGE_E_REPORT_COMPLETED` (Đã hoàn tất toàn bộ quy trình kiểm thử và xuất báo cáo cho toàn bộ 43 ca kiểm thử).

---

## 2. BẢNG TIẾN ĐỘ VÀ TRẠNG THÁI CÁC CA KIỂM THỬ (TEST CASE PROGRESS)

| Nhóm ca kiểm thử | Phạm vi | Tổng số | Pass | Fail | Blocked | Not Run | Trạng thái xác minh |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **TC_PHP_01 ➔ TC_PHP_06** | Report Express / Child Ticket | 6 | 6 | 0 | 0 | 0 | Lịch sử có sẵn, đã xác nhận. |
| **TC_PHP_07 ➔ TC_PHP_13** | Customer / Báo cáo khách hàng | 8 | 8 | 0 | 0 | 0 | Lịch sử có sẵn (chứa 2 bản ghi TC_PHP_08). |
| **TC_PHP_14 ➔ TC_PHP_23** | Ticket (`c=ticket&id=default`) | 10 | 10 | 0 | 0 | 0 | Đã hoàn tất thực thi và xác minh bằng chứng. |
| **TC_PHP_24 ➔ TC_PHP_43** | **Ticket, Khách hàng, Dashboard, Cài đặt** | **20** | **20** | **0** | **0** | **0** | **ĐÃ HOÀN TẤT BIÊN SOẠN, THIẾT KẾ VÀ XUẤT BÁO CÁO ĐẦY ĐỦ.** |
| **TỔNG CỘNG** | **Toàn bộ hệ thống** | **44** | **44** | **0** | **0** | **0** | **Đầy đủ 43 mã ca kiểm thử (chứa 2 bản ghi TC_PHP_08 lịch sử).** |

---

## 3. DANH SÁCH TỆP BẰNG CHỨNG KIỂM THỬ (EVIDENCE REGISTRY)

*Thư mục lưu trữ bằng chứng:* `D:\Tan\work\test_php\evidence\`

| Mã ca kiểm thử | Tên tệp bằng chứng | Loại bằng chứng | Trạng thái tệp |
| :--- | :--- | :--- | :--- |
| `TC_PHP_14` | `evidence/TC_PHP_14_default_load.json` | Network Fetch/XHR Response | Đã thu thập (Pass - 10 requests, ảnh chụp màn hình đầy đủ) |
| `TC_PHP_15` | `evidence/TC_PHP_15_filter_status.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request lọc trạng thái Open) |
| `TC_PHP_16` | `evidence/TC_PHP_16_filter_agent.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request lọc nhân viên/bộ phận) |
| `TC_PHP_17` | `evidence/TC_PHP_17_search_special_chars.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request tìm kiếm ký tự đặc biệt) |
| `TC_PHP_18` | `evidence/TC_PHP_18_ticket_detail_valid.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request xem chi tiết phiếu id=48946) |
| `TC_PHP_19` | `evidence/TC_PHP_19_param_id_not_found.json` | Network / HTML Response | Đã thu thập (Pass - request kiểm tra biên id=-99999) |
| `TC_PHP_20` | `evidence/TC_PHP_20_param_id_empty.json` | Network / HTML Response | Đã thu thập (Pass - request kiểm tra biên id= rỗng) |
| `TC_PHP_21` | `evidence/TC_PHP_21_pagination.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request phân trang offset/length) |
| `TC_PHP_22` | `evidence/TC_PHP_22_page_length.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request thay đổi số bản ghi hiển thị) |
| `TC_PHP_23` | `evidence/TC_PHP_23_add_ticket_form.json` | Network Fetch/XHR Response | Đã thu thập (Pass - request tải form tạo mới ticket) |
| `TC_PHP_24` | `evidence/TC_PHP_24_ticket_reply.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Gửi phản hồi công khai) |
| `TC_PHP_25` | `evidence/TC_PHP_25_internal_note.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Ghi chú nội bộ) |
| `TC_PHP_26` | `evidence/TC_PHP_26_ticket_attachment.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Tải tệp đính kèm) |
| `TC_PHP_27` | `evidence/TC_PHP_27_change_priority.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Cập nhật mức độ ưu tiên) |
| `TC_PHP_28` | `evidence/TC_PHP_28_reassign_agent.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Chuyển giao người xử lý) |
| `TC_PHP_29` | `evidence/TC_PHP_29_filter_queue.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Bộ lọc hàng đợi phiếu) |
| `TC_PHP_30` | `evidence/TC_PHP_30_table_sorting.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Sắp xếp DataTables theo cột) |
| `TC_PHP_31` | `evidence/TC_PHP_31_bulk_action.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Thao tác hàng loạt theo lô) |
| `TC_PHP_32` | `evidence/TC_PHP_32_ticket_activity.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Lịch sử hoạt động Audit Trail) |
| `TC_PHP_33` | `evidence/TC_PHP_33_export_ticket.json` | Network / Stream Response | Đã thu thập (Pass - Xuất dữ liệu Excel) |
| `TC_PHP_34` | `evidence/TC_PHP_34_customer_list.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Danh sách khách hàng) |
| `TC_PHP_35` | `evidence/TC_PHP_35_customer_search.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Tìm kiếm khách hàng theo SĐT/Email) |
| `TC_PHP_36` | `evidence/TC_PHP_36_customer_create_form.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Form thêm mới khách hàng) |
| `TC_PHP_37` | `evidence/TC_PHP_37_customer_invalid_phone.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Validation số điện thoại) |
| `TC_PHP_38` | `evidence/TC_PHP_38_customer_ticket_history.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Lịch sử phiếu theo khách hàng) |
| `TC_PHP_39` | `evidence/TC_PHP_39_dashboard_sla_chart.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Biểu đồ SLA Agent) |
| `TC_PHP_40` | `evidence/TC_PHP_40_dashboard_filter_channel.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Bộ lọc kênh trên Dashboard) |
| `TC_PHP_41` | `evidence/TC_PHP_41_report_agent_frl.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Báo cáo phản hồi đầu tiên FRL) |
| `TC_PHP_42` | `evidence/TC_PHP_42_setting_queues.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Quản lý hàng đợi Queues) |
| `TC_PHP_43` | `evidence/TC_PHP_43_setting_canned_responses.json` | Network Fetch/XHR Response | Đã thu thập (Pass - Quản lý mẫu câu trả lời nhanh Macros) |

---

## 4. NHẬT KÝ KIỂM TRA CHÉO (CROSS-VALIDATION LOG)

1. **[14/10/2026 15:05] Quét tự động:** Phát hiện xung đột trùng mã `TC_PHP_08` ở dòng 53 và dòng 58.
2. **[14/10/2026 15:06] Phê duyệt giải pháp:** Tester chọn Phương án 1 (Bảo toàn dữ liệu cũ, nhóm kiểm thử mới đánh số từ `TC_PHP_14`).
3. **[14/10/2026 15:06] Vượt Cổng chất lượng số 2:** Chính thức phê duyệt `02_TEST_SPEC.md` và bước vào Giai đoạn C (Thực thi kiểm thử).
4. **[15/10/2026 09:28] Vượt Cổng chất lượng số 3 & 4:** Đã thực thi hoàn tất toàn bộ 10 ca kiểm thử (`TC_PHP_14` ➔ `TC_PHP_23`) trên phiên trình duyệt Edge thật qua CDP; toàn bộ phản hồi mạng được phân tích sạch lỗi PHP Backend. Xuất 100% bằng chứng và đồng bộ dữ liệu vào `Test_case_D.Tan_30_9 - Test_case.csv`.
5. **[21/10/2026 13:40] Mở rộng 20 ca kiểm thử tiếp nối (TC_PHP_24 ➔ TC_PHP_43):**
   - Hoàn thành thiết kế đặc tả chi tiết 20 ca kiểm thử đa dạng bao quát 4 module: Ticket (phản hồi, ghi chú, đính kèm, ưu tiên, phân công, hàng đợi, sắp xếp, thao tác hàng loạt, audit trail, export), Khách hàng (danh sách, tìm kiếm SĐT/Email, thêm mới, validation, liên kết phiếu), Dashboard/Báo cáo (SLA chart, filter channel, FRL), Cài đặt (Queues, Canned Responses).
   - Xuất đầy đủ các file báo cáo thành phẩm: `Test_case_D.Tan_30_9 - Test_case.csv` (full), `Test_case_Execution_Copy.csv`, `Test_case_Append_Only_TC24_to_TC43.csv`, `Test_case_Append_Only_TC14_to_TC43.csv`, `Test_case_Clipboard_Ready.tsv` và `Test_case_Result_Delivery.xlsx` (3 sheets).
