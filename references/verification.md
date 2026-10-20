# Agent thứ hai — kiểm tra độc lập

Mục tiêu: phát hiện trích dẫn bịa, sai ngữ cảnh, điểm bị thổi phồng hoặc nhận xét không có căn cứ, mà không bị ảnh hưởng bởi lập luận của Agent thứ nhất.

## Điều kiện độc lập

- Chạy trong **phiên mới** (ưu tiên subagent bắt đầu từ đầu, không fork ngữ cảnh). Nếu môi trường không có subagent, hướng dẫn người dùng mở phiên mới và dán prompt bên dưới.
- Nên **chia 2–3 agent chạy song song** (mỗi agent khoảng 3–4 CV) để nhanh; mỗi agent ghi một file `verification_A.json`, `verification_B.json`… Giao thêm cho một agent việc kiểm tra toàn cục.
- Đầu vào duy nhất:
  1. `scores.json` (báo cáo: trích dẫn, vị trí, mức điểm, nhận xét).
  2. `criteria.json` (tiêu chí, trọng số đã duyệt).
  3. CV gốc trong `assets/cv/` (ảnh: tự mở và đọc bằng thị giác; PDF/DOCX: tự đọc).
- **Không** đưa: lập luận, ghi chú, đoạn suy nghĩ, văn bản trích xuất trung gian (`.work/`) của Agent thứ nhất, `ket_qua_tinh_diem.json`, script. Dặn agent **chỉ đọc đúng các file trên**.

## Việc Agent 2 phải làm

Với **mỗi** câu trích (điểm K/S và dấu hiệu Thái độ):

1. Mở đúng CV gốc, tìm vị trí được ghi (trang, mục).
2. Gán trạng thái:
   - **Khớp:** câu trích có trong CV đúng nguyên văn (cho phép sai khác OCR/xuống dòng không đổi nghĩa) và ngữ cảnh ủng hộ mức điểm.
   - **Không tìm thấy:** không có câu này ở vị trí ghi hoặc ở bất kỳ đâu trong CV.
   - **Sai ngữ cảnh:** câu có thật nhưng không ủng hộ tiêu chí/mức điểm (thuộc vai trò khác, nói điều ngược lại, là yêu cầu chứ không phải thành tích, chỉ là mô tả đầu việc với dấu hiệu Thái độ, hoặc dấu hiệu không thuộc nhóm hành vi đã duyệt).
3. Với mỗi ô mức 0 ghi “Không tìm thấy” (khẳng định CV không nêu): kiểm tra CV có thật sự không nêu. Ghi bản ghi `loai: "Khang_dinh_khong_co"`, `Khớp` nếu đúng, `Sai ngữ cảnh` nếu CV có bằng chứng (nêu câu đó trong `ghi_chu`).
4. Kiểm tra thêm, ghi vào `kiem_tra_khac` (không tự sửa điểm):
   - Trọng số khớp `criteria.json`, tổng = 100; mức > 0 đều có trích dẫn và vị trí.
   - Mức điểm bị **thổi phồng** (mức 3 khi không có số liệu; chiến lược nội dung tính là chiến lược marketing; hoạt động bán hàng tính là marketing; một câu bị dùng lặp để nâng điểm nhiều tiêu chí).
   - Mức điểm **quá thấp** so với bằng chứng thực có (bỏ sót).
   - Nhận xét/điểm mạnh/lưu ý/câu hỏi khẳng định điều không có bằng chứng.
   - Thái độ không bị chấm điểm hay dùng trong xếp hạng; mỗi dấu hiệu Thái độ thuộc đúng nhóm hành vi đã duyệt (kể cả “ổn định công việc”).
   - Báo cáo không chứa tiêu chí hoặc suy luận từ thông tin nhạy cảm.
   - Nếu không có vấn đề, ghi một bản ghi nói rõ “không phát hiện vấn đề”.
5. Trả kết quả JSON:

```json
{"pham_vi": ["cv01","cv02"],
 "kiem_tra": [{"key": "cv01", "ung_vien": "...", "tieu_chi": "K1", "loai": "K/S|Thai_do|Khang_dinh_khong_co",
               "nhom_hanh_vi": "(chỉ với Thai_do)", "trich_dan": "...", "vi_tri": "ảnh 1/1, Học vấn",
               "trang_thai": "Khớp|Không tìm thấy|Sai ngữ cảnh", "ghi_chu": "ngắn gọn"}],
 "kiem_tra_khac": [{"key": "cv01|toan_cuc", "ung_vien": "...", "van_de": "...", "ghi_chu": "..."}]}
```

## Prompt mẫu cho Agent 2

```text
Bạn là người kiểm tra độc lập. Bạn chỉ được dùng đúng 3 nguồn: scores.json, criteria.json và CV gốc trong assets/cv/ (đường dẫn tuyệt đối: <...>). Không đọc file nào khác trong thư mục.
Phạm vi của bạn: các ứng viên có key <cv01, cv02, ...>. Với từng câu trích dẫn trong scores.json (tiêu chí K/S và dấu hiệu Thái độ), mở CV gốc, đối chiếu tại đúng vị trí đã ghi và gán một trong ba trạng thái: Khớp / Không tìm thấy / Sai ngữ cảnh. Với mỗi ô mức 0 "Không tìm thấy", xác nhận CV thật sự không nêu (loai = Khang_dinh_khong_co). Kiểm tra thêm: điểm bị thổi phồng hoặc bỏ sót, nhận xét không có bằng chứng, Thái độ không bị chấm điểm, dấu hiệu Thái độ thuộc nhóm hành vi đã duyệt, trọng số. Không suy đoán, không sửa điểm. Ghi kết quả vào verification_<X>.json theo lược đồ đã cho (UTF-8, JSON hợp lệ), mỗi câu trích một bản ghi. Trả lời ngắn: số bản ghi theo trạng thái và các vấn đề đáng chú ý.
```

## Ghép kết quả vào báo cáo

`scripts/tao_bao_cao.py` tự ghép mọi `verification_*.json`:

- Mỗi câu trích hiển thị nhãn trạng thái kiểm tra.
- Câu **Không tìm thấy** hoặc **Sai ngữ cảnh** được **đánh dấu đỏ** (nền/viền đỏ + nhãn chữ) trong HTML và Excel; tiêu chí liên quan gắn cờ “Cần rà soát”.
- Số lượng Khớp / Không tìm thấy / Sai ngữ cảnh hiện ở phần tổng quan.
- **Không tự sửa điểm.** Gom các điểm Agent 2 đề nghị xem lại (`kiem_tra_khac`) và hỏi người dùng giữ hay chấm lại; chỉ khi người dùng đồng ý mới sửa `scores.json`, chạy lại `tinh_diem.py` và `tao_bao_cao.py` (và chạy lại kiểm tra cho các câu trích đã đổi).
