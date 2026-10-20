---
name: agent-loc-cv
description: Sàng lọc CV theo khung ASK (Attitude, Skills, Knowledge) từ Gmail hoặc thư mục người dùng cung cấp; tạo báo cáo Excel và HTML có bằng chứng, điểm phù hợp, câu hỏi xác minh và CV gốc. Dùng khi người dùng muốn đọc, đối chiếu, chấm điểm hoặc lập shortlist CV theo tiêu chí tuyển dụng.
---

# Lọc CV theo ASK

Tạo một quy trình sàng lọc có thể kiểm tra lại bằng bằng chứng. Điểm số chỉ phản ánh mức độ bằng chứng trong CV, không phải phán quyết năng lực hoặc quyết định tuyển/loại.

## Cổng đầu vào bắt buộc

Trước khi đọc bất kỳ CV nào, hỏi và chờ người dùng xác nhận hai nhóm thông tin dưới đây. Nếu người dùng đã nêu sẵn một phần, chỉ hỏi phần còn thiếu; vẫn xác nhận phạm vi nguồn trước khi truy cập.

### 1. Chọn nguồn CV

Hỏi đúng hai lựa chọn:

1. **Gmail** — đọc CV đính kèm từ phạm vi email do người dùng xác định.
2. **Thư mục** — đọc CV trong đường dẫn cục bộ do người dùng cung cấp.

Sau khi người dùng chọn, đọc [references/data-sources.md](references/data-sources.md) và thu thập phạm vi tối thiểu cần thiết. Không đọc Gmail hoặc thư mục trước khi có xác nhận.

### 2. Thu thập tiêu chí ASK

Giải thích ngắn:

- **A — Attitude:** hành vi/thái độ quan sát được trong công việc, ví dụ chủ động, phối hợp, học hỏi, chịu trách nhiệm.
- **S — Skills:** kỹ năng thực hành và công cụ cần dùng để làm việc.
- **K — Knowledge:** kiến thức nền, lĩnh vực, quy trình, sản phẩm hoặc chứng chỉ cần biết.

Đưa mẫu điền có gợi ý, rồi chờ người dùng trả lời:

```text
Vị trí tuyển dụng:
Mô tả công việc:

A — Attitude
- Hành vi mong muốn (gợi ý: chủ động, phối hợp Sales, chịu trách nhiệm kết quả):
- Bằng chứng nào được chấp nhận?
- Tiêu chí bắt buộc / ưu tiên:

S — Skills
- Kỹ năng, công cụ, số năm kinh nghiệm (gợi ý: Google Ads, Meta Ads, Canva, content, GA4):
- Mức độ cần thiết: bắt buộc / ưu tiên:
- Kết quả hoặc KPI mong muốn:

K — Knowledge
- Kiến thức cần có (gợi ý: B2B/SaaS, funnel, SEO, landing page, attribution):
- Mức độ cần thiết: bắt buộc / ưu tiên:

Trọng số A/S/K (tổng 100, có thể bỏ trống):
Ngưỡng/điều kiện cần HR lưu ý:
```

Nếu người dùng không chọn trọng số, dùng mặc định **A 20 / S 50 / K 30** và nêu rõ giả định trước khi chấm. Đọc [references/ask-scoring.md](references/ask-scoring.md) trước khi lập ma trận và tính điểm.

## Thực hiện

1. Lập danh mục tất cả CV trong phạm vi đã xác nhận. Giữ tên nguồn để truy vết.
2. Trích xuất nội dung từ PDF, DOCX và ảnh bằng công cụ phù hợp. Với file scan, dùng OCR/đọc ảnh; không suy đoán phần không đọc được.
3. Chuẩn hóa từng tiêu chí ASK thành: nhóm A/S/K, bắt buộc/ưu tiên, trọng số, bằng chứng chấp nhận được.
4. Đối chiếu từng ứng viên với từng tiêu chí. Ghi trạng thái, bằng chứng cụ thể và nguồn CV.
5. Phân biệt rõ:
   - **Đáp ứng:** có bằng chứng trực tiếp.
   - **Đáp ứng một phần:** bằng chứng gián tiếp hoặc chưa đủ phạm vi.
   - **Không đáp ứng:** CV có thông tin rõ ràng trái với yêu cầu tối thiểu.
   - **Chưa đủ bằng chứng:** CV không nêu; không được biến thành suy đoán tiêu cực.
6. Tính **điểm bằng chứng phù hợp** và độ bao phủ theo [references/ask-scoring.md](references/ask-scoring.md).
7. Đề xuất nhóm HR nên xem kỹ hơn; không tự động quyết định tuyển hoặc loại.
8. Với mỗi ứng viên, tạo câu hỏi phỏng vấn nhắm đúng các khoảng trống ASK và số liệu cần xác minh.

## Gửi báo cáo cho nhà tuyển dụng (tùy chọn)

