# Hợp đồng đầu ra

Báo cáo **bắt buộc** có đúng bố cục "CV Radar" dưới đây (không có phần A/Thái độ trong điểm). Không tự dựng giao diện khác: dùng `scripts/tao_bao_cao.py` với `assets/mau_bao_cao.html` và `assets/giao_dien.js`; nếu cần chỉnh, sửa mẫu rồi chạy lại script.

Thư mục kết quả:

```text
ket-qua-loc-cv-<vi-tri>-<yyyymmdd>/
|-- index.html                      # báo cáo TỰ CHỨA (ảnh CV nhúng data URI)
|-- Danh_gia_CV_<vi_tri>.xlsx       # 5 sheet
|-- criteria.json                   # tiêu chí đã duyệt
|-- scores.json                     # điểm, trích dẫn, vị trí (đầu vào của script và Agent 2)
|-- tinh_diem.py                    # bản sao script tính điểm
|-- ket_qua_tinh_diem.json          # điểm do script tính
|-- verification_A.json ...         # kết quả từng Agent 2
|-- verification.json               # gộp kết quả Agent 2
|-- verification_nhan_xet.json      # nhận xét thêm của Agent 2 (điểm thổi phồng/bỏ sót)
|-- tong_hop.json
|-- anh_xa_cv.json                  # tên gốc -> tên lưu
|-- email-nhap.md                   # chỉ khi người tuyển dụng yêu cầu
`-- assets/
    |-- cv/        # CV gốc (bản sao)
    `-- preview/   # ảnh xem trước
```

Điểm tổng, điểm K, điểm S, độ bao phủ và thứ hạng trong Excel/HTML phải lấy từ `ket_qua_tinh_diem.json` (do script tính), không nhập tay. Điểm **chỉ gồm K và S**; Thái độ không có điểm.

## Vì sao `index.html` phải tự chứa

Trình duyệt tích hợp của **Claude Code** và **Codex** mở file cục bộ như một trang `data:` (ảnh chụp), nên:

- ảnh tham chiếu `assets/cv/...` (đường dẫn tương đối) **không hiện**;
- `localhost` có thể bị chặn hoặc không sẵn sàng;
- mở data URI trực tiếp ở tab mới bị trình duyệt chặn.

Do đó: nhúng mọi ảnh CV vào `index.html` dạng `data:image/jpeg;base64,...` (nén, rộng tối đa 1100 px, chất lượng ~80, tổng file thường 3–6 MB), và nút "Mở ảnh CV ở tab mới" dùng **blob URL** tạo từ data URI. Không tạo thêm bản HTML thứ hai không cần thiết. Font K2D tải từ Google Fonts, nếu offline sẽ tự dùng font hệ thống.

## HTML — bố cục bắt buộc (thứ tự từ trên xuống)

Phong cách "CV Radar": nền gradient xanh nhạt, header bo tròn có logo, khối hero gradient xanh đậm với vòng tròn số (ví dụ `3/11` ưu tiên xem kỹ), ô số liệu có viền trên màu xanh, thẻ ưu tiên bo góc lớn (thẻ đầu nền tối, số điểm vàng), bảng có header xanh đậm, hộp chi tiết có tab dạng viên thuốc. Font K2D, chữ nội dung ≥ 15–16 px. Ít chữ, ưu tiên quét nhanh.

1. **Header** (`CV Radar` + vị trí · số hồ sơ · ngày) và **hero** (tiêu đề "Hồ sơ cần xem kỹ.", đoạn dẫn, vòng tròn `3/N`).
2. **4 ô thống kê:** số CV đã đọc; số hồ sơ từ 70 điểm và đủ tiêu chí bắt buộc; trọng số K / S (ghi rõ A không chấm điểm); số câu trích Agent 2 xác nhận khớp và số mục cần rà soát.
3. Khối **`<details>` "ASK là gì?"**: 3 cột A (không chấm điểm) · S · K + dòng giải thích thang 0–3, công thức, "điểm bằng chứng", giả định trọng số/X.
4. **Ứng viên ưu tiên:** đúng 3 thẻ có điểm cao nhất (thẻ đầu nền tối). Mỗi thẻ: nhãn "Ưu tiên n", tên, chức danh, điểm `/100`, 3–4 chip điểm mạnh ngắn, dòng "Cần xác minh". Điểm dưới 70 thêm "Cần làm rõ trước". Chỉ hiện điểm tổng, không hiện K/S hay độ bao phủ ngoài thẻ.
5. **Tất cả hồ sơ:** bộ lọc (Tất cả / Ưu tiên / Còn lại), nút sắp xếp theo điểm, bảng gồm Ứng viên · Điểm · S · K · Độ bao phủ · Mức bằng chứng (kèm "Thiếu bắt buộc: …") · Kiểm tra độc lập. Hàng có mục cần rà soát nền đỏ nhạt + nhãn chữ.
6. **Hộp chi tiết** (click thẻ hoặc hàng), hai tab:
   - **Tóm tắt:** 3 ô điểm (Tổng, S, K) + độ bao phủ; **radar theo từng tiêu chí K/S** (≥3 tiêu chí); tóm tắt, "điểm cần kiểm tra"; danh sách tiêu chí **Phù hợp** và **Chưa đủ bằng chứng**, mỗi tiêu chí có mức `n/3`, nhãn "Bắt buộc", nhận xét, các câu trích nguyên văn kèm vị trí và nhãn kiểm tra độc lập; khối **Thái độ** (dấu hiệu + ổn định công việc + câu hỏi STAR, không có điểm); câu hỏi cần làm rõ.
   - **CV gốc:** ảnh lớn, giữ tỷ lệ, không cắt, cuộn trong hộp thoại; nút "Mở ảnh CV ở tab mới" (blob URL).
