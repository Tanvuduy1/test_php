# 05. NGUYÊN TẮC KIỂM TRA CHÉO VÀ GIẢI QUYẾT XUNG ĐỘT (CROSS-VALIDATION & CONFLICT RESOLUTION)

> **CẤP ĐỘ QUYỀN HẠN:** `READ-ONLY CHO AGENT`. Bổ sung vào hệ thống kiểm soát chất lượng.  
> **PHIÊN BẢN:** 1.0.0 | **NGÀY HIỆU LỰC:** 14/10/2026

---

## 1. NGUYÊN TẮC BẤT BIẾN VỀ KIỂM TRA CHÉO (CROSS-VALIDATION INVARIANTS)

1. **Kiểm tra toàn vẹn định danh (ID Uniqueness & Sequence):**
   - Trước khi đề xuất bất kỳ Test Case ID nào mới, Agent bắt buộc phải chạy script quét tự động 100% các dòng của file dữ liệu hiện hữu để phát hiện:
     * Trùng lặp mã (Duplicate ID).
     * Đứt gãy số thứ tự (Sequence gap).
   - Tuyệt đối không đọc lướt một vài dòng đầu/cuối rồi suy đoán tổng thể.

2. **Kiểm tra tính nhất quán 3 bên (Triangular Consistency):**
   Mọi bản ghi kiểm thử phải khớp nhau 100% giữa 3 nguồn:
   - **Nguồn 1:** `docs/02_TEST_SPEC.md` (Đặc tả thiết kế).
   - **Nguồn 2:** `docs/04_STATE_CHECKPOINT.md` (Nhật ký trạng thái).
   - **Nguồn 3:** File dữ liệu thực tế `Test_case_D.Tan_30_9 - Test_case.csv`.

---

## 2. QUY TRÌNH PHÁT HIỆN VÀ GIẢI QUYẾT XUNG ĐỘT (CONFLICT RESOLUTION WORKFLOW)

Khi phát hiện dữ liệu xung đột (ví dụ: phát hiện 2 dòng cùng mang mã `TC_PHP_08` trong file gốc):
1. **DỪNG LẠI NGAY LẬP TỨC (HALT):** Không tự ý sửa đè dữ liệu cũ của Tester nếu chưa được cấp phép.
2. **CÔNG KHAI XUNG ĐỘT:** Báo cáo chi tiết vị trí xung đột (dòng, nội dung, mức độ ảnh hưởng) lên bảng nhật ký và thông báo cho Tester.
3. **ĐỀ XUẤT PHƯƠNG ÁN XỬ LÝ:**
   - *Phương án A (Tôn trọng lịch sử):* Đánh lại mã từ điểm xung đột (`TC_PHP_08_A`, `TC_PHP_08_B` hoặc tăng dần).
   - *Phương án B (Bảo lưu dữ liệu cũ):* Giữ nguyên dữ liệu cũ, chỉ đánh số tiếp nối an toàn từ ID cao nhất tiếp theo (`TC_PHP_14`).
4. **CHỜ QUYẾT ĐỊNH CỦA TESTER:** Chỉ hành động khi người dùng đã lựa chọn giải pháp.
