# 02. ĐẶC TẢ CA KIỂM THỬ MODULE PHIẾU (TEST SPECIFICATION - TICKET MODULE)

> **CẤP ĐỘ QUYỀN HẠN:** `ĐỀ XUẤT CHO TESTER DUYỆT`.  
> **ĐỐI TƯỢNG:** Màn hình Phiếu yêu cầu hỗ trợ (`https://dev-85.midesk.vn/vi?c=ticket&id=default`)  
> **QUY ƯỚC MÃ ĐỊNH DANH:** Tiếp nối file template thực tế từ **`TC_PHP_14`** đến **`TC_PHP_23`** (Vì template đã có đến `TC_PHP_13`).  
> **MỤC TIÊU:** Phát hiện các lỗi PHP (Notice, Warning, Deprecated, Fatal error, Undefined index/property) qua Network Fetch/XHR Response.

---

## MA TRẬN 10 CA KIỂM THỬ TIẾP NỐI (TC_PHP_14 ➔ TC_PHP_23)

### TC_PHP_14: Tải màn hình danh sách Ticket mặc định (`id=default`)
- **Module / Chức năng:** Ticket / Tải danh sách mặc định
- **Mô tả:** Kiểm tra hệ thống tải giao diện danh sách phiếu mặc định không phát sinh lỗi PHP trong các request khởi tạo.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab `Network` > bật lọc `Fetch/XHR` và xóa log cũ.
  2. Truy cập URL: `https://dev-85.midesk.vn/vi?c=ticket&id=default`.
  3. Chờ bảng danh sách phiếu và các thanh menu trạng thái bên trái tải xong.
  4. Kiểm tra các request AJAX khởi tạo: `getDataTable`, `reload_count_ticket`, `getCountQueues`.
  5. Mở tab `Response` của từng request, tìm kiếm các từ khóa: `PHP Error`, `Warning`, `Deprecated`, `Notice`, `Fatal error`, `Undefined`.
- **Expected Result:** Các request trả mã HTTP 200, nội dung JSON hợp lệ, không chứa bất kỳ chuỗi thông báo lỗi PHP nào.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_14_default_load.json`

---

### TC_PHP_15: Lọc Ticket theo Trạng thái (Mới, Đang xử lý, Chờ phản hồi, Đóng)
- **Module / Chức năng:** Ticket / Bộ lọc trạng thái phiếu
- **Mô tả:** Kiểm tra không phát sinh PHP Error/Warning khi chuyển đổi qua lại giữa các trạng thái ticket.
- **Các bước thực hiện:**
  1. Bật DevTools > Network > Fetch/XHR, xóa log cũ.
  2. Trên thanh trạng thái bên trái (hoặc dropdown trạng thái), bấm chọn lần lượt: "Mới" -> "Đang xử lý" -> "Đã đóng".
  3. Bắt các request gửi lên (thường là `getDataTable` với tham số `status` hoặc `filter`).
  4. Kiểm tra Response của từng request tìm lỗi PHP.
- **Expected Result:** Response trả về danh sách phiếu tương ứng theo trạng thái, HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_15_filter_status.json`

---

### TC_PHP_16: Lọc Ticket theo Agent phụ trách
- **Module / Chức năng:** Ticket / Lọc theo nhân viên xử lý
- **Mô tả:** Kiểm tra không phát sinh lỗi PHP (Undefined array key, SQL Exception) khi lọc phiếu theo một Agent cụ thể.
- **Các bước thực hiện:**
  1. Mở DevTools > Network > Fetch/XHR.
  2. Bấm vào bộ lọc Agent, chọn 1 nhân viên cụ thể có nhiều phiếu và 1 nhân viên chưa có phiếu nào.
  3. Kiểm tra request API lọc dữ liệu.
  4. Kiểm tra Response tìm lỗi PHP backend.
