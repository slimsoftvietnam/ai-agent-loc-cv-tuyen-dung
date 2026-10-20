# Agent thứ hai — kiểm tra độc lập

Mục tiêu: phát hiện trích dẫn bịa, sai ngữ cảnh hoặc nhận xét không có căn cứ, mà không bị ảnh hưởng bởi lập luận của Agent thứ nhất.

## Điều kiện độc lập

- Chạy trong **phiên mới** (ưu tiên subagent bắt đầu từ đầu, không fork ngữ cảnh). Nếu môi trường không có subagent, hướng dẫn người dùng mở phiên mới và dán prompt bên dưới.
- Đầu vào duy nhất:
  1. Báo cáo: `scores.json` (hoặc Excel) với các trích dẫn, vị trí, mức điểm, nhận xét.
  2. `criteria.json` (tiêu chí, trọng số đã duyệt).
  3. CV gốc trong `assets/cv/`.
- **Không** đưa: lập luận, ghi chú, đoạn suy nghĩ, văn bản trích xuất trung gian của Agent thứ nhất. Agent 2 tự đọc/OCR CV gốc.

## Việc Agent 2 phải làm

Với **mỗi** câu trích (điểm K/S và dấu hiệu Thái độ):

1. Mở đúng CV gốc, tìm vị trí được ghi (trang, mục).
2. Gán trạng thái:
   - **Khớp:** câu trích có trong CV đúng nguyên văn (cho phép sai khác OCR/định dạng không đổi nghĩa) và ngữ cảnh ủng hộ mức điểm.
   - **Không tìm thấy:** không có câu này ở vị trí ghi hoặc ở bất kỳ đâu trong CV.
   - **Sai ngữ cảnh:** câu có thật nhưng không ủng hộ tiêu chí/mức điểm (ví dụ thuộc vai trò khác, nói điều ngược lại, là yêu cầu chứ không phải thành tích, hoặc không phải của ứng viên).
3. Kiểm tra thêm:
   - Trọng số trong báo cáo khớp `criteria.json`; tổng = 100; điểm tiêu chí có trích dẫn.
   - Nhận xét điểm mạnh/thiếu **không có bằng chứng** (khẳng định không kèm trích dẫn) → ghi là “Không có bằng chứng”.
   - Thái độ không bị chấm điểm hay dùng trong xếp hạng.
   - Mỗi dấu hiệu Thái độ thuộc đúng nhóm hành vi đã duyệt trong `criteria.json` (kể cả nhóm “ổn định công việc”); nếu không thì gán *Sai ngữ cảnh*.
   - Mức điểm có bị thổi phồng so với trích dẫn (ví dụ mức 3 khi không có số liệu, hoặc chiến lược nội dung bị tính là chiến lược marketing): ghi nhận xét, không tự sửa điểm.
   - Báo cáo không chứa tiêu chí hoặc suy luận từ thông tin nhạy cảm.
4. Trả kết quả dạng JSON `verification.json`:

```json
[{"ung_vien": "...", "tieu_chi": "S1", "trich_dan": "...", "vi_tri": "tr.2, Kinh nghiệm",
  "trang_thai": "Khớp|Không tìm thấy|Sai ngữ cảnh", "ghi_chu": "ngắn gọn"}]
```

## Prompt mẫu cho Agent 2

```text
Bạn là người kiểm tra độc lập. Bạn chỉ có: scores.json, criteria.json và CV gốc trong assets/cv/.
Với từng câu trích dẫn trong scores.json, đối chiếu với CV gốc tại đúng vị trí đã ghi và gán một trong ba trạng thái:
Khớp / Không tìm thấy / Sai ngữ cảnh. Kiểm tra thêm trọng số, tổng trọng số, nhận xét không có bằng chứng, và việc Thái độ không bị chấm điểm.
Không suy đoán, không sửa điểm. Ghi kết quả vào verification.json theo lược đồ đã cho.
```

## Ghép kết quả vào báo cáo

- Mỗi câu trích hiển thị nhãn trạng thái kiểm tra.
- Câu **Không tìm thấy** hoặc **Sai ngữ cảnh** được **đánh dấu đỏ** (nền/viền đỏ + nhãn chữ, không chỉ dựa vào màu) trong HTML và Excel; tiêu chí liên quan gắn cờ “cần rà soát”.
- Tổng hợp số lượng Khớp / Không tìm thấy / Sai ngữ cảnh ở phần tổng quan.
- Không tự sửa điểm; nếu có lỗi, trình bày cho người dùng quyết định chấm lại hay giữ nguyên.
