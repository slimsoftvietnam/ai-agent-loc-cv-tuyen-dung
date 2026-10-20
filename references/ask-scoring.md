# Khung ASK và chấm điểm bằng chứng

Chỉ **K (Knowledge)** và **S (Skills)** được chấm điểm. **A (Attitude)** không được chấm.

## Đề xuất tiêu chí từ JD

Agent đọc JD và đề xuất bộ tiêu chí để người dùng duyệt. Mỗi tiêu chí K/S có:

- `id` (ví dụ K1, S1)
- `nhóm`: K hoặc S
- `mô tả quan sát được`
- `mức độ`: bắt buộc hoặc ưu tiên
- `trọng số` (tổng tất cả tiêu chí K+S = 100)
- `bằng chứng chấp nhận được`

Không dùng nhãn mơ hồ. Ví dụ: “có kinh nghiệm chạy Google Ads có số liệu chi tiêu/kết quả” cụ thể hơn “giỏi quảng cáo”.

Nếu người dùng chỉ cung cấp trọng số theo nhóm K/S, chia đều trong từng nhóm; tiêu chí bắt buộc không tự có trọng số cao hơn nếu chưa được yêu cầu. Gợi ý mặc định khi JD không nói gì: S 60 / K 40, nêu rõ là giả định.

## Thái độ (Attitude) — không chấm điểm

Trong `criteria.json`, Thái độ chỉ là danh sách **hành vi cần xác minh**, không có `trọng số` và không có mức 0–3. Với mỗi ứng viên:

- **Dấu hiệu từ CV:** các hành vi/kết quả cụ thể có trong CV (chủ động đề xuất, chịu trách nhiệm end-to-end, phối hợp liên phòng ban…), mỗi dấu hiệu kèm trích dẫn nguyên văn và vị trí. Nếu không có, ghi “Không tìm thấy dấu hiệu”; điều này không phải kết luận tiêu cực.
- **Câu hỏi phỏng vấn hành vi (STAR):** 2–4 câu để người tuyển dụng xác minh.
- Không suy từ ảnh, sở thích, tính từ tự mô tả hoặc phong cách thiết kế CV.
- Không đưa Thái độ vào điểm tổng, thứ hạng, màu mức phù hợp hay nhãn ưu tiên.

## Mức bằng chứng (K và S)

Chấm từng tiêu chí theo thang 0–3:

- **3 — Mạnh:** bằng chứng trực tiếp, có phạm vi/kết quả/số liệu hoặc lặp lại ở nhiều vai trò.
- **2 — Đủ:** bằng chứng trực tiếp nhưng ít chi tiết.
- **1 — Một phần:** bằng chứng gián tiếp, gần tương đương hoặc chưa rõ vai trò cá nhân.
- **0 — Không tìm thấy / không đạt:** CV không nêu (ghi “Không tìm thấy”) hoặc nêu rõ không đạt yêu cầu tối thiểu.

### Quy tắc bằng chứng bắt buộc

Mỗi mức > 0 phải có:

- **Câu trích nguyên văn** từ CV (đúng từng chữ, không diễn giải).
- **Vị trí**: số trang và tên mục (ví dụ “tr.2, Kinh nghiệm làm việc”). Với DOCX/ảnh không có trang thật, ghi mục và thứ tự trang/ảnh.

Không có trích dẫn kèm vị trí thì không được chấm quá 0. Mức 0 phải ghi “Không tìm thấy”.

Giữ cột trạng thái riêng: `Đáp ứng` (mức 2–3), `Đáp ứng một phần` (mức 1), `Không tìm thấy` (CV không nêu), `Không đáp ứng` (CV nêu rõ trái yêu cầu tối thiểu). Điểm 0 không được diễn giải thành kết luận người đó không có năng lực.

## Công thức (tính bằng mã chương trình)

Tính bằng script chạy thật, không tính nhẩm.

```text
Điểm bằng chứng phù hợp = Σ(trọng số tiêu chí × mức bằng chứng / 3)   (chỉ K và S)
Điểm K = Σ trong nhóm K, quy về thang 100 của nhóm K
Điểm S = Σ trong nhóm S, quy về thang 100 của nhóm S
Độ bao phủ = số tiêu chí K/S có mức > 0 / tổng số tiêu chí K/S
```

Hiển thị điểm thang 100, làm tròn một chữ số. Script phải: kiểm tra tổng trọng số = 100, báo lỗi nếu thiếu trích dẫn khi mức > 0, và xuất kết quả ra file để Excel/HTML dùng lại.

## Diễn giải mặc định

Chỉ dùng khi người dùng không cung cấp ngưỡng:

- 85–100: Bằng chứng phù hợp rất mạnh.
- 70–84,9: Bằng chứng phù hợp tốt.
- 50–69,9: Bằng chứng phù hợp một phần.
- Dưới 50: Bằng chứng còn hạn chế.

Đây là nhãn hỗ trợ ưu tiên rà soát, không phải quyết định tuyển/loại. Một tiêu chí bắt buộc có trạng thái `Không đáp ứng` hoặc `Không tìm thấy` phải hiển thị nổi bật dù tổng điểm cao.