- **Expected Result:** Trả về danh sách phiếu đúng của Agent đó (hoặc mảng rỗng `[]` nếu không có phiếu), không sinh Warning/Notice.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_16_filter_agent.json`

---

### TC_PHP_17: Tìm kiếm Ticket bằng từ khóa đặc biệt
- **Module / Chức năng:** Ticket / Tìm kiếm từ khóa
- **Mô tả:** Kiểm tra backend xử lý an toàn các ký tự đặc biệt, không phát sinh lỗi cú pháp SQL hoặc PHP String handling.
- **Các bước thực hiện:**
  1. Mở DevTools > Network > Fetch/XHR.
  2. Nhập vào ô tìm kiếm các chuỗi: `'`, `"`, `%`, `<script>`, `&amp;`, chuỗi tiếng Việt có dấu dài.
  3. Nhấn Enter hoặc nút Tìm kiếm.
  4. Mở Response của request tìm kiếm (`search` hoặc `getDataTable`).
- **Expected Result:** Hệ thống lọc an toàn, trả về kết quả rỗng hoặc khớp từ khóa, HTTP 200, không bị lỗi PHP 500 hay crash query.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_17_search_special_chars.json`

---

### TC_PHP_18: Mở xem chi tiết một Ticket hợp lệ
- **Module / Chức năng:** Ticket / Chi tiết phiếu
- **Mô tả:** Kiểm tra việc load thông tin chi tiết của 1 phiếu (timeline, lịch sử trao đổi, thông tin khách hàng) không bị lỗi PHP.
- **Các bước thực hiện:**
  1. Bật DevTools > Network > Fetch/XHR.
  2. Click vào tiêu đề/mã của 1 ticket bất kỳ trên danh sách để mở xem chi tiết.
  3. Kiểm tra các request load nội dung: `get_ticket_detail`, `get_timeline`, `load_comment`.
  4. Mở Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Giao diện chi tiết hiển thị đầy đủ, Response trả về thông tin chi tiết sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_18_ticket_detail_valid.json`

---

### TC_PHP_19: Kiểm tra truy cập với tham số ID không tồn tại (`id=-99999`)
- **Module / Chức năng:** Ticket / Kiểm tra kiểm soát tham số đường dẫn (Boundary)
- **Mô tả:** Kiểm tra backend PHP xử lý ngoại lệ khi tham số `id` là một số âm hoặc mã phiếu không tồn tại trong hệ thống.
- **Các bước thực hiện:**
  1. Bật DevTools > Network > Fetch/XHR.
  2. Nhập trực tiếp trên thanh địa chỉ URL: `https://dev-85.midesk.vn/vi?c=ticket&id=-99999` (hoặc `id=999999999`).
  3. Nhấn Enter để tải trang.
  4. Kiểm tra trang hiển thị và Response trả về.
- **Expected Result:** Hệ thống hiển thị thông báo "Không tìm thấy dữ liệu" hoặc chuyển về trang mặc định một cách an toàn; không hiển thị màn hình lỗi cam của PHP/Xdebug hay lỗi `Call to a member function ... on null`.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_19_param_id_not_found.json`

---

### TC_PHP_20: Kiểm tra truy cập với tham số ID rỗng (`id=`)
- **Module / Chức năng:** Ticket / Kiểm tra tham số rỗng
- **Mô tả:** Kiểm tra backend PHP không phát sinh `Undefined index` hoặc `Warning: Trying to access array offset on value of type null` khi bỏ trống `id`.
- **Các bước thực hiện:**
  1. Bật DevTools > Network > Fetch/XHR.
  2. Truy cập URL: `https://dev-85.midesk.vn/vi?c=ticket&id=`.
  3. Quan sát giao diện và kiểm tra các request trong Network tab.
