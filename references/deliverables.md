# Hợp đồng đầu ra

Tạo một thư mục kết quả có cấu trúc tối thiểu:

```text
ket-qua-loc-cv-<vi-tri>-<yyyymmdd>/
|-- Danh_gia_CV_<vi-tri>.xlsx
|-- index.html
`-- assets/
    `-- cv/
        `-- <cac-file-cv-goc>
```

## Excel

Dùng font dễ đọc, freeze header, wrap text và màu trạng thái nhất quán. Bắt buộc có:

### Sheet `Tổng quan`

- Số CV đã đọc, nguồn và phạm vi.
- Tiêu chí/trọng số ASK.
- Nhóm HR nên ưu tiên xem kỹ hơn, lý do và điểm cần xác minh.
- Ghi rõ điểm là điểm bằng chứng, không phải quyết định tuyển dụng.

### Sheet `Ứng viên`

Các cột tối thiểu:

| Ứng viên | Điểm bằng chứng | Độ bao phủ | Điểm A | Điểm S | Điểm K | Mức phù hợp | Tiêu chí đáp ứng | Tiêu chí chưa đáp ứng/chưa đủ bằng chứng | Bằng chứng từ CV | Câu hỏi cần xác minh | CV gốc |

### Sheet `Ma trận ASK`

Mỗi hàng là ứng viên × tiêu chí. Có nhóm ASK, bắt buộc/ưu tiên, trọng số, mức 0–3, trạng thái, bằng chứng, nguồn và câu hỏi xác minh. Điểm tổng phải dùng công thức có thể kiểm tra lại; không hard-code kết quả nếu có thể dùng công thức rõ ràng.

### Sheet `Hướng dẫn ASK`

Giải thích A/S/K, thang 0–3, công thức, giả định trọng số và các giới hạn của đánh giá từ CV.

Kiểm tra lỗi công thức, ô bị cắt và mọi liên kết nguồn trước khi xuất.

## HTML

Tạo trang responsive, font K2D, ít chữ và ưu tiên quét nhanh. Không phụ thuộc framework nếu không cần.

Bắt buộc có:

- Tổng quan số CV, nguồn và số hồ sơ ưu tiên.
- Khối `<details>` thu gọn tên **“ASK là gì?”**; khi mở phải giải thích A, S, K, thang điểm và lưu ý “điểm bằng chứng”.
- Danh sách/card ứng viên ưu tiên chỉ hiển thị điểm tổng `/100`; không hiện điểm A/S/K hoặc tỷ lệ bao phủ trên card. Có thể đặt chip điểm mạnh và mục cần xác minh ngắn gọn để HR quét nhanh.
- Bộ lọc hoặc sắp xếp theo mức phù hợp/điểm khi danh sách dài.
- Bấm tên hoặc card ứng viên mở dialog/drawer chi tiết.
- Khi mở chi tiết ứng viên, chỉ có hai phần/tab nhìn thấy được: **Tóm tắt** và **CV gốc**. Phần **Tóm tắt** phải có điểm tổng cùng điểm A/S/K, tiêu chí phù hợp, tiêu chí chưa phù hợp/chưa đủ bằng chứng, bằng chứng và câu hỏi cần hỏi thêm. Ưu tiên biểu đồ mạng nhện cho điểm A/S/K, có nhãn/giá trị rõ; tạo khoảng cách rõ giữa các khối và cỡ chữ đọc thoải mái, hạn chế chú thích dài.
- Cỡ chữ nội dung thường trên trang tổng quan nên khoảng 16px trên desktop và 15px trên màn hình nhỏ; các nhãn phụ không nên nhỏ tới mức khó đọc. Ảnh CV trong tab **CV gốc** cần hiển thị lớn, giữ đúng tỷ lệ và không bị cắt; cho phép cuộn trong hộp thoại khi ảnh vượt chiều cao màn hình.
- Tab **CV gốc**:
  - Ảnh: hiển thị bằng `<img>`.
  - PDF: hiển thị bằng `<iframe>`/`<object>` và có nút mở file.
  - DOCX hoặc định dạng không preview được: cung cấp nút mở/tải file; tạo preview PDF/ảnh nếu công cụ sẵn có.
- Nút mở CV gốc ở tab mới.
- Chỉ hiển thị thông tin nghề nghiệp cần thiết; không đưa dữ liệu nhạy cảm vào thẻ tổng quan.

Dùng đường dẫn tương đối vào `assets/cv/` để báo cáo có thể di chuyển cùng thư mục. Escaped/encode tên file đúng cách. Kiểm tra mọi candidate key khớp dữ liệu dialog, mọi file CV tồn tại và JavaScript không lỗi cú pháp.

## Bàn giao

Nêu ngắn gọn:

- Số CV đã xử lý và nguồn.
- Giả định trọng số ASK.
- Nhóm cần HR xem kỹ hơn.
- Đường dẫn Excel và HTML.
- Các giới hạn hoặc file không đọc được.

