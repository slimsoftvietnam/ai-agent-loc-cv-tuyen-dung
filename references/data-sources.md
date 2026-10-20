# Nguồn CV

Chỉ đọc nguồn sau khi người dùng đã chọn và xác nhận phạm vi.

## Gmail

Thu thập các thông tin sau trước khi tìm kiếm:

- Tài khoản hoặc hộp thư cần dùng, nếu có nhiều kết nối.
- Khoảng thời gian. Gợi ý mặc định: 90 ngày gần nhất.
- Từ khóa tiêu đề/nội dung, nhãn, người gửi hoặc tên vị trí.
- Chỉ lấy email có file đính kèm hay cả link Drive.
- Định dạng file chấp nhận: PDF, DOCX, JPG, PNG, WEBP; hỏi thêm nếu có định dạng khác.
- Có giới hạn số email/CV không.

Dùng công cụ Gmail được kết nối để tìm và đọc đúng phạm vi. Khâu thu thập CV là thao tác chỉ đọc: không gửi thư, tạo bản nháp, chuyển tiếp, lưu trữ, xóa hoặc gắn nhãn. Nếu người dùng muốn gửi báo cáo sau khi hoàn tất, xử lý riêng theo mục **Gửi báo cáo cho nhà tuyển dụng** trong `SKILL.md`; cần duyệt người nhận, nội dung và tệp đính kèm trước khi gửi.

Nếu Gmail chưa kết nối hoặc không thể tải file đính kèm, báo rõ và đề nghị người dùng chọn phương án thư mục. Không tự chuyển sang đọc toàn bộ hộp thư.

Lưu bản sao file CV đã đọc vào thư mục kết quả `assets/cv/` với tên an toàn, giữ phần mở rộng và lập bảng ánh xạ tên gốc → tên lưu. Không ghi nội dung email không liên quan vào báo cáo.

## Thư mục

Hỏi:

- Đường dẫn tuyệt đối của thư mục.
- Có đọc thư mục con không.
- Định dạng cần bao gồm hoặc loại trừ.

Trước khi đọc, liệt kê số file theo định dạng và xác nhận nếu phạm vi khác đáng kể so với mô tả của người dùng. Bỏ qua file tạm, file đầu ra cũ và file không phải CV.

Không sửa hoặc đổi tên file nguồn. Sao chép CV cần dùng vào `assets/cv/` của báo cáo HTML để liên kết hoạt động ổn định; giữ bảng ánh xạ về nguồn ban đầu trong Excel.

## Trích xuất

Dùng `scripts/chuan_bi_cv.py` để chuẩn bị (xem SKILL.md, Bước 3). Nó sao chép CV gốc vào `assets/cv/`, tạo ảnh xem trước `assets/preview/` và trích văn bản vào `.work/van-ban/`.

- **Ảnh (JPG/PNG/WEBP):** bắt buộc đọc bằng thị giác (mở ảnh bằng công cụ đọc ảnh). Ảnh rất lớn: đọc bản `assets/preview/` nếu đủ rõ; nếu chữ nhỏ thì đọc bản gốc. Ghi vị trí dạng `ảnh k/n, tên mục`.
- **PDF có text:** dùng văn bản trích (có số trang); PDF scan (script báo “không có text”): đọc ảnh xem trước từng trang bằng thị giác, đánh dấu đoạn không chắc.
- **DOCX:** dùng văn bản trích (mục, bảng); nếu máy có LibreOffice, script tạo ảnh xem trước để báo cáo hiển thị CV gốc; nếu không, báo cáo chỉ có chỗ mở file.
- Nhiều file cùng ứng viên: gộp chỉ khi có bằng chứng rõ là cùng người; nếu không, giữ tách biệt.
- File trùng nội dung: giữ một bản phân tích, ghi các tên nguồn trùng.
- Windows: luôn chạy Python với `-X utf8`; tên file tiếng Việt được chuẩn hóa thành tên an toàn, bảng ánh xạ ở `anh_xa_cv.json`.
- Văn bản trích trong `.work/` chỉ dành cho Agent thứ nhất; **không đưa cho Agent kiểm tra**.
