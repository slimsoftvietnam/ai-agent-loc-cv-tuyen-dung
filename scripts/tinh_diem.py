#!/usr/bin/env python3
"""Tính điểm bằng chứng K+S, độ bao phủ, xếp hạng và nhãn ổn định công việc.

Dùng:  python -X utf8 tinh_diem.py <thu_muc_ket_qua>
Đọc criteria.json + scores.json trong thư mục kết quả, ghi ket_qua_tinh_diem.json
và chép chính script này vào thư mục kết quả để HR kiểm tra lại.
Thoát mã 1 nếu có lỗi dữ liệu (thiếu trích dẫn khi mức > 0, tổng trọng số != 100...).
"""
import json, os, shutil, sys
from datetime import date

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

D = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
crit = json.load(open(os.path.join(D, "criteria.json"), encoding="utf8"))
sc = json.load(open(os.path.join(D, "scores.json"), encoding="utf8"))
errors, warns = [], []
tc = crit["tieu_chi"]
W = {t["id"]: t["trong_so"] for t in tc}
G = {t["id"]: t["nhom"] for t in tc}
REQ = [t["id"] for t in tc if t["muc_do"] == "Bắt buộc"]
TIME_RULE = {t["id"]: t["kiem_tra_thoi_gian"] for t in tc if t.get("kiem_tra_thoi_gian")}
if abs(sum(W.values()) - 100) > 1e-6:
    errors.append("Tổng trọng số != 100")
today = date.fromisoformat(sc["ngay"])
th = crit.get("thai_do", {}).get("nguong_on_dinh", {})
N_SHORT = th.get("so_vi_tri_duoi_6_thang", 2)
YEARS = th.get("trong_so_nam_gan_nhat", 3)


def ym(s):
    p = s.split("-")
    return int(p[0]), (int(p[1]) if len(p) > 1 else 1)


def months(p):
    a = ym(p["bat_dau"])
    b = ym(p["ket_thuc"]) if p["ket_thuc"] else (today.year, today.month)
    m = (b[0] - a[0]) * 12 + (b[1] - a[1])
    if p.get("do_chinh_xac", "thang") == "thang":
        m += 1
    return m


def level_by_months(m, rule):
    for lv in ("3", "2", "1"):
        if m >= rule["nguong_thang"][lv]:
            return int(lv)
    return 0


def time_expected(c, rule):
    chinh = sum(months(p) for p in c["thoi_gian_lam_viec"] if p["tinh_chat"] in ("chinh", "digital"))
    td = sum(months(p) for p in c["thoi_gian_lam_viec"] if p["tinh_chat"] in ("chinh", "digital", "tuong_duong"))
    lv = level_by_months(chinh, rule)
    if td > chinh:
        lv = max(lv, min(rule.get("tuong_duong_toi_da", 2), level_by_months(td, rule)))
    return lv, chinh, td


res = []
for c in sc["ung_vien"]:
    ten, d = c["ten"], c["diem"]
    for t in tc:
        i = t["id"]
        if i not in d:
            errors.append(f"{ten}: thiếu {i}")
            continue
        x = d[i]
        if x["muc"] not in (0, 1, 2, 3):
            errors.append(f"{ten} {i}: mức sai")
        if x["muc"] > 0 and not x["trich_dan"]:
            errors.append(f"{ten} {i}: mức>0 thiếu trích dẫn")
        for q in x["trich_dan"]:
            if not q["text"].strip() or not q["vi_tri"].strip():
                errors.append(f"{ten} {i}: trích dẫn thiếu vị trí")
    t_info = {}
    for i, rule in TIME_RULE.items():
        if i in d:
            exp, chinh, td = time_expected(c, rule)
            t_info[i] = {"so_thang_chinh": chinh, "so_thang_tuong_duong": td, "muc_theo_quy_tac": exp}
            if exp != d[i]["muc"]:
                warns.append(f"{ten}: {i} chấm {d[i]['muc']} nhưng quy tắc tháng cho {exp} (chính {chinh} tháng, tương đương {td} tháng)")

    def grp(g):
        ids = [i for i in W if G[i] == g]
        tot = sum(W[i] for i in ids)
        return round(sum(W[i] * d[i]["muc"] / 3 for i in ids) / tot * 100, 1) if tot else 0.0

    diem = sum(W[i] * d[i]["muc"] / 3 for i in W)
    cover = sum(1 for i in W if d[i]["muc"] > 0)
    thieu = [i for i in REQ if d[i]["muc"] == 0]
    ngan = []
    for p in c["thoi_gian_lam_viec"]:
        if p.get("do_chinh_xac", "thang") != "thang":
            continue
        m = months(p)
        b = ym(p["ket_thuc"]) if p["ket_thuc"] else (today.year, today.month)
        if m < 6 and (today.year - b[0]) * 12 + (today.month - b[1]) <= YEARS * 12:
            ngan.append((p["vai_tro"], m))
    nhan = (len(ngan) >= N_SHORT) or any(m < 3 for _, m in ngan)
    ov = {"nhan": nhan, "so_vi_tri": len(c["thoi_gian_lam_viec"]), "vi_tri_ngan": ngan,
          "chi_tiet": [{"vai_tro": p["vai_tro"], "don_vi": p["don_vi"], "so_thang": months(p), "chinh_xac": p.get("do_chinh_xac", "thang")} for p in c["thoi_gian_lam_viec"]]}
    res.append({"key": c["key"], "ten": ten, "diem_tong": round(diem, 1), "diem_K": grp("K"), "diem_S": grp("S"),
                "do_bao_phu": round(cover / len(W) * 100, 1), "so_tieu_chi_co_bang_chung": cover,
                "tieu_chi_bat_buoc_thieu": thieu, "on_dinh": ov, "kiem_tra_thoi_gian": t_info})

res.sort(key=lambda r: -r["diem_tong"])
for r in res:
    r["hang"] = 1 + sum(1 for o in res if o["diem_tong"] > r["diem_tong"])
    r["muc_phu_hop"] = next(m["nhan"] for m in crit["muc_phu_hop"] if r["diem_tong"] >= m["tu"])
json.dump({"loi": errors, "canh_bao": warns, "ket_qua": res}, open(os.path.join(D, "ket_qua_tinh_diem.json"), "w", encoding="utf8"), ensure_ascii=False, indent=1)
me = os.path.abspath(__file__)
if os.path.dirname(me) != D:
    shutil.copy2(me, os.path.join(D, "tinh_diem.py"))
print("LỖI:", errors)
print("CẢNH BÁO:", warns)
for r in res:
    print(r["hang"], r["ten"], r["diem_tong"], "K", r["diem_K"], "S", r["diem_S"], "bao phủ", r["do_bao_phu"], "thiếu bắt buộc", r["tieu_chi_bat_buoc_thieu"], "nhãn ổn định", r["on_dinh"]["nhan"])
sys.exit(1 if errors else 0)
