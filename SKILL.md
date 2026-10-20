---
name: agent-loc-cv
description: Sàng lọc CV theo khung ASK (Attitude, Skills, Knowledge) từ Gmail hoặc thư mục người dùng cung cấp. Agent tự đề xuất bộ tiêu chí từ mô tả công việc để người dùng duyệt; chấm Kiến thức và Kỹ năng có trích dẫn nguyên văn, KHÔNG chấm Thái độ (chỉ ghi dấu hiệu và câu hỏi hành vi); tính điểm bằng mã; một agent thứ hai kiểm tra độc lập các trích dẫn; xuất báo cáo HTML "CV Radar" tự chứa (xem được ảnh CV trong trình duyệt của Claude Code và Codex) + Excel, và nháp email cho người tuyển dụng quyết định. Dùng khi người dùng muốn đọc, đối chiếu, chấm điểm hoặc lập shortlist CV.
---

# Lọc CV theo ASK

Tạo một quy trình sàng lọc có thể kiểm tra lại bằng bằng chứng. Điểm số chỉ phản ánh mức độ bằng chứng trong CV về **Kiến thức và Kỹ năng**; không phải phán quyết năng lực hoặc quyết định tuyển/loại. **Thái độ (Attitude) không được chấm điểm.**

Skill chạy trên **Claude Code** và **Codex**. Mã nằm trong `scripts/` (Python 3.9+; cần `pillow`, `openpyxl`, `pymupdf`, `python-docx`). Luôn chạy Python với `-X utf8` trên Windows. Đường dẫn `scripts/`, `assets/`, `references/` tính từ thư mục chứa file SKILL.md này.

## Tổng quan quy trình

1. Cổng đầu vào: chọn nguồn CV + nhận mô tả công việc (JD).
2. Agent đọc JD, **tự đề xuất** bộ tiêu chí ASK + trọng số → người dùng điều chỉnh và **phê duyệt**.
3. Chỉ sau khi được duyệt mới chuẩn bị, đọc và trích xuất CV (`scripts/chuan_bi_cv.py`).
4. Chấm K và S có trích dẫn nguyên văn + vị trí; Thái độ chỉ ghi dấu hiệu và câu hỏi hành vi. Ghi `scores.json`.
5. Tính điểm **bằng mã** (`scripts/tinh_diem.py`).
6. **Agent thứ hai** kiểm tra độc lập từng trích dẫn trong phiên mới (có thể chia nhiều agent chạy song song).
7. Tạo báo cáo (`scripts/tao_bao_cao.py`): `index.html` tự chứa + Excel; kiểm tra bằng trình duyệt.
8. Bàn giao, hỗ trợ người tuyển dụng quyết định: đề xuất nhóm xem xét, soạn **nháp** email. Không tự loại, tự liên hệ hay gửi.

## Bước 1 — Cổng đầu vào (bắt buộc, chưa đọc CV)

Hỏi và chờ người dùng xác nhận. Nếu người dùng đã nêu sẵn một phần (ví dụ đã đưa đường dẫn thư mục và file JD), chỉ hỏi phần còn thiếu.

### 1a. Chọn nguồn CV

Hỏi đúng hai lựa chọn:

1. **Gmail** — đọc CV đính kèm từ phạm vi email do người dùng xác định.
2. **Thư mục** — đọc CV trong đường dẫn cục bộ do người dùng cung cấp.

Sau khi người dùng chọn, đọc [references/data-sources.md](references/data-sources.md) và thu thập phạm vi tối thiểu. Không đọc Gmail hoặc thư mục trước khi có xác nhận.

### 1b. Nhận mô tả công việc

Xin **vị trí tuyển dụng** và **mô tả công việc (JD)** (dán văn bản hoặc đường dẫn file; DOCX/PDF thì tự đọc). Người dùng không cần tự soạn tiêu chí; agent sẽ đề xuất ở Bước 2. Nếu người dùng muốn nêu sẵn tiêu chí hoặc trọng số, ghi nhận và dùng làm đầu vào cho đề xuất.

### 1c. Hỏi tùy chọn

