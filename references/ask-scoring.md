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
- **Dấu hiệu ổn định công việc:** tính từ mốc thời gian trong CV (số tháng mỗi vị trí, tính bằng script). Nhãn mặc định: ≥2 vị trí dưới 6 tháng trong 3 năm gần nhất, hoặc có vị trí dưới 3 tháng. Đây chỉ là dữ kiện để đặt câu hỏi (“lý do rời vị trí ngắn hạn?”), không phải kết luận về thái độ; vẫn không chấm điểm. Người dùng có thể đổi ngưỡng khi duyệt tiêu chí.
- Chỉ ghi dấu hiệu thuộc các nhóm hành vi đã duyệt (ví dụ giao tiếp/làm việc nhóm, tư duy phân tích, ổn định công việc). Thành tích chuyên môn không liên quan nhóm đó (ví dụ độ chính xác bảng lương, vệ sinh an toàn thực phẩm) không dùng làm dấu hiệu Thái độ.

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

## Quy tắc nhất quán khi chấm (rút từ các lần kiểm tra độc lập)

- **Mức 3 cần số liệu hoặc lặp ở từ 2 vai trò trở lên.** Nếu tiêu chí yêu cầu “kèm số liệu/kết quả” mà CV chỉ nêu nền tảng và việc làm, không có con số, chấm tối đa mức 2 (trừ khi lặp ở nhiều vai trò và có chứng chỉ/kết quả hỗ trợ; khi đó ghi rõ lý do trong `nhan_xet`).
- **Bằng chứng phải thuộc đúng lĩnh vực của tiêu chí.** Hoạt động bán hàng (gọi điện, gửi email chào hàng, báo cáo doanh số) không phải marketing; viết HTML/CSS không phải viết nội dung; kỹ năng dựng video cơ bản không phải phối hợp content. Nếu chỉ có bằng chứng ngoài lĩnh vực thì chấm 0 (Không tìm thấy) hoặc tối đa 1 và nói rõ là gián tiếp. Áp dụng **cùng một tiêu chuẩn** cho mọi ứng viên.
- **Không dùng lặp một câu để nâng điểm nhiều tiêu chí.** Một câu có thể làm chứng cho nhiều tiêu chí chỉ khi nội dung câu thật sự đáp ứng từng tiêu chí; nếu không, chỉ tính cho tiêu chí khớp nhất và ghi rõ.
- **Vị trí tương đương** (ví dụ Content/Truyền thông so với Digital Marketing): mức tiêu chí số năm kinh nghiệm tối đa 2; ghi lưu ý cần xác nhận mức tương đương.
- **Ngân sách/số liệu tiền:** “quản lý ngân sách” không kèm số tiền chỉ đạt mức 2 cho tiêu chí yêu cầu “có số tiền cụ thể”; ngân sách vận hành khác lĩnh vực (nhà hàng, kế toán) không tính.
- **Tiêu chí về bằng cấp:** chuyên ngành thuộc lĩnh vực khác ghi `Không đáp ứng` (mức 0, kèm trích dẫn chuyên ngành); CV không có mục học vấn ghi `Không tìm thấy` — hai trường hợp khác nhau, đừng gộp.
- **Dấu hiệu Thái độ** phải **thể hiện hành vi** (chủ động đề xuất, chịu trách nhiệm kết quả, phối hợp…); một câu chỉ mô tả đầu việc (“Lên ý tưởng tổ chức sự kiện”) không đủ làm dấu hiệu “chủ động và chịu trách nhiệm kết quả”. Thiếu dấu hiệu thì ghi “Không tìm thấy dấu hiệu”, đó không phải kết luận tiêu cực.
- **Hồ sơ nghi trùng nội dung** (cùng công ty, cùng mô tả giữa các ứng viên khác tên): vẫn chấm riêng từng hồ sơ, đừng gộp; ghi vào `luu_y` để người tuyển dụng xác minh nguồn gốc.