- **Expected Result:** Hệ thống tự động fallback về màn hình mặc định hoặc xử lý an toàn, không có PHP Warning/Notice rò rỉ.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_20_param_id_empty.json`

---

### TC_PHP_21: Phân trang danh sách Ticket (Pagination)
- **Module / Chức năng:** Ticket / Phân trang
- **Mô tả:** Kiểm tra tính toán phân trang (offset, limit) không bị lỗi chia cho 0 (`Division by zero`) hoặc lỗi mảng ngoài phạm vi.
- **Các bước thực hiện:**
  1. Mở DevTools > Network > Fetch/XHR.
  2. Kéo xuống cuối danh sách phiếu, chuyển sang trang 2, trang 3 hoặc trang cuối cùng.
  3. Mở Response của request `getDataTable` (chứa tham số `page=2`, `start=...`).
  4. Tìm kiếm từ khóa lỗi PHP.
- **Expected Result:** Tải trang mới trơn tru, Response chứa danh sách trang kế tiếp, HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_21_pagination.json`

---

### TC_PHP_22: Thay đổi số lượng bản ghi hiển thị trên mỗi trang (Page Length)
- **Module / Chức năng:** Ticket / Chọn số lượng bản ghi (10, 25, 50, 100)
- **Mô tả:** Kiểm tra backend không phát sinh lỗi bộ nhớ (`Memory limit exhausted`) hoặc lỗi vòng lặp khi chọn xem 100 ticket.
- **Các bước thực hiện:**
  1. Bật DevTools > Network > Fetch/XHR.
  2. Tại dropdown hiển thị số bản ghi, chọn hiển thị `50` hoặc `100` phiếu/trang.
  3. Bắt request tải dữ liệu.
  4. Mở Response kiểm tra mã trạng thái và nội dung.
- **Expected Result:** Tải 50/100 phiếu thành công, HTTP 200, không bị lỗi timeout hoặc PHP Fatal Error.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_22_page_length.json`

---

### TC_PHP_23: Mở form tạo mới Ticket (Tải các trường dữ liệu động)
- **Module / Chức năng:** Ticket / Tải form thêm mới
- **Mô tả:** Kiểm tra việc load các trường tùy biến (custom fields), danh mục ticket, SLA không bị lỗi PHP khi mở popup tạo mới.
- **Các bước thực hiện:**
  1. Bật DevTools > Network > Fetch/XHR.
  2. Bấm nút "Tạo mới phiếu" (hoặc dấu `+` / `Thêm phiếu`).
  3. Chờ popup hoặc form tạo phiếu hiển thị.
  4. Kiểm tra các request load form: `get_ticket_fields`, `get_categories`, `get_sla`.
  5. Mở tab Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Form hiển thị đầy đủ các trường, các request cấu hình trả về JSON hợp lệ, không có PHP Warning/Notice.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_23_add_ticket_form.json`

---

## MA TRẬN 20 CA KIỂM THỬ MỞ RỘNG TIẾP NỐI (TC_PHP_24 ➔ TC_PHP_43)

### TC_PHP_24: Gửi phản hồi công khai (Public Reply)
- **Module / Chức năng:** Ticket / Thêm phản hồi trao đổi công khai
- **Mô tả:** Kiểm tra khi Agent gửi phản hồi công khai cho khách hàng trên ticket, backend xử lý lưu trữ nội dung trao đổi, cập nhật timeline không phát sinh lỗi PHP (Undefined array key, SQL syntax error, null email header).
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Mở một phiếu bất kỳ đang ở trạng thái Open hoặc Mới.
  3. Tại khung nhập nội dung phản hồi công khai, nhập chuỗi văn bản: "Bộ phận kỹ thuật đã ghi nhận và đang xử lý yêu cầu.".
  4. Bấm nút "Gửi" (Send / Trả lời).
  5. Bắt request API lưu phản hồi (ví dụ: `save_comment` hoặc `reply`).
  6. Mở tab Response, tìm các từ khóa: `PHP Error`, `Warning`, `Notice`, `Deprecated`, `Fatal error`.