7. **Footer:** nguồn CV và câu "Đánh giá hỗ trợ rà soát, không quyết định tuyển dụng".

Câu trích bị Agent 2 gắn *Không tìm thấy* hoặc *Sai ngữ cảnh* hiển thị **đỏ kèm nhãn chữ** (không chỉ dựa vào màu); tiêu chí liên quan gắn "Cần rà soát". Chỉ hiển thị thông tin nghề nghiệp cần thiết; không đưa dữ liệu nhạy cảm vào thẻ tổng quan.

## Checklist kiểm tra HTML (bắt buộc, trên trình duyệt thật)

1. Khởi động máy chủ tĩnh chỉ để kiểm tra (ví dụ `python -m http.server <cổng>` trong thư mục kết quả) rồi mở `index.html` trong trình duyệt tích hợp. Không giao máy chủ này cho người dùng; bản giao là file tự chứa.
2. Console **không có lỗi** (lỗi hay gặp: đặt tên biến trùng biến toàn cục như `top`, `name`, `status`; `node --check` không phát hiện được).
3. Đủ 3 thẻ ưu tiên, số dòng bảng = số CV, vòng tròn và ô thống kê hiện đúng số (mảng rỗng trong JavaScript là `truthy`: dùng `.length`).
4. Mở một ứng viên: tab Tóm tắt có radar và đủ tiêu chí; tab **CV gốc** có ảnh với `naturalWidth > 0`.
5. Bộ lọc và sắp xếp hoạt động; ứng viên có mục đỏ hiển thị nhãn chữ.
6. Nếu mở thẳng `file://` trong trình duyệt tích hợp, ảnh vẫn hiện (vì đã nhúng).

## Excel

Font Arial, header xanh navy chữ trắng, freeze header, wrap text; trạng thái: **xanh** (Đáp ứng), **xanh dương** (Đáp ứng một phần), **đỏ nhạt** (Chưa đủ bằng chứng / Không đáp ứng), **vàng** (tiêu chí bắt buộc còn thiếu). Ô có câu trích bị Agent 2 gắn *Không tìm thấy*/*Sai ngữ cảnh* tô **đỏ** kèm nhãn chữ. Năm sheet:

1. **Tổng quan:** số CV, nguồn, phạm vi, tiêu chí ASK, lưu ý; bảng "Nhóm HR xem kỹ · Ứng viên · Lý do · Kiểm tra trước quyết định"; thang điểm 0–3; số liệu kiểm tra độc lập; các điểm Agent 2 đề nghị xem lại.
2. **Ứng viên:** Hạng · Ứng viên · Điểm bằng chứng · Độ bao phủ · Điểm S · Điểm K · Mức bằng chứng · Tiêu chí bắt buộc còn thiếu · Kiểm tra độc lập · CV gốc (liên kết).
3. **Ma trận đối chiếu:** mỗi hàng = ứng viên × tiêu chí: ID · ASK · Tiêu chí · Mức độ · Trọng số · Điểm 0–3 · Điểm quy đổi · Trạng thái · Bằng chứng nguyên văn · Nguồn CV (trang, mục) · Kiểm tra độc lập · Câu hỏi cần xác minh.
4. **Thái độ:** dấu hiệu hành vi (kèm trích dẫn, vị trí, kiểm tra độc lập), dấu hiệu ổn định công việc, câu hỏi STAR. **Không có cột điểm.**
5. **Hướng dẫn ASK:** A/S/K, thang 0–3, công thức, lý do không chấm Thái độ, giới hạn của đánh giá từ CV.

Kiểm tra lỗi công thức, ô bị cắt và mọi liên kết trước khi xuất.

## Nháp email (khi người tuyển dụng yêu cầu)

Soạn nháp email mời phỏng vấn hoặc cảm ơn vào `email-nhap.md`, chỉ cho ứng viên/nhóm do người tuyển dụng chọn. Không nêu điểm số, lý do loại hay thông tin nhạy cảm. Chỉ là nháp để duyệt; không gửi, không tạo draft trong hộp thư khi chưa được xác nhận rõ.
