#!/usr/bin/env python3
"""Chuẩn bị CV từ một thư mục: sao chép bản gốc, tạo ảnh xem trước, trích văn bản (nếu có).

Dùng:  python -X utf8 chuan_bi_cv.py <thu_muc_cv> <thu_muc_ket_qua> [--de-quy]

Tạo trong thư mục kết quả:
  assets/cv/<cvNN>-<ten-an-toan>.<duoi>   bản sao CV gốc (không sửa file nguồn)
  assets/preview/<cvNN>.jpg               ảnh xem trước (ảnh: nén; PDF: ghép tối đa 4 trang; DOCX: qua LibreOffice nếu có)
  .work/van-ban/<cvNN>.txt                văn bản trích từ PDF/DOCX có text (chỉ cho Agent 1, KHÔNG đưa cho Agent 2)
  anh_xa_cv.json                          bảng ánh xạ key, tên gốc, nguồn, file lưu, xem trước, loại
CV dạng ảnh/PDF scan: Agent 1 phải tự mở ảnh (assets/preview hoặc assets/cv) và đọc bằng thị giác.
"""
import json, os, re, shutil, subprocess, sys, unicodedata
from PIL import Image

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

EXT = {".pdf", ".docx", ".jpg", ".jpeg", ".png", ".webp"}
IMG = {".jpg", ".jpeg", ".png", ".webp"}


def slug(s):
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-") or "cv"


def preview_image(src, dst):
    im = Image.open(src).convert("RGB")
    if im.width > 1400:
        im = im.resize((1400, int(im.height * 1400 / im.width)), Image.LANCZOS)
    im.save(dst, "JPEG", quality=82, optimize=True)


def pdf_pages(src):
    try:
        import pymupdf as fitz
    except Exception:
        import fitz
    return fitz.open(src)


def preview_pdf(src, dst, max_pages=4):
    doc = pdf_pages(src)
    ims = []
    for i, page in enumerate(doc):
        if i >= max_pages:
            break
        pix = page.get_pixmap(dpi=110)
        ims.append(Image.frombytes("RGB", (pix.width, pix.height), pix.samples))
    if not ims:
        return False
    w = max(i.width for i in ims)
    canvas = Image.new("RGB", (w, sum(i.height for i in ims)), "white")
    y = 0
    for i in ims:
        canvas.paste(i, (0, y)); y += i.height
    canvas.save(dst, "JPEG", quality=82, optimize=True)
    return True


def text_pdf(src):
    doc = pdf_pages(src)
    return "\n".join(f"=== trang {i + 1} ===\n{p.get_text()}" for i, p in enumerate(doc))


def text_docx(src):
    import docx
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    d = docx.Document(src)
    out = []
    for el in d.element.body.iterchildren():
        if el.tag.endswith("}p"):
            t = Paragraph(el, d).text.strip()
            if t:
                out.append(t)
        elif el.tag.endswith("}tbl"):
            for r in Table(el, d).rows:
                out.append(" | ".join(c.text.replace("\n", " / ") for c in r.cells))
    return "\n".join(out)


def docx_to_pdf(src, outdir):
    for exe in ("soffice", "libreoffice"):
        if shutil.which(exe):
            try:
                subprocess.run([exe, "--headless", "--convert-to", "pdf", "--outdir", outdir, src], check=True, capture_output=True, timeout=120)
                p = os.path.join(outdir, os.path.splitext(os.path.basename(src))[0] + ".pdf")
                return p if os.path.exists(p) else None
            except Exception:
                return None
    return None


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    src_dir, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    deq = "--de-quy" in sys.argv
    files = []
    for root, _, fs in os.walk(src_dir):
        for f in sorted(fs):
            if os.path.splitext(f)[1].lower() in EXT and not f.startswith(("~$", ".")):
                files.append(os.path.join(root, f))
        if not deq:
            break
    files.sort(key=lambda p: os.path.basename(p).lower())
    cvd, pvd, txd = (os.path.join(out, "assets", "cv"), os.path.join(out, "assets", "preview"), os.path.join(out, ".work", "van-ban"))
    for d in (cvd, pvd, txd):
        os.makedirs(d, exist_ok=True)
    mp = []
    for n, p in enumerate(files, 1):
        base, ext = os.path.splitext(os.path.basename(p)); ext = ext.lower()
        key = f"cv{n:02d}"
        name = f"{key}-{slug(base)}{ext}"
        shutil.copy2(p, os.path.join(cvd, name))
        prev, text, note = None, None, ""
        try:
            if ext in IMG:
                preview_image(p, os.path.join(pvd, key + ".jpg")); prev = f"assets/preview/{key}.jpg"
            elif ext == ".pdf":
                text = text_pdf(p)
                if preview_pdf(p, os.path.join(pvd, key + ".jpg")):
                    prev = f"assets/preview/{key}.jpg"
                if len(text.replace("=== trang", "").strip()) < 80:
                    note = "PDF không có text (scan): phải đọc bằng thị giác"; text = None
            elif ext == ".docx":
                text = text_docx(p)
                pdf = docx_to_pdf(p, pvd)
                if pdf and preview_pdf(pdf, os.path.join(pvd, key + ".jpg")):
                    prev = f"assets/preview/{key}.jpg"
                    os.remove(pdf)
                else:
                    note = "Không tạo được ảnh xem trước DOCX (cần LibreOffice); báo cáo chỉ có nút mở file"
        except Exception as e:
            note = f"Lỗi xử lý: {e}"
        if text:
            open(os.path.join(txd, key + ".txt"), "w", encoding="utf8").write(text)
        mp.append({"key": key, "ten_goc": os.path.basename(p), "nguon": p, "file_luu": f"assets/cv/{name}", "xem_truoc": prev,
                   "loai": ext.strip("."), "co_van_ban": bool(text), "ghi_chu": note})
        print(key, os.path.basename(p), "->", name, "| xem trước:", prev or "KHÔNG", note)
    json.dump(mp, open(os.path.join(out, "anh_xa_cv.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
    from collections import Counter
    print("Tổng:", len(mp), dict(Counter(m["loai"] for m in mp)))


main()