- **Expected Result:** Phản hồi được thêm vào timeline thành công, request trả mã HTTP 200, nội dung JSON hợp lệ, sạch lỗi PHP backend.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_24_ticket_reply.json`

---

### TC_PHP_25: Thêm ghi chú nội bộ (Internal Note)
- **Module / Chức năng:** Ticket / Thêm ghi chú nội bộ
- **Mô tả:** Kiểm tra tính năng thêm ghi chú riêng tư dành riêng cho nhân viên nội bộ không phát sinh lỗi PHP trong việc xử lý cờ phân quyền (private flag) và lưu dữ liệu.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại màn hình chi tiết phiếu, chuyển tab/chế độ nhập liệu sang "Ghi chú nội bộ" (Private Note).
  3. Nhập nội dung ghi chú: "Ghi chú kỹ thuật: Cần đối soát lại log hệ thống trước 17h.".
  4. Nhấn nút "Lưu ghi chú".
  5. Bắt request API lưu ghi chú (`save_internal_note` / `add_note`).
  6. Mở Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Ghi chú nội bộ hiển thị với viền vàng/khác biệt trên timeline, request trả HTTP 200, không phát sinh PHP Warning/Notice.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_25_internal_note.json`

---

### TC_PHP_26: Tải lên tệp đính kèm (Attachment Upload)
- **Module / Chức năng:** Ticket / Đính kèm tệp tin vào bình luận
- **Mô tả:** Kiểm tra backend PHP xử lý luồng upload tệp đính kèm (hình ảnh PNG/JPG, tài liệu PDF), validate kích thước và định dạng MIME không bị lỗi `Undefined $_FILES` hoặc PHP File Upload Exception.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại khung phản hồi của ticket, nhấn nút đính kèm tệp tin.
  3. Chọn tải lên 1 tệp hình ảnh hợp lệ (`test_evidence.png`, dung lượng < 5MB).
  4. Bắt request upload file (`upload_attachment` hoặc `upload_file`).
  5. Mở tab Response của request upload, kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Tệp tải lên thành công, response trả HTTP 200 kèm link đường dẫn hoặc attachment ID, không có lỗi PHP Warning/Notice.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_26_ticket_attachment.json`

---

### TC_PHP_27: Thay đổi mức độ ưu tiên (Priority)
- **Module / Chức năng:** Ticket / Cập nhật mức độ ưu tiên
- **Mô tả:** Kiểm tra thay đổi mức độ ưu tiên của ticket (Khẩn cấp, Cao, Trung bình, Thấp) backend cập nhật trường priority và tính toán lại hạn SLA không gây lỗi PHP.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại panel thông tin bên phải của chi tiết ticket, bấm vào dropdown "Mức độ ưu tiên".
  3. Chọn giá trị mới (ví dụ từ "Trung bình" thành "Khẩn cấp" hoặc "Cao").
  4. Bấm Lưu hoặc kích hoạt trigger cập nhật tự động.
  5. Bắt request `update_priority` hoặc `update_ticket_field`.
  6. Mở Response kiểm tra lỗi PHP backend.
- **Expected Result:** Mức độ ưu tiên được cập nhật ngay lập tức trên UI, response trả HTTP 200, sạch lỗi PHP backend.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_27_change_priority.json`

---

