---
name: agent-loc-cv
description: Sàng lọc CV theo khung ASK (Attitude, Skills, Knowledge) từ Gmail hoặc thư mục người dùng cung cấp. Agent tự đề xuất bộ tiêu chí từ mô tả công việc để người dùng duyệt; chấm Kiến thức và Kỹ năng có trích dẫn nguyên văn, KHÔNG chấm Thái độ (chỉ ghi dấu hiệu và câu hỏi hành vi); tính điểm bằng mã; một agent thứ hai kiểm tra độc lập các trích dẫn; xuất Excel + HTML và nháp email cho người tuyển dụng quyết định. Dùng khi người dùng muốn đọc, đối chiếu, chấm điểm hoặc lập shortlist CV.
---

# Lọc CV theo ASK

Tạo một quy trình sàng lọc có thể kiểm tra lại bằng bằng chứng. Điểm số chỉ phản ánh mức độ bằng chứng trong CV về **Kiến thức và Kỹ năng**; không phải phán quyết năng lực hoặc quyết định tuyển/loại. **Thái độ (Attitude) không được chấm điểm.**

## Tổng quan quy trình

1. Cổng đầu vào: chọn nguồn CV + nhận mô tả công việc (JD).
2. Agent đọc JD, **tự đề xuất** bộ tiêu chí ASK + trọng số → người dùng điều chỉnh và **phê duyệt**.
3. Chỉ sau khi được duyệt mới đọc và trích xuất CV.
4. Chấm K và S có trích dẫn nguyên văn + vị trí; Thái độ chỉ ghi dấu hiệu và câu hỏi hành vi.
5. Tính điểm **bằng mã chương trình**, xếp hạng, tạo báo cáo.
6. **Agent thứ hai** kiểm tra độc lập từng trích dẫn trong phiên mới; câu lỗi bị đánh dấu đỏ.
7. Hỗ trợ người tuyển dụng quyết định: đề xuất nhóm xem xét, soạn **nháp** email. Không tự loại, tự liên hệ hay gửi.

## Bước 1 — Cổng đầu vào (bắt buộc, chưa đọc CV)

Hỏi và chờ người dùng xác nhận. Nếu người dùng đã nêu sẵn một phần, chỉ hỏi phần còn thiếu.

### 1a. Chọn nguồn CV

Hỏi đúng hai lựa chọn:

1. **Gmail** — đọc CV đính kèm từ phạm vi email do người dùng xác định.
2. **Thư mục** — đọc CV trong đường dẫn cục bộ do người dùng cung cấp.

Sau khi người dùng chọn, đọc [references/data-sources.md](references/data-sources.md) và thu thập phạm vi tối thiểu. Không đọc Gmail hoặc thư mục trước khi có xác nhận.

### 1b. Nhận mô tả công việc

Xin **vị trí tuyển dụng** và **mô tả công việc (JD)** (dán văn bản hoặc đường dẫn file). Người dùng không cần tự soạn tiêu chí; agent sẽ đề xuất ở Bước 2. Nếu người dùng muốn nêu sẵn tiêu chí hoặc trọng số, ghi nhận và dùng làm đầu vào cho đề xuất.

### 1c. Hỏi tùy chọn

Hỏi: **“Bạn có muốn gửi báo cáo cho nhà tuyển dụng qua email sau khi hoàn tất không? Nếu có, vui lòng cung cấp email người nhận. Có thể bỏ qua nếu bạn chỉ cần file báo cáo.”** Địa chỉ này là email nhà tuyển dụng/người nhận, không phải email ứng viên. Không chặn việc lọc CV nếu người dùng bỏ qua.

## Bước 2 — Đề xuất và phê duyệt bộ tiêu chí

Đọc [references/ask-scoring.md](references/ask-scoring.md). Từ JD, agent **tự đề xuất** bộ tiêu chí và trình bày cho người dùng:

- **K — Knowledge:** kiến thức nền, lĩnh vực, quy trình, sản phẩm, chứng chỉ. Có điểm.
- **S — Skills:** kỹ năng thực hành, công cụ, số năm kinh nghiệm, KPI/kết quả. Có điểm.
- **A — Attitude:** hành vi quan sát được cần xác minh (ví dụ chủ động, phối hợp, chịu trách nhiệm). **Không có điểm, không có trọng số**; chỉ dùng để tìm dấu hiệu và tạo câu hỏi phỏng vấn.