Hỏi: **“Bạn có muốn gửi báo cáo cho nhà tuyển dụng qua email sau khi hoàn tất không? Nếu có, vui lòng cung cấp email người nhận. Có thể bỏ qua nếu bạn chỉ cần file báo cáo.”** Địa chỉ này là email nhà tuyển dụng/người nhận, không phải email ứng viên. Không chặn việc lọc CV nếu người dùng bỏ qua.

## Bước 2 — Đề xuất và phê duyệt bộ tiêu chí

Đọc [references/ask-scoring.md](references/ask-scoring.md). Từ JD, agent **tự đề xuất** bộ tiêu chí và trình bày cho người dùng:

- **K — Knowledge:** kiến thức nền, lĩnh vực, quy trình, sản phẩm, chứng chỉ. Có điểm.
- **S — Skills:** kỹ năng thực hành, công cụ, số năm kinh nghiệm, KPI/kết quả. Có điểm.
- **A — Attitude:** hành vi quan sát được cần xác minh (ví dụ chủ động, phối hợp, chịu trách nhiệm). **Không có điểm, không có trọng số**; chỉ dùng để tìm dấu hiệu và tạo câu hỏi phỏng vấn.

Mỗi tiêu chí K/S nêu: id, nhóm, mô tả quan sát được, bắt buộc/ưu tiên, trọng số, bằng chứng chấp nhận được. Tổng trọng số K+S = 100. Gợi ý khi JD không nêu gì: S 60 / K 40; nêu rõ đây là giả định. Nếu JD có ẩn số (ví dụ "X năm kinh nghiệm") phải **hỏi giá trị** hoặc nêu rõ giả định đã chọn khi trình bày.

**Cổng phê duyệt:** dừng lại, cho người dùng điều chỉnh (thêm/bớt/sửa tiêu chí, đổi trọng số, đổi bắt buộc/ưu tiên). Chỉ chuyển sang đọc CV khi người dùng xác nhận rõ bộ tiêu chí cuối cùng. Lưu bộ tiêu chí đã duyệt thành `criteria.json` trong thư mục kết quả (lược đồ ở [references/schema-du-lieu.md](references/schema-du-lieu.md)) để script chấm và agent kiểm tra dùng lại.

Nếu người dùng đưa tiêu chí nhạy cảm (tuổi, giới tính, hôn nhân, ảnh, quê quán, tôn giáo, sức khỏe…), không áp dụng; đề nghị thay bằng yêu cầu nghề nghiệp quan sát được.

## Bước 3 — Chuẩn bị và đọc CV

1. Tạo thư mục kết quả `ket-qua-loc-cv-<vi-tri>-<yyyymmdd>/` (không đè lên thư mục kết quả cũ; file cũ trong đó giữ nguyên).
2. Chạy `python -X utf8 scripts/chuan_bi_cv.py "<thu_muc_cv>" "<thu_muc_ket_qua>"`. Script sao chép CV gốc vào `assets/cv/`, tạo ảnh xem trước `assets/preview/*.jpg` (ảnh nén; PDF ghép tối đa 4 trang; DOCX qua LibreOffice nếu có), trích văn bản PDF/DOCX có text vào `.work/van-ban/` và ghi `anh_xa_cv.json`.
3. Đọc nội dung: PDF/DOCX có text → dùng văn bản trích, **luôn giữ số trang/mục**; ảnh và PDF scan → **mở ảnh bằng công cụ đọc ảnh và đọc bằng thị giác**, đánh dấu đoạn không chắc, không suy đoán phần không đọc được.

Chi tiết nguồn và trích xuất: [references/data-sources.md](references/data-sources.md).

## Bước 4 — Chấm điểm có bằng chứng

Với **mỗi CV × mỗi tiêu chí K/S**:

- Ghi **câu trích nguyên văn** từ CV và **vị trí** (trang, mục). Không diễn giải lại thay cho trích dẫn.
- Chọn mức bằng chứng 0–3 theo [references/ask-scoring.md](references/ask-scoring.md), gồm các **quy tắc nhất quán** ở cuối file đó (mức 3 cần số liệu hoặc lặp ở ≥2 vai trò; không tính hoạt động ngoài lĩnh vực như bằng chứng trực tiếp; không dùng một câu để nâng điểm nhiều tiêu chí).
- Nếu CV không có bằng chứng: ghi **“Không tìm thấy”** và chấm **0**. Không biến thành suy đoán tiêu cực.

Với **Thái độ**: tuyệt đối không chấm điểm, không đưa vào điểm tổng, không xếp hạng theo Thái độ. Chỉ ghi (a) các dấu hiệu hành vi có trong CV kèm trích dẫn và vị trí, nếu có (câu phải **thể hiện hành vi**, không chỉ là mô tả đầu việc); (b) **dấu hiệu ổn định công việc** trích từ mốc thời gian trong CV (số công ty, số tháng ở mỗi vị trí, khoảng trống): gắn nhãn khi có từ 2 vị trí dưới 6 tháng trong 3 năm gần nhất hoặc có vị trí dưới 3 tháng (ngưỡng mặc định, người dùng có thể đổi khi duyệt tiêu chí). Nhãn này chỉ là dữ kiện để hỏi lại, không suy ra thái độ vì CV không cho biết lý do (cắt giảm, hết hợp đồng, dự án ngắn hạn…); (c) 2–4 câu hỏi phỏng vấn hành vi (STAR) để người tuyển dụng xác minh, kèm câu hỏi về lý do rời vị trí ngắn hạn nếu có nhãn. Mọi dấu hiệu phải thuộc nhóm hành vi đã được duyệt ở Bước 2; dấu hiệu nằm ngoài nhóm đó sẽ bị Agent kiểm tra gắn *Sai ngữ cảnh*.

Với mỗi ứng viên, tạo thêm: câu hỏi làm rõ cho các khoảng trống K/S và số liệu cần xác minh; điểm mạnh, lưu ý; và khối `tom_tat` (thẻ ưu tiên, lý do cho HR). Ghi tất cả vào `scores.json` theo [references/schema-du-lieu.md](references/schema-du-lieu.md).

## Bước 5 — Tính điểm, xếp hạng

Chạy `python -X utf8 scripts/tinh_diem.py "<thu_muc_ket_qua>"`. Script kiểm tra tổng trọng số = 100, báo lỗi nếu mức > 0 thiếu trích dẫn/vị trí, tính tổng điểm, điểm K, điểm S, độ bao phủ, thứ hạng (đồng hạng nếu bằng điểm), nhãn ổn định công việc, rồi ghi `ket_qua_tinh_diem.json` và chép chính nó vào thư mục kết quả. **Không tính nhẩm.** Sửa lỗi dữ liệu nếu script báo; xem các cảnh báo.

## Bước 6 — Agent thứ hai kiểm tra độc lập

Đọc [references/verification.md](references/verification.md). Chạy **Agent kiểm tra** trong **phiên mới** (subagent không kế thừa ngữ cảnh; nếu không có subagent, hướng dẫn người dùng mở phiên mới). Có thể chia ứng viên thành nhiều agent (mỗi agent khoảng 3–4 CV) chạy song song, mỗi agent ghi `verification_<A|B|C…>.json`. Agent này chỉ nhận: `scores.json`, `criteria.json` và CV gốc. **Không** nhận lập luận, ghi chú hay văn bản trích xuất trung gian của Agent thứ nhất.

Agent kiểm tra xét từng câu trích (K/S và Thái độ), cả các khẳng định “CV không nêu”, rồi gán **Khớp**, **Không tìm thấy**, **Sai ngữ cảnh**, và ghi thêm nhận xét về điểm bị thổi phồng/bỏ sót. **Không tự sửa điểm để che lỗi**; trình bày cho người dùng quyết định (xem Bàn giao).

## Bước 7 — Tạo báo cáo và kiểm tra bằng trình duyệt

