# 01. HỢP ĐỒNG HỆ THỐNG VÀ RANH GIỚI KIỂM THỬ (SYSTEM CONTRACT)

> **CẤP ĐỘ QUYỀN HẠN:** `READ-ONLY CHO AGENT`. Chỉ người dùng (Tester/Admin) mới có quyền sửa đổi tài liệu này.  
> **PHIÊN BẢN:** 1.0.0 | **NGÀY HIỆU LỰC:** 14/10/2026

---

## 1. NGUYÊN TẮC BẤT BIẾN VỀ NGÔN NGỮ (LANGUAGE INVARIANT)
1. **Toàn bộ quá trình làm việc và các tài liệu/báo cáo phải sử dụng tiếng Việt.**
2. Không tự ý tạo tài liệu, báo cáo hoặc dữ liệu bằng tiếng Anh.
3. Các thuật ngữ kỹ thuật, thông báo lỗi nguyên bản (Raw Error), mã trạng thái HTTP (`HTTP 200`, `HTTP 500`...) và các mã trạng thái quy ước (`PASS`, `FAIL`, `BLOCKED`, `NOT RUN`, `UNDEFINED`) được giữ nguyên để đảm bảo tính chính xác kỹ thuật, nhưng phải có phần giải thích bằng tiếng Việt.
4. Mọi thông báo lỗi từ website bằng tiếng Anh phải được lưu nguyên văn làm bằng chứng kèm diễn giải tiếng Việt, không tự dịch làm méo mó lỗi gốc.

---

## 2. ĐỐI TƯỢNG VÀ PHẠM VI KIỂM THỬ ĐƯỢC PHÊ DUYỆT

### 2.1. Mục tiêu
- **Website mục tiêu:** `https://dev-85.midesk.vn/vi?c=ticket&id=default`
- **Loại kiểm thử:** Kiểm thử hộp xám (Grey-box Testing) trên giao diện Web và các cuộc gọi mạng nền (Network Fetch/XHR), tập trung phát hiện các lỗi phát sinh từ tầng backend PHP (Fatal Error, Parse Error, Warning, Notice, Deprecated, Exception, rò rỉ mã nguồn/đường dẫn máy chủ).
- **Mẫu báo cáo hợp đồng:** Dựa trên file mẫu thực tế `Test_case_D.Tan_30_9 - Test_case.csv` (đồng bộ với Google Sheet mục tiêu).

### 2.2. Các hành động BỊ CẤM TUYỆT ĐỐI (Safety Invariants)
- **CẤM** can thiệp chỉnh sửa mã nguồn hoặc cấu hình web server.
- **CẤM** thực hiện các hành động phá hủy dữ liệu: không xóa ticket có sẵn, không xóa cấu hình hàng đợi (queue), không xóa người dùng.
- **CẤM** gửi tin nhắn/thư điện tử (Email, SMS, Zalo, Webhook) thật ra ngoài cho khách hàng thực.
- **CẤM** khai thác lỗ hổng bảo mật chuyên sâu (như SQL Injection khai thác phá hủy DB, tấn công DoS/DDoS).
- **CẤM** lưu trữ, thu thập hoặc làm lộ mật khẩu, cookie phiên làm việc của người dùng vào tài liệu công khai.

---

## 3. HỢP ĐỒNG DỮ LIỆU ĐẦU RA (CSV OUTPUT CONTRACT)

File báo cáo đầu ra phải tuân thủ nghiêm ngặt cấu trúc 10 cột của bảng tính sau:
1. `Test Case ID`: Mã định danh ca kiểm thử (bắt đầu bằng `TC_PHP_xx`).
2. `Module`: Phân hệ chức năng (ví dụ: `Ticket / Danh sách phiếu`, `Ticket / Chi tiết`).
3. `Chức năng`: Tên chức năng cụ thể được kiểm tra.
4. `Mô tả`: Mục tiêu kiểm thử (phải nêu rõ việc kiểm tra không phát sinh PHP Error / Deprecated / Warning / Notice / Fatal).
5. `Các bước thực hiện`: Các bước từng bước, bao gồm thao tác UI và bước mở F12 Network Fetch/XHR để kiểm tra Response.
6. `Expected Result`: Kết quả mong đợi chuẩn xác (ví dụ: HTTP 200, JSON hợp lệ, không chứa chuỗi lỗi PHP).
7. `Actual Result / Đánh giá`: Kết quả thực tế quan sát được (phải dựa trên bằng chứng, không suy diễn).
8. `Log/Screenshot/Video`: Tên hoặc đường dẫn tệp bằng chứng lưu tại thư mục `evidence/`.
9. `Status`: Chỉ chấp nhận 4 giá trị: `Pass`, `Fail`, `Blocked`, `Not Run`.
10. `Phản hồi`: Ghi chú hoặc diễn giải chi tiết bằng tiếng Việt.

---

## 4. QUY TẮC BẢO TOÀN TÍNH CHÂN THỰC (TRUTH INTEGRITY)
- **Không tự tạo kết quả giả (No Hallucination):** Agent tuyệt đối không tự đánh dấu `Pass` hoặc `Fail` nếu chưa có bằng chứng cụ thể (Network response hoặc ảnh chụp màn hình).
- **Khi công cụ lỗi hoặc thiếu quyền:** Agent phải chuyển trạng thái ca kiểm thử sang `Blocked`, ghi rõ lý do vào nhật ký và yêu cầu Tester trợ giúp, không được tự suy đoán kết quả.