Mỗi tiêu chí K/S nêu: id, nhóm, mô tả quan sát được, bắt buộc/ưu tiên, trọng số, bằng chứng chấp nhận được. Tổng trọng số K+S = 100. Gợi ý khi JD không nêu gì: S 60 / K 40; nêu rõ đây là giả định.

**Cổng phê duyệt:** dừng lại, cho người dùng điều chỉnh (thêm/bớt/sửa tiêu chí, đổi trọng số, đổi bắt buộc/ưu tiên). Chỉ chuyển sang đọc CV khi người dùng xác nhận rõ bộ tiêu chí cuối cùng. Lưu bộ tiêu chí đã duyệt thành `criteria.json` trong thư mục kết quả để script chấm và agent kiểm tra dùng lại.

Nếu người dùng đưa tiêu chí nhạy cảm (tuổi, giới tính, hôn nhân, ảnh, quê quán, tôn giáo, sức khỏe…), không áp dụng; đề nghị thay bằng yêu cầu nghề nghiệp quan sát được.

## Bước 3 — Đọc và trích xuất CV

1. Lập danh mục toàn bộ CV trong phạm vi đã xác nhận (PDF, Word, ảnh). Giữ tên nguồn để truy vết.
2. Trích xuất nội dung: PDF có text → lấy text kèm **số trang**; DOCX → đọc cấu trúc (mục, bảng, mốc thời gian); PDF scan/ảnh chụp → **OCR hoặc đọc ảnh** để chuyển thành văn bản, đánh dấu đoạn không đọc chắc chắn, không suy đoán phần không đọc được.
3. Lưu văn bản trích xuất kèm vị trí (trang, mục) cho từng CV để làm căn cứ trích dẫn.

Chi tiết nguồn và trích xuất: [references/data-sources.md](references/data-sources.md).

## Bước 4 — Chấm điểm có bằng chứng

Với **mỗi CV × mỗi tiêu chí K/S**:

- Ghi **câu trích nguyên văn** từ CV và **vị trí** (trang, mục). Không diễn giải lại thay cho trích dẫn.
- Chọn mức bằng chứng 0–3 theo [references/ask-scoring.md](references/ask-scoring.md).
- Nếu CV không có bằng chứng: ghi **“Không tìm thấy”** và chấm **0**. Không biến thành suy đoán tiêu cực.

Với **Thái độ**: tuyệt đối không chấm điểm, không đưa vào điểm tổng, không xếp hạng theo Thái độ. Chỉ ghi (a) các dấu hiệu hành vi có trong CV kèm trích dẫn và vị trí, nếu có; (b) **dấu hiệu ổn định công việc** trích từ mốc thời gian trong CV (số công ty, số tháng ở mỗi vị trí, khoảng trống): gắn nhãn khi có từ 2 vị trí dưới 6 tháng trong 3 năm gần nhất hoặc có vị trí dưới 3 tháng (ngưỡng mặc định, người dùng có thể đổi khi duyệt tiêu chí). Nhãn này chỉ là dữ kiện để hỏi lại, không suy ra thái độ vì CV không cho biết lý do (cắt giảm, hết hợp đồng, dự án ngắn hạn…); (c) 2–4 câu hỏi phỏng vấn hành vi (STAR) để người tuyển dụng xác minh, kèm câu hỏi về lý do rời vị trí ngắn hạn nếu có nhãn. Mọi dấu hiệu phải thuộc nhóm hành vi đã được duyệt ở Bước 2; dấu hiệu nằm ngoài nhóm đó sẽ bị Agent kiểm tra gắn *Sai ngữ cảnh*.

Với mỗi ứng viên, tạo thêm câu hỏi làm rõ cho các khoảng trống K/S và số liệu cần xác minh.

## Bước 5 — Tính điểm, xếp hạng, tạo báo cáo