Trong bước thu thập đầu vào, hỏi thêm: **“Bạn có muốn gửi báo cáo cho nhà tuyển dụng qua email sau khi hoàn tất không? Nếu có, vui lòng cung cấp email người nhận. Có thể bỏ qua nếu bạn chỉ cần file báo cáo.”** Địa chỉ được hỏi là email nhà tuyển dụng/người nhận, không phải email ứng viên. Nếu người dùng chọn gửi, xác nhận tệp muốn đính kèm (Excel, HTML hoặc cả hai) và thông tin cần có trong thư. Không chặn việc lọc CV nếu người dùng không muốn gửi email.

Trước khi gửi, trình bày người nhận, tiêu đề, nội dung thư và danh sách tệp đính kèm để người dùng duyệt. Chỉ gửi sau khi người dùng xác nhận rõ nội dung cuối cùng. Không tự gửi CV gốc hoặc thêm người nhận khác nếu chưa được yêu cầu. Nếu không có công cụ gửi email được kết nối, cung cấp nội dung thư để người dùng tự gửi.

## Đầu ra bắt buộc

Luôn tạo cả hai đầu ra trong cùng một thư mục kết quả:

1. Một file `.xlsx` dễ kiểm tra và có ma trận ASK.
2. Một báo cáo HTML responsive, font **K2D**, ít chữ và có tương tác.

Đọc [references/deliverables.md](references/deliverables.md) trước khi tạo file. Dùng kỹ năng bảng tính hiện có cho Excel và kỹ năng Sites hiện có cho HTML. Xác minh nội dung, công thức, liên kết CV và khả năng mở chi tiết ứng viên trước khi bàn giao.

### Quy ước giao diện HTML

- Thẻ ứng viên ở danh sách/nhóm ưu tiên bên ngoài chỉ hiển thị **điểm tổng / 100**; không hiển thị điểm A/S/K hoặc phần trăm tiêu chí có bằng chứng trên thẻ. Có thể giữ điểm chi tiết bên trong phần tóm tắt hồ sơ.
- Khi mở một ứng viên, chỉ dùng hai phần/tab nhìn thấy được: **Tóm tắt** và **CV gốc**. Đưa điểm tổng và A/S/K, tiêu chí phù hợp/chưa phù hợp/chưa đủ bằng chứng, bằng chứng và câu hỏi phỏng vấn vào **Tóm tắt**.
- Trong phần **Tóm tắt**, thể hiện điểm A/S/K bằng biểu đồ năng lực dạng mạng nhện gọn, dễ đọc, có nhãn và giá trị rõ ràng. Dùng khoảng cách thoải mái giữa các khối và chữ nhỉnh hơn cỡ chú thích; vẫn ưu tiên ít chữ, dễ quét.
- Trên trang bên ngoài, đặt cỡ chữ nội dung thường đủ dễ đọc (khoảng 16px desktop, không thu nhỏ các chú thích quan trọng quá mức). Trong **CV gốc**, cho ảnh xem trước lớn nhất có thể trong khung, giữ nguyên tỷ lệ, không cắt; cho phép cuộn nếu ảnh cao hơn màn hình.
- Giữ giao diện gọn, giàu tương phản và có màu sắc nhất quán; dùng card phân cấp rõ, huy hiệu/thứ tự, chip điểm mạnh và dòng ngắn về nội dung cần xác minh. Có thể dùng một card nổi bật cho ứng viên xếp đầu; không chép cứng nội dung hay tên trong ảnh tham khảo.
- Lược bỏ chú thích, nhãn lặp và đoạn hướng dẫn không cần cho thao tác. Giữ phần giải thích ASK trong khối thu gọn bắt buộc để người xem chủ động mở khi cần.

## Nguyên tắc tuyển dụng công bằng

- Chỉ đánh giá bằng tiêu chí liên quan trực tiếp tới công việc.
- Không dùng hoặc suy luận từ tuổi, giới tính, tình trạng hôn nhân, ảnh, dân tộc, tôn giáo, sức khỏe, khuyết tật, thai sản, hoàn cảnh gia đình, quan điểm chính trị hoặc thông tin nhạy cảm khác.
- Tên ứng viên được dùng để nhận diện hồ sơ, không được dùng làm tín hiệu đánh giá.
- Không suy luận Attitude từ ảnh, cách trình bày CV, sở thích hoặc các tính từ tự mô tả thiếu bằng chứng.
- Nếu người dùng cung cấp tiêu chí nhạy cảm, không áp dụng tiêu chí đó; đề nghị thay bằng yêu cầu nghề nghiệp quan sát được.
- Giữ nguyên CV gốc. Khi thu thập CV qua Gmail, chỉ đọc email và tệp trong phạm vi được duyệt; không thay đổi trạng thái, nhãn hoặc nội dung thư. Việc gửi báo cáo là bước riêng, tùy chọn, tuân theo quy trình xác nhận ở trên.