### TC_PHP_28: Chuyển giao người / nhóm xử lý (Reassign Ticket)
- **Module / Chức năng:** Ticket / Thay đổi nhân viên/nhóm phụ trách
- **Mô tả:** Kiểm tra backend xử lý điều phối ticket sang một Agent hoặc Bộ phận khác không bị lỗi khóa ngoại (Foreign key) hoặc lỗi gửi thông báo nội bộ.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại chi tiết ticket, chọn dropdown "Người xử lý" hoặc "Bộ phận xử lý".
  3. Chọn sang một nhân viên hoặc bộ phận khác trong danh sách.
  4. Bấm Lưu / Cập nhật.
  5. Bắt request API `assign_agent` hoặc `change_assignee`.
  6. Mở Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Ticket chuyển quyền phụ trách thành công, hiển thị người mới trong thông tin phiếu, request trả HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_28_reassign_agent.json`

---

### TC_PHP_29: Lọc theo Hàng đợi phiếu (Queue: Chưa xử lý, Quá hạn, Đã giải quyết)
- **Module / Chức năng:** Ticket / Bộ lọc hàng đợi phiếu
- **Mô tả:** Kiểm tra việc chuyển đổi qua lại giữa các hàng đợi (Unsolved, Breached, Unassign, Solved) trên thanh menu bên trái không phát sinh xung đột tham số truy vấn SQL hoặc lỗi PHP.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại panel hàng đợi bên trái màn hình Ticket, click lần lượt:
     - "Yêu cầu chưa giải quyết trong bộ phận" (`data-id="unsolved-team"`)
     - "Phiếu quá hạn chưa xử lý" (`data-id="breached"`)
     - "Phiếu chưa phân công" (`data-id="unassign"`)
  3. Bắt các request gửi lên (`getDataTableQueue` / `getDataTableFilter`).
  4. Mở Response của từng request kiểm tra lỗi PHP.
- **Expected Result:** Bảng danh sách phiếu lọc chính xác theo hàng đợi đã chọn, số lượng bản ghi khớp với số đếm trên badge, HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_29_filter_queue.json`

---

### TC_PHP_30: Sắp xếp bảng danh sách theo cột (Sorting: ID, Ngày tạo, Ngày cập nhật)
- **Module / Chức năng:** Ticket / Sắp xếp bảng danh sách
- **Mô tả:** Kiểm tra backend DataTables xử lý tham số order (cột sắp xếp và chiều ASC/DESC) an toàn, không bị lỗi cú pháp `ORDER BY` trong câu lệnh SQL.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại bảng danh sách phiếu, click vào tiêu đề cột "ID" để đổi sang sắp xếp tăng dần (ASC).
  3. Click lần nữa để đổi sang sắp xếp giảm dần (DESC).
  4. Click tiếp vào cột "Ngày cập nhật" hoặc "Ngày tạo".
  5. Bắt các request `getDataTable` (chứa các tham số `order[0][column]` và `order[0][dir]`).
  6. Mở Response kiểm tra lỗi PHP.
- **Expected Result:** Dữ liệu bảng được sắp xếp đúng thứ tự cột và chiều yêu cầu, HTTP 200, JSON hợp lệ, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_30_table_sorting.json`

---

### TC_PHP_31: Thao tác hàng loạt (Bulk Action: Đóng nhiều phiếu)
- **Module / Chức năng:** Ticket / Thao tác hàng loạt trên danh sách phiếu
- **Mô tả:** Kiểm tra backend xử lý mảng danh sách ID khi thực hiện thao tác hàng loạt (chọn nhiều checkbox và cập nhật) không phát sinh lỗi tràn bộ nhớ hoặc Undefined index.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại bảng danh sách phiếu, tick chọn checkbox của 2 đến 3 phiếu khác nhau.
  3. Bấm vào menu "Thao tác" / "Thao tác hàng loạt" ở phía trên bảng.
  4. Chọn thao tác "Cập nhật trạng thái" hoặc "Đóng phiếu".
  5. Xác nhận thực hiện và bắt request API xử lý hàng loạt (`bulk_action` / `batch_update`).
  6. Mở tab Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Hệ thống cập nhật thành công các phiếu đã chọn, hiển thị thông báo thành công, HTTP 200, sạch lỗi PHP backend.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_31_bulk_action.json`

---