1. Chạy `python -X utf8 scripts/tao_bao_cao.py "<thu_muc_ket_qua>"`. Script ghép `verification_*.json` và tạo:
   - `index.html` — **tự chứa**, ảnh CV nhúng dạng data URI. Bắt buộc như vậy vì trình duyệt tích hợp của Claude Code và Codex mở file cục bộ như trang `data:`; ảnh tham chiếu bằng đường dẫn tương đối hoặc `localhost` sẽ không hiện.
   - `Danh_gia_CV_<vi_tri>.xlsx` — năm sheet.
   - `verification.json`, `verification_nhan_xet.json`, `tong_hop.json`.
2. **Bắt buộc kiểm tra** trước khi bàn giao theo checklist ở [references/deliverables.md](references/deliverables.md): mở `index.html` trong trình duyệt (khởi động máy chủ tĩnh cục bộ chỉ để kiểm tra), xem console không có lỗi JavaScript, đủ thẻ/bảng, mở hộp chi tiết và tab **CV gốc** thấy ảnh. `node --check` không bắt được lỗi trùng tên biến toàn cục của trình duyệt (như `top`), nên phải chạy trên trình duyệt thật.
3. Giao diện, Excel và hợp đồng đầu ra: [references/deliverables.md](references/deliverables.md). Không tự đổi bố cục khác với hợp đồng này.

## Bước 8 — Hỗ trợ người tuyển dụng quyết định

- Đề xuất nhóm ứng viên phù hợp để xem xét phỏng vấn; không tự loại ai.
- Khi người tuyển dụng yêu cầu, soạn **nháp** email mời phỏng vấn hoặc email cảm ơn cho từng ứng viên hoặc nhóm vào `email-nhap.md`. Chỉ soạn nháp để duyệt, không dùng thông tin nhạy cảm, không nêu điểm số hay lý do loại trong thư.
- **Không tự liên hệ ứng viên và không gửi email** (kể cả tạo bản nháp trong hộp thư) khi người tuyển dụng chưa quyết định và chưa xác nhận rõ.

### Gửi báo cáo cho nhà tuyển dụng (nếu đã chọn ở Bước 1c)

Xác nhận tệp đính kèm (Excel, HTML hoặc cả hai) và nội dung thư. Trước khi gửi, trình bày người nhận, tiêu đề, nội dung và tệp đính kèm để người dùng duyệt. Chỉ gửi sau khi người dùng xác nhận rõ nội dung cuối cùng. Không tự gửi CV gốc hoặc thêm người nhận khác. Nếu không có công cụ gửi email, cung cấp nội dung thư để người dùng tự gửi.

## Bàn giao

Nêu ngắn gọn: số CV đã xử lý và nguồn; bộ tiêu chí và trọng số đã duyệt (kèm giả định); bảng xếp hạng ngắn; nhóm nên xem xét phỏng vấn; kết quả kiểm tra độc lập (số câu Khớp / Không tìm thấy / Sai ngữ cảnh, số khẳng định “không nêu” đúng/sai); **các điểm Agent 2 đề nghị xem lại để người dùng quyết định giữ hay chấm lại** (chưa sửa); đường dẫn `index.html` và Excel; các file không đọc được, nghi trùng nội dung hoặc giới hạn khác.

## Nguyên tắc tuyển dụng công bằng

- Chỉ đánh giá bằng tiêu chí liên quan trực tiếp tới công việc.
- Không dùng hoặc suy luận từ tuổi, giới tính, tình trạng hôn nhân, ảnh, dân tộc, tôn giáo, sức khỏe, khuyết tật, thai sản, hoàn cảnh gia đình, quê quán, quan điểm chính trị hoặc thông tin nhạy cảm khác.
- Tên ứng viên chỉ dùng để nhận diện hồ sơ, không được dùng làm tín hiệu đánh giá.
- Không suy luận Thái độ từ ảnh, cách trình bày CV, sở thích hoặc tính từ tự mô tả; và không chấm điểm Thái độ.
- Giữ nguyên CV gốc. Khi thu thập qua Gmail, chỉ đọc email và tệp trong phạm vi được duyệt; không thay đổi trạng thái, nhãn hoặc nội dung thư.
