# Lược đồ dữ liệu (`criteria.json`, `scores.json`)

Hai file này là nguồn duy nhất cho `scripts/tinh_diem.py` và `scripts/tao_bao_cao.py`. Viết bằng UTF-8. Có thể sinh bằng một script Python ngắn (ghi bằng `json.dump(..., ensure_ascii=False)`).

## criteria.json

```json
{
  "vi_tri": "Chuyên viên Digital Marketing",
  "ngay_duyet": "2026-10-20",
  "gia_dinh": ["Trọng số K 40 / S 60 là giả định mặc định vì JD không nêu.", "X = 2 năm là giả định."],
  "tieu_chi": [
    {"id": "K1", "nhom": "K", "mo_ta": "Tốt nghiệp Đại học Marketing, Truyền thông hoặc liên quan",
     "muc_do": "Bắt buộc", "trong_so": 10, "bang_chung_chap_nhan": "Mục Học vấn nêu chuyên ngành"},
    {"id": "S1", "nhom": "S", "mo_ta": "Có từ 2 năm kinh nghiệm ...", "muc_do": "Bắt buộc", "trong_so": 10,
     "bang_chung_chap_nhan": "...",
     "kiem_tra_thoi_gian": {"nguong_thang": {"3": 36, "2": 24, "1": 12}, "tuong_duong_toi_da": 2}}
  ],
  "tong_trong_so": 100,
  "mo_ta_nhom": {"A": "...", "S": "...", "K": "..."},
  "thai_do": {"nhom_hanh_vi": ["Giao tiếp và làm việc nhóm", "Tư duy phân tích và phản biện", "Chủ động và chịu trách nhiệm kết quả", "Ổn định công việc"],
              "nguong_on_dinh": {"so_vi_tri_duoi_6_thang": 2, "trong_so_nam_gan_nhat": 3, "vi_tri_duoi_3_thang": 1}},
  "muc_phu_hop": [{"tu": 85, "nhan": "Bằng chứng phù hợp rất mạnh"}, {"tu": 70, "nhan": "Bằng chứng phù hợp tốt"},
                  {"tu": 50, "nhan": "Bằng chứng phù hợp một phần"}, {"tu": 0, "nhan": "Bằng chứng còn hạn chế"}]
}
```

- `nhom` là `K` hoặc `S` (Thái độ không có trong `tieu_chi`). `muc_do`: `Bắt buộc` hoặc `Ưu tiên`. Tổng `trong_so` = 100.
- `kiem_tra_thoi_gian` (tùy chọn, gắn vào tiêu chí số năm kinh nghiệm): script so mức đã chấm với số tháng tính từ `thoi_gian_lam_viec` và **cảnh báo** nếu lệch (không tự đổi điểm). Vị trí `tuong_duong` bị chặn ở mức `tuong_duong_toi_da`.
- `mo_ta_nhom` (tùy chọn) là chữ hiện trong khối “ASK là gì?”.

## scores.json

```json
{
  "vi_tri": "Chuyên viên Digital Marketing", "ngay": "2026-10-20",
  "nguon": "Thư mục ...\\Mẫu CV (11 file ảnh)", "pham_vi": "11 ảnh JPG/WEBP",
  "ung_vien": [{
    "key": "cv01", "ten": "Nguyễn Văn A", "file_goc": "tên file gốc.jpg",
    "file_luu": "assets/cv/cv01-nguyen-van-a.jpg", "xem_truoc": "assets/preview/cv01.jpg",
    "chuc_danh_trong_cv": "Senior Digital Marketing",
    "diem": {
      "K1": {"muc": 3, "trang_thai": "Đáp ứng",
             "trich_dan": [{"text": "Cử nhân Marketing", "vi_tri": "ảnh 1/1, Học vấn"}], "nhan_xet": "..."},
      "S2": {"muc": 0, "trang_thai": "Không tìm thấy", "trich_dan": [], "nhan_xet": "CV không nêu."}
    },
    "thoi_gian_lam_viec": [
      {"vai_tro": "Senior Digital Marketing", "don_vi": "Công ty X", "bat_dau": "2023-07", "ket_thuc": null,
       "tinh_chat": "chinh", "do_chinh_xac": "thang"}
    ],
    "thai_do": {"dau_hieu": [{"nhom": "Giao tiếp và làm việc nhóm", "text": "câu trích nguyên văn", "vi_tri": "ảnh 1/1, Kinh nghiệm"}],
                "cau_hoi_star": ["...", "..."]},
    "cau_hoi_lam_ro": ["..."], "diem_manh": ["..."], "luu_y": ["..."],
    "tom_tat": {"tin_hieu": ["4+ năm Digital", "Ads đa kênh"], "can_xac_minh": "Công cụ phân tích web · ngân sách",
                "tong_ket": "Một câu tóm tắt hồ sơ.", "ly_do_hr": "Lý do HR nên xem hồ sơ này."}
  }]
}
```

- Mọi tiêu chí trong `criteria.json` phải có mặt trong `diem`. `muc` ∈ {0,1,2,3}; `muc` > 0 bắt buộc có `trich_dan` kèm `vi_tri`. Mức 0: `trang_thai` là `Không tìm thấy` (CV không nêu) hoặc `Không đáp ứng` (CV nêu rõ trái yêu cầu, ví dụ chuyên ngành khác; vẫn nên kèm trích dẫn). Mức 1: `Đáp ứng một phần`; mức 2–3: `Đáp ứng`.
- `trich_dan[].text` phải là **nguyên văn** (nối các dòng xuống dòng thành một câu, giữ lỗi chính tả của CV).
- `vi_tri`: `trang N, tên mục` (PDF/DOCX) hoặc `ảnh k/n, tên mục` (ảnh).
- `thoi_gian_lam_viec`: `bat_dau`/`ket_thuc` dạng `YYYY-MM` (hoặc `YYYY` khi CV chỉ ghi năm, kèm `do_chinh_xac: "nam"`); `ket_thuc: null` nghĩa là đến nay. `tinh_chat`: `chinh` (đúng vị trí cần tuyển), `tuong_duong`, `khac`. Script tự tính số tháng và nhãn ổn định công việc từ trường này.
- `xem_truoc`: ảnh xem trước từ `chuan_bi_cv.py` (nếu thiếu, script dùng `file_luu`).
- `tom_tat` (khuyến nghị): `tin_hieu` 2–4 chip ngắn (≤ 25 ký tự), `can_xac_minh` một dòng, `tong_ket` một câu, `ly_do_hr` một câu. Nếu thiếu, script tự suy ra từ `diem_manh`/`luu_y`.
- `ten` lấy từ nội dung CV (không dùng tên file nếu khác); giữ ánh xạ ở `anh_xa_cv.json`.