### TC_PHP_32: Xem nhật ký hoạt động (Audit Log / Activity History)
- **Module / Chức năng:** Ticket / Xem lịch sử hoạt động phiếu
- **Mô tả:** Kiểm tra việc truy xuất và hiển thị danh sách nhật ký thay đổi của phiếu (thời gian, người thực hiện, trường dữ liệu cũ và mới) không bị lỗi định dạng ngày tháng hoặc null pointer PHP.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Mở xem chi tiết một ticket có nhiều lượt tương tác.
  3. Click vào tab "Lịch sử hoạt động" (Activity / Audit log).
  4. Bắt request API tải nhật ký (`ticket/getActivity` hoặc `ticket/get_ticket_log`).
  5. Mở Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Danh sách lịch sử hoạt động hiển thị đầy đủ mốc thời gian, người thao tác và hành vi thay đổi; request trả HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_32_ticket_activity.json`

---

### TC_PHP_33: Xuất danh sách phiếu ra tệp Excel (Export Excel)
- **Module / Chức năng:** Ticket / Xuất dữ liệu danh sách phiếu
- **Mô tả:** Kiểm tra tiến trình xuất dữ liệu danh sách phiếu ra tệp Excel không phát sinh lỗi tràn bộ nhớ (`Memory limit exhausted`), lỗi thư viện PhpSpreadsheet hoặc lỗi mã hóa ký tự.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network, tick "Preserve log".
  2. Tại màn hình danh sách phiếu, nhấn nút "Xuất file" / "Export (.xlsx)".
  3. Bắt request API xuất file (`ticket/export_excel` hoặc `exportTicket`).
  4. Kiểm tra mã trạng thái HTTP, Content-Type (`application/vnd.openxmlformats...` hoặc `application/octet-stream`) và nội dung trả về xem có dính HTML lỗi PHP không.
- **Expected Result:** File Excel được tải về thành công, HTTP 200, file mở được bình thường, không chứa mã lỗi PHP trong file stream.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_33_export_ticket.json`

---

### TC_PHP_34: Tải danh sách khách hàng mặc định
- **Module / Chức năng:** Khách hàng / Tải danh sách khách hàng
- **Mô tả:** Kiểm tra màn hình danh sách khách hàng (`c=customer`) tải giao diện và nạp dữ liệu ban đầu không phát sinh lỗi PHP trong các request khởi tạo.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Truy cập URL: `https://dev-85.midesk.vn/vi?c=customer` (hoặc click menu "Khách hàng" từ thanh điều hướng).
  3. Chờ bảng danh sách khách hàng tải hoàn tất.
  4. Bắt các request khởi tạo DataTables của phân hệ khách hàng (`customer/getDataTable`).
  5. Mở Response kiểm tra các từ khóa lỗi PHP.
- **Expected Result:** Danh sách khách hàng hiển thị đầy đủ, request DataTables trả về mã HTTP 200, JSON hợp lệ, sạch lỗi PHP backend.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_34_customer_list.json`

---

### TC_PHP_35: Tìm kiếm khách hàng theo Số điện thoại / Email
- **Module / Chức năng:** Khách hàng / Tìm kiếm khách hàng
- **Mô tả:** Kiểm tra tính năng tìm kiếm khách hàng bằng số điện thoại hoặc email chính xác và chuỗi ký tự không phát sinh lỗi SQL Injection escaping hoặc lỗi xử lý chuỗi PHP.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại ô tìm kiếm của danh sách khách hàng, nhập số điện thoại (ví dụ: `0917601298`) hoặc địa chỉ email.
  3. Nhấn Enter hoặc nút Tìm kiếm.
  4. Bắt request `customer/getDataTable` với tham số tìm kiếm `search[value]`.
  5. Mở Response kiểm tra dữ liệu trả về và lỗi PHP.
- **Expected Result:** Trả về bản ghi khách hàng tương ứng hoặc danh sách rỗng nếu không tìm thấy, HTTP 200, JSON hợp lệ, không có lỗi PHP Warning/Notice.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_35_customer_search.json`

---

