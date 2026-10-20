# Hợp đồng đầu ra

Tạo một thư mục kết quả có cấu trúc tối thiểu:

```text
ket-qua-loc-cv-<vi-tri>-<yyyymmdd>/
|-- Danh_gia_CV_<vi-tri>.xlsx
|-- index.html
|-- criteria.json          # bộ tiêu chí đã được người dùng duyệt
|-- scores.json            # điểm, trích dẫn, vị trí (đầu vào của script và Agent 2)
|-- tinh_diem.py           # script tính điểm (hoặc .js)
|-- verification.json      # kết quả Agent kiểm tra thứ hai
|-- email-nhap.md          # nháp email (chỉ khi người tuyển dụng yêu cầu)
`-- assets/
    `-- cv/
        `-- <cac-file-cv-goc>
```

Điểm tổng, điểm K, điểm S, độ bao phủ và thứ hạng trong Excel/HTML phải lấy từ kết quả của script, không nhập tay. Điểm **chỉ gồm K và S**; Thái độ không có điểm.

## Excel

Dùng font dễ đọc, freeze header, wrap text và màu trạng thái nhất quán. Câu trích bị Agent 2 gắn *Không tìm thấy* hoặc *Sai ngữ cảnh* tô **đỏ** kèm nhãn chữ. Bắt buộc có:

### Sheet `Tổng quan`

- Số CV đã đọc, nguồn và phạm vi.
- Tiêu chí/trọng số K và S đã duyệt.
- Nhóm HR nên ưu tiên xem xét phỏng vấn, lý do và điểm cần xác minh.
- Kết quả kiểm tra độc lập: số câu Khớp / Không tìm thấy / Sai ngữ cảnh.
- Ghi rõ điểm là điểm bằng chứng K+S, không chấm Thái độ, không phải quyết định tuyển dụng.

### Sheet `Ứng viên`

Các cột tối thiểu:

| Ứng viên | Điểm bằng chứng | Độ bao phủ | Điểm K | Điểm S | Mức phù hợp | Tiêu chí đáp ứng | Tiêu chí thiếu/không tìm thấy | Bằng chứng từ CV | Dấu hiệu Thái độ (không chấm điểm) | Câu hỏi cần xác minh | Kiểm tra độc lập | CV gốc |

### Sheet `Ma trận ASK`

Mỗi hàng là ứng viên × tiêu chí K/S: nhóm, bắt buộc/ưu tiên, trọng số, mức 0–3, trạng thái, **câu trích nguyên văn**, **vị trí (trang, mục)**, nguồn, trạng thái kiểm tra độc lập, câu hỏi xác minh. Điểm tổng dùng công thức hoặc giá trị lấy từ script; không hard-code ước lượng.

### Sheet `Thái độ`

Mỗi hàng là ứng viên: dấu hiệu hành vi trong CV (kèm trích dẫn + vị trí, hoặc “Không tìm thấy dấu hiệu”) và câu hỏi phỏng vấn hành vi STAR. **Không có cột điểm.**

### Sheet `Hướng dẫn ASK`

Giải thích A/S/K, thang 0–3, công thức, trọng số đã duyệt, lý do không chấm Thái độ và các giới hạn của đánh giá từ CV.

Kiểm tra lỗi công thức, ô bị cắt và mọi liên kết nguồn trước khi xuất.

## HTML

Tạo trang responsive, font K2D, ít chữ và ưu tiên quét nhanh. Không phụ thuộc framework nếu không cần.

Bắt buộc có:

- Tổng quan số CV, nguồn, số hồ sơ ưu tiên và tóm tắt kết quả kiểm tra độc lập.
- Khối `<details>` thu gọn tên **“ASK là gì?”**; khi mở phải giải thích A, S, K, thang điểm, lưu ý “điểm bằng chứng” và rằng Thái độ không được chấm điểm.
- Danh sách/card ứng viên chỉ hiển thị **điểm tổng /100** (K+S); không hiện điểm K/S hoặc độ bao phủ trên card. Có thể đặt chip điểm mạnh và mục cần xác minh ngắn gọn.
- Bộ lọc hoặc sắp xếp theo mức phù hợp/điểm khi danh sách dài.
- Bấm tên hoặc card ứng viên mở dialog/drawer chi tiết.
- Chi tiết ứng viên chỉ có hai tab nhìn thấy được: **Tóm tắt** và **CV gốc**.
  - **Tóm tắt:** điểm tổng, điểm K và S (biểu đồ gọn có nhãn/giá trị, ví dụ radar theo từng tiêu chí khi ≥3 tiêu chí, hoặc thanh ngang), điểm mạnh, phần còn thiếu/không tìm thấy, bằng chứng (trích dẫn + vị trí + nhãn kiểm tra độc lập), dấu hiệu Thái độ và câu hỏi phỏng vấn hành vi (không có điểm), câu hỏi cần làm rõ. Câu trích *Không tìm thấy* hoặc *Sai ngữ cảnh* hiển thị **đỏ** kèm nhãn chữ.
  - Dùng khoảng cách thoải mái giữa các khối, chữ nhỉnh hơn cỡ chú thích, ưu tiên ít chữ.
- Cỡ chữ nội dung thường khoảng 16px desktop, 15px màn hình nhỏ. Ảnh CV trong tab **CV gốc** hiển thị lớn, giữ tỷ lệ, không cắt; cho phép cuộn trong hộp thoại.
- Tab **CV gốc**:
  - Ảnh: `<img>`.
  - PDF: `<iframe>`/`<object>` và có nút mở file.
  - DOCX hoặc định dạng không preview được: nút mở/tải file; tạo preview PDF/ảnh nếu công cụ sẵn có.
- Nút mở CV gốc ở tab mới.
- Giữ giao diện gọn, tương phản tốt, màu nhất quán; card phân cấp rõ, huy hiệu thứ tự; có thể dùng card nổi bật cho ứng viên đứng đầu.
- Chỉ hiển thị thông tin nghề nghiệp cần thiết; không đưa dữ liệu nhạy cảm vào thẻ tổng quan.

Dùng đường dẫn tương đối vào `assets/cv/`, encode tên file đúng cách. Kiểm tra mọi candidate key khớp dữ liệu dialog, mọi file CV tồn tại và JavaScript không lỗi cú pháp.

## Nháp email (khi người tuyển dụng yêu cầu)

Soạn nháp email mời phỏng vấn hoặc cảm ơn vào `email-nhap.md`, chỉ cho ứng viên/nhóm do người tuyển dụng chọn. Không nêu điểm số, lý do loại hay thông tin nhạy cảm. Chỉ là nháp để duyệt; không gửi, không tạo draft trong hộp thư khi chưa được xác nhận rõ.

## Bàn giao

Nêu ngắn gọn:

- Số CV đã xử lý và nguồn.
- Bộ tiêu chí và trọng số đã duyệt.
- Nhóm cần HR xem xét phỏng vấn.
- Kết quả kiểm tra độc lập (Khớp / Không tìm thấy / Sai ngữ cảnh).
- Đường dẫn Excel và HTML.
- Các giới hạn hoặc file không đọc được.
