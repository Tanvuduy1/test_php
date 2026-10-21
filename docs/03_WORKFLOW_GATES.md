# 03. QUY TRÌNH THỰC THI VÀ CỔNG CHẤT LƯỢNG (WORKFLOW & QUALITY GATES)

> **CẤP ĐỘ QUYỀN HẠN:** `READ-ONLY CHO AGENT`. Quy định các điều kiện chuyển trạng thái nghiêm ngặt.  
> **PHIÊN BẢN:** 1.0.0 | **NGÀY HIỆU LỰC:** 14/10/2026

---

## 1. MÔ HÌNH CHUYỂN TRẠNG THÁI (STATE MACHINE)

Quy trình làm việc của Agent gồm 5 trạng thái bắt buộc tuần tự:

```
[STAGE_A: KHẢO SÁT] ➔ (CỔNG 1) ➔ [STAGE_B: THIẾT KẾ SPEC] ➔ (CỔNG 2) ➔ [STAGE_C: THỰC THI KIỂM THỬ] ➔ (CỔNG 3) ➔ [STAGE_D: XÁC MINH & BẰNG CHỨNG] ➔ (CỔNG 4) ➔ [STAGE_E: XUẤT BÁO CÁO]
```

---

## 2. QUY ĐỊNH CÁC CỔNG CHẤT LƯỢNG (QUALITY GATES)

Agent **KHÔNG ĐƯỢC PHÉP** tự ý nhảy cóc sang giai đoạn tiếp theo nếu chưa vượt qua điều kiện kiểm tra tại các Cổng chất lượng sau:

### CỔNG 1: Khảo sát ➔ Thiết kế ca kiểm thử (Gate A ➔ B)
- **Tiêu chuẩn vượt qua:**
  1. Đã xác định rõ URL mục tiêu, loại kiểm thử (Hộp xám giao diện & Network).
  2. Đã đọc và hiểu trọn vẹn cấu trúc 10 cột của tệp template CSV.
  3. Đã có xác nhận của người dùng (Tester) cho phép bắt đầu lập kịch bản.

### CỔNG 2: Thiết kế ➔ Thực thi kiểm thử (Gate B ➔ C)
- **Tiêu chuẩn vượt qua:**
  1. Toàn bộ các ca kiểm thử trong `02_TEST_SPEC.md` phải có đầy đủ: Mã ID, Tiền điều kiện, Các bước rõ ràng (chỉ định rõ URL API/Fetch cần bắt), Kết quả mong đợi và Tên file bằng chứng dự kiến.
  2. Người dùng (Tester) đã kiểm tra và gửi xác nhận phê duyệt danh sách Test Case này.
  - *Nếu chưa duyệt:* Agent phải dừng lại ở trạng thái chờ (`WAITING_APPROVAL`).

### CỔNG 3: Thực thi ➔ Xác minh bằng chứng (Gate C ➔ D)
- **Tiêu chuẩn vượt qua:**
  1. Mỗi ca kiểm thử được đánh dấu `Pass` hoặc `Fail` bắt buộc phải có tệp bằng chứng tồn tại thực tế trong thư mục `evidence/` (ví dụ: `evidence/TC_PHP_09_get_data_table.json`).
  2. Trường hợp không thể thực thi (mất kết nối, lỗi trình duyệt, thiếu quyền), bắt buộc gán nhãn `Blocked` kèm lý do cụ thể. Cấm tuyệt đối việc suy đoán `Pass`.

### CỔNG 4: Xác minh ➔ Xuất báo cáo và Nghiệm thu (Gate D ➔ E)
- **Tiêu chuẩn vượt qua:**
  1. File CSV kết quả phải đồng bộ 100% về số lượng ca kiểm thử với tài liệu đặc tả và bảng trạng thái `04_STATE_CHECKPOINT.md`.
  2. Toàn bộ nội dung báo cáo sử dụng 100% tiếng Việt đúng chuẩn theo quy định tại Hợp đồng hệ thống.
  3. Tất cả các liên kết đến tệp bằng chứng đều hợp lệ và truy cập được trên máy cục bộ.

---

## 3. CƠ CHẾ XỬ LÝ NGOẠI LỆ VÀ SỰ CỐ (ERROR HANDLING)

1. **Khi công cụ tự động / Script bị lỗi:**
   - Dừng hành động ngay lập tức.
   - Ghi lại nhật ký lỗi vào `04_STATE_CHECKPOINT.md` (mã lỗi, bước thất bại).
   - Chuyển trạng thái ca kiểm thử tương ứng thành `Blocked`.
   - Thông báo rõ ràng cho người dùng để yêu cầu can thiệp thủ công hoặc cấp quyền.
2. **Khi phát hiện phản hồi trả về lỗi PHP:**
   - Lưu trọn vẹn chuỗi Response (Body + Headers) thành tệp `.json` hoặc `.txt` vào thư mục `evidence/`.
   - Trích xuất dòng thông báo lỗi gốc, vị trí file PHP và số dòng bị lỗi (nếu có lộ trong stack trace).
   - Đánh dấu trạng thái ca kiểm thử là `Fail`.
   - Dịch nghĩa và giải thích lỗi bằng tiếng Việt vào cột `Actual Result / Đánh giá` và `Phản hồi`.