### TC_PHP_36: Mở form thêm mới khách hàng
- **Module / Chức năng:** Khách hàng / Tải form thêm mới khách hàng
- **Mô tả:** Kiểm tra việc nạp popup/form thêm mới khách hàng (bao gồm danh sách nhóm khách hàng, trường tùy biến khách hàng) không phát sinh lỗi PHP backend.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại màn hình danh sách khách hàng, bấm nút "Thêm khách hàng" (hoặc dấu `+`).
  3. Chờ popup modal thêm khách hàng hiển thị.
  4. Bắt các request tải form (`customer/create_customer` hoặc `customer/get_custom_fields`).
  5. Mở tab Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Form thêm mới khách hàng hiển thị đầy đủ các trường nhập liệu (Họ tên, Số điện thoại, Email, Nhóm...), request trả HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_36_customer_create_form.json`

---

### TC_PHP_37: Kiểm tra kiểm soát tính hợp lệ của Số điện thoại
- **Module / Chức năng:** Khách hàng / Kiểm tra tính hợp lệ dữ liệu (Validation)
- **Mô tả:** Kiểm tra backend PHP validate an toàn khi người dùng nhập số điện thoại chứa ký tự chữ cái hoặc chuỗi ký tự đặc biệt, không phát sinh Uncaught Exception.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Mở form thêm mới hoặc chỉnh sửa khách hàng.
  3. Tại trường "Số điện thoại", nhập chuỗi không hợp lệ: `invalid_phone_123!@#`.
  4. Bấm nút "Lưu" / "Xác nhận".
  5. Bắt request submit dữ liệu (`customer/save_customer` hoặc `customer/update_customer`).
  6. Mở Response kiểm tra mã lỗi và thông báo trả về.
- **Expected Result:** Backend xử lý validation an toàn, trả về thông báo lỗi hợp lệ cho người dùng, HTTP 200 hoặc 422, không bị sập script hay sinh PHP Warning.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_37_customer_invalid_phone.json`

---

### TC_PHP_38: Xem tab lịch sử phiếu của khách hàng
- **Module / Chức năng:** Khách hàng / Lịch sử phiếu theo khách hàng
- **Mô tả:** Kiểm tra khi mở xem chi tiết một khách hàng, tab "Danh sách phiếu" của khách hàng đó truy vấn và load danh sách phiếu liên quan không bị lỗi PHP JOIN query.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Mở chi tiết một khách hàng bất kỳ (ví dụ: MKH000290 - Khang Trần).
  3. Click vào tab "Danh sách phiếu" / "Phiếu yêu cầu".
  4. Bắt request API lấy danh sách phiếu của khách hàng (`customer/get_ticket_by_customer` hoặc `load_customer_tickets`).
  5. Mở Response kiểm tra dữ liệu và chuỗi lỗi PHP.
- **Expected Result:** Trả về danh sách các phiếu thuộc về khách hàng đó, HTTP 200, JSON hợp lệ, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_38_customer_ticket_history.json`

---

### TC_PHP_39: Biểu đồ tỷ lệ đạt SLA của Agent
- **Module / Chức năng:** Dashboard / Biểu đồ tỷ lệ SLA nhân viên
- **Mô tả:** Kiểm tra backend tính toán tỷ lệ đạt SLA của từng Agent (`chart_sla_ticket_agent`) không bị lỗi chia cho 0 (`Division by zero`) khi có Agent chưa có phiếu nào xử lý.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Truy cập màn hình Dashboard / Báo cáo Ticket.
  3. Chờ phần biểu đồ "Tỉ lệ đạt SLA theo nhân viên" (`#chart_sla_ticket_agent`) tải xong.
  4. Bắt request API nạp dữ liệu biểu đồ (`dashboard/load_category` hoặc `report/get_sla_agent_chart`).
  5. Mở Response kiểm tra các giá trị tỷ lệ và chuỗi lỗi PHP.
