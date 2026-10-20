# Agent lọc CV tuyển dụng (skill `agent-loc-cv`)

Skill cho **Claude Code** và **Codex**: sàng lọc CV theo khung **ASK** (Attitude · Skills · Knowledge) có bằng chứng, kiểm tra độc lập bằng agent thứ hai, xuất báo cáo **HTML "CV Radar"** (xem được ảnh CV ngay trong trình duyệt tích hợp) và **Excel**.

- Điểm chỉ gồm **K và S**, mỗi điểm có trích dẫn nguyên văn + vị trí. **Thái độ không chấm điểm**, chỉ ghi dấu hiệu và câu hỏi phỏng vấn STAR.
- Điểm tính bằng mã (`scripts/tinh_diem.py`), không tính nhẩm.
- Agent thứ hai đối chiếu từng trích dẫn với CV gốc; câu sai bị tô đỏ. Không tự sửa điểm.
- Không tự loại ứng viên, không tự liên hệ hay gửi email.

## Cài đặt

Chép cả thư mục này vào thư mục skill rồi mở phiên mới:

| Công cụ | Thư mục skill |
|---|---|
| Claude Code | `~/.claude/skills/agent-loc-cv/` (Windows: `C:\Users\<tên>\.claude\skills\agent-loc-cv\`) |
| Codex | `~/.codex/skills/agent-loc-cv/` (hoặc `.agents/skills/` trong dự án) |

```bash
git clone https://github.com/slimsoftvietnam/ai-agent-loc-cv-tuyen-dung ~/.claude/skills/agent-loc-cv
python -m pip install pillow openpyxl pymupdf python-docx
```

Yêu cầu: Python 3.9+. DOCX muốn có ảnh xem trước thì cần LibreOffice (không bắt buộc). Gmail chỉ cần khi chọn nguồn CV là Gmail.

## Cách dùng

Gõ `/agent-loc-cv` (Claude Code) hoặc `$agent-loc-cv` (Codex), rồi trả lời: nguồn CV (Gmail hoặc thư mục), vị trí + JD. Agent đề xuất tiêu chí để bạn duyệt, sau đó đọc CV, chấm điểm, cho agent thứ hai kiểm tra, và tạo báo cáo.

## Kết quả

Thư mục `ket-qua-loc-cv-<vi-tri>-<yyyymmdd>/` gồm `index.html` (tự chứa, ảnh CV nhúng sẵn nên xem được trong trình duyệt của Claude Code/Codex), `Danh_gia_CV_<vi_tri>.xlsx`, `criteria.json`, `scores.json`, `verification*.json`, `tinh_diem.py`. Chi tiết bố cục và checklist kiểm tra: `references/deliverables.md`.

## Cấu trúc

```text
SKILL.md                  quy trình 8 bước
agents/openai.yaml        cấu hình hiển thị cho Codex
references/               tiêu chí ASK, nguồn CV, hợp đồng đầu ra, kiểm tra độc lập, lược đồ dữ liệu
scripts/                  chuan_bi_cv.py · tinh_diem.py · tao_bao_cao.py
assets/                   mau_bao_cao.html · giao_dien.js (giao diện CV Radar)
```

Điểm là điểm bằng chứng trong CV, hỗ trợ rà soát; **quyết định tuyển/loại thuộc về người tuyển dụng**.