1. Ghi kết quả chấm của từng tiêu chí vào một file dữ liệu có cấu trúc (`scores.json`).
2. **Tính tổng điểm, điểm K, điểm S, độ bao phủ và thứ hạng bằng mã chương trình** (script Python hoặc JS chạy thật), không tính nhẩm. Lưu script cùng thư mục kết quả để kiểm tra lại.
3. Đọc [references/deliverables.md](references/deliverables.md), tạo Excel và HTML từ dữ liệu đã tính. Dùng kỹ năng bảng tính hiện có cho Excel và kỹ năng Sites hiện có cho HTML.
4. Đề xuất nhóm ứng viên HR nên xem xét phỏng vấn, kèm lý do. Tiêu chí bắt buộc bị “Không tìm thấy”/“Không đáp ứng” phải hiển thị nổi bật dù tổng điểm cao.

## Bước 6 — Agent thứ hai kiểm tra độc lập

Đọc [references/verification.md](references/verification.md). Sau khi có báo cáo, chạy **Agent kiểm tra** trong một **phiên mới** (ưu tiên subagent không kế thừa ngữ cảnh; nếu không có, hướng dẫn người dùng mở phiên mới). Agent này chỉ nhận: báo cáo (`scores.json` / Excel), `criteria.json` và CV gốc. **Không** nhận lập luận, ghi chú hay văn bản trích xuất trung gian của Agent thứ nhất.

Agent kiểm tra xét từng câu trích, ngữ cảnh, trọng số và nhận xét không có bằng chứng, rồi gán một trong ba trạng thái: **Khớp**, **Không tìm thấy**, **Sai ngữ cảnh**. Agent thứ nhất ghép kết quả vào báo cáo; mọi câu *Không tìm thấy* hoặc *Sai ngữ cảnh* được **đánh dấu đỏ** trong cả HTML và Excel, và điểm tiêu chí liên quan được gắn cờ “cần rà soát”. Không tự sửa điểm để che lỗi; trình bày cho người dùng quyết định.

## Bước 7 — Hỗ trợ người tuyển dụng quyết định

- Đề xuất nhóm ứng viên phù hợp để xem xét phỏng vấn; không tự loại ai.
- Khi người tuyển dụng yêu cầu, soạn **nháp** email mời phỏng vấn hoặc email cảm ơn cho từng ứng viên hoặc nhóm. Chỉ soạn nháp để duyệt, không dùng thông tin nhạy cảm, không nêu điểm số hay lý do loại trong thư.
- **Không tự liên hệ ứng viên và không gửi email** (kể cả tạo bản nháp trong hộp thư) khi người tuyển dụng chưa quyết định và chưa xác nhận rõ.

### Gửi báo cáo cho nhà tuyển dụng (nếu đã chọn ở Bước 1c)

Xác nhận tệp đính kèm (Excel, HTML hoặc cả hai) và nội dung thư. Trước khi gửi, trình bày người nhận, tiêu đề, nội dung và tệp đính kèm để người dùng duyệt. Chỉ gửi sau khi người dùng xác nhận rõ nội dung cuối cùng. Không tự gửi CV gốc hoặc thêm người nhận khác. Nếu không có công cụ gửi email, cung cấp nội dung thư để người dùng tự gửi.

## Bàn giao

Nêu ngắn gọn: số CV đã xử lý và nguồn; bộ tiêu chí và trọng số đã duyệt; nhóm nên xem xét phỏng vấn; kết quả kiểm tra độc lập (số câu Khớp / Không tìm thấy / Sai ngữ cảnh); đường dẫn Excel và HTML; các file không đọc được hoặc giới hạn khác.

## Nguyên tắc tuyển dụng công bằng

- Chỉ đánh giá bằng tiêu chí liên quan trực tiếp tới công việc.
- Không dùng hoặc suy luận từ tuổi, giới tính, tình trạng hôn nhân, ảnh, dân tộc, tôn giáo, sức khỏe, khuyết tật, thai sản, hoàn cảnh gia đình, quê quán, quan điểm chính trị hoặc thông tin nhạy cảm khác.
- Tên ứng viên chỉ dùng để nhận diện hồ sơ, không được dùng làm tín hiệu đánh giá.
- Không suy luận Thái độ từ ảnh, cách trình bày CV, sở thích hoặc tính từ tự mô tả; và không chấm điểm Thái độ.
- Giữ nguyên CV gốc. Khi thu thập qua Gmail, chỉ đọc email và tệp trong phạm vi được duyệt; không thay đổi trạng thái, nhãn hoặc nội dung thư.