- **Expected Result:** Dữ liệu JSON của biểu đồ trả về chuẩn xác, các tỷ lệ được làm tròn hoặc xử lý 0% an toàn, HTTP 200, không bị lỗi PHP `Division by zero` hay NaN.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_39_dashboard_sla_chart.json`

---

### TC_PHP_40: Lọc dữ liệu Dashboard theo Kênh tiếp nhận
- **Module / Chức năng:** Dashboard / Lọc Dashboard theo kênh
- **Mô tả:** Kiểm tra backend xử lý lọc số liệu thống kê Dashboard khi chọn kênh tiếp nhận (Web, Email, Chat, Voice, Zalo) không phát sinh lỗi SQL syntax hoặc Undefined index.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại dropdown "Channel" trên thanh bộ lọc Dashboard, chọn lần lượt: "Email" -> "Voice" -> "Live chat".
  3. Bấm nút "Filter".
  4. Bắt các request API cập nhật số liệu Dashboard.
  5. Mở Response của từng request kiểm tra lỗi PHP.
- **Expected Result:** Số liệu tổng quan và biểu đồ tự động cập nhật lại theo kênh đã chọn, HTTP 200, JSON hợp lệ, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_40_dashboard_filter_channel.json`

---

### TC_PHP_41: Báo cáo thời gian phản hồi đầu tiên (FRL Report)
- **Module / Chức năng:** Báo cáo / Báo cáo thời gian phản hồi đầu tiên (First Response Time)
- **Mô tả:** Kiểm tra trang báo cáo thời gian phản hồi đầu tiên của Agent (`chart_sla_frl_agent`) tải và tính toán thời lượng trung bình không bị lỗi PHP DateInterval hoặc Arithmetic error.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Tại Dashboard / Báo cáo, cuộn xuống phần biểu đồ FRL (`#chart_sla_frl_agent`).
  3. Chọn khoảng thời gian "Tháng này" hoặc "Tuần này".
  4. Bắt request API tính toán FRL (`report/get_sla_frl_chart` hoặc `dashboard/load_category`).
  5. Mở tab Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Biểu đồ FRL render thành công, các mốc thời gian hiển thị chính xác, HTTP 200, sạch lỗi PHP backend.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_41_report_agent_frl.json`

---

### TC_PHP_42: Tải danh sách Hàng đợi (Queues Management)
- **Module / Chức năng:** Cài đặt / Quản lý hàng đợi phiếu
- **Mô tả:** Kiểm tra trang cấu hình Hàng đợi phiếu (`c=setting&act=queue` hoặc tương đương) nạp danh sách cấu hình điều kiện lọc không phát sinh lỗi PHP.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Truy cập menu Cài đặt -> Hàng đợi phiếu (Queues).
  3. Chờ bảng danh sách các hàng đợi và rule tải xong.
  4. Bắt các request khởi tạo cấu hình (`setting/getQueues` hoặc `ticket/getCountQueues`).
  5. Mở Response kiểm tra chuỗi thông báo lỗi PHP.
- **Expected Result:** Danh sách các hàng đợi và số lượng phiếu trong queue hiển thị chuẩn xác, HTTP 200, sạch lỗi PHP.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_42_setting_queues.json`

---

### TC_PHP_43: Tải danh sách Mẫu trả lời nhanh (Canned Responses / Macros)
- **Module / Chức năng:** Cài đặt / Quản lý mẫu câu trả lời nhanh
- **Mô tả:** Kiểm tra trang quản lý mẫu câu trả lời nhanh (Macros/Canned response) tải danh sách mẫu phản hồi không bị lỗi mã hóa UTF-8 ký tự tiếng Việt hoặc Undefined offset.
- **Các bước thực hiện:**
  1. Mở DevTools (F12) > tab Network > Fetch/XHR.
  2. Truy cập menu Cài đặt -> Mẫu câu trả lời (Canned Responses / Macros).
  3. Chờ bảng danh sách các mẫu phản hồi tải xong.
  4. Bắt request API lấy danh sách mẫu câu (`setting/getCannedResponses` hoặc `ticket/get_macro_list`).
  5. Mở Response kiểm tra chuỗi lỗi PHP.
- **Expected Result:** Danh sách các câu trả lời mẫu tải đầy đủ, hiển thị chính xác văn bản tiếng Việt có dấu, request trả HTTP 200, sạch lỗi PHP backend.
- **Tệp bằng chứng dự kiến:** `evidence/TC_PHP_43_setting_canned_responses.json`

