#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成 100 个 2FA 矩阵号规划表（原表只读，输出到新文件）。"""

import json
import os
import sys

import pandas as pd

FILE_A = "/Users/a600/Downloads/比特0627导出窗口.xlsx"
FILE_B = "/Users/a600/Downloads/x号/x号_merged_marked.xlsx"
OUT_FILE = "/Users/a600/Downloads/x号/x_100_2fa_matrix_ready(已整理100个2FA矩阵号_不改原表).xlsx"

GROUPS = [
    "Group_A_Proxy(住宅代理)",
    "Group_B_Scrape(反爬API)",
    "Group_C_GPU(算力云)",
    "Group_D_Pay(出海收单)",
]
COOKIE_OK = "已有完整Cookie可直接免登"
COOKIE_NEED = "需用账号+密码+2FA自动登录"


def norm(v):
    """统一成去空白字符串，缺失值返回空串。"""
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return ""
    s = str(v).strip()
    return "" if s.lower() in ("nan", "none", "nat") else s


def cookie_is_complete(value):
    """Cookie 是否为可解析的 JSON 数组。"""
    text = norm(value)
    if not text.startswith("["):
        return False
    try:
        return isinstance(json.loads(text), list)
    except (ValueError, TypeError):
        return False


def read_sheet(path, preferred=None):
    book = pd.ExcelFile(path, engine="openpyxl")
    sheet = preferred if preferred in book.sheet_names else book.sheet_names[0]
    return pd.read_excel(book, sheet_name=sheet, dtype=str, engine="openpyxl")


def pick_col(df, *names):
    for name in names:
        if name in df.columns:
            return name
    raise KeyError("缺少列: " + " / ".join(names))


def main():
    for path in (FILE_A, FILE_B):
        if not os.path.isfile(path):
            sys.exit("找不到输入文件: " + path)

    # ---------- 读取文件 A（只读） ----------
    a_raw = read_sheet(FILE_A, "导出窗口")
    user_a = pick_col(a_raw, "用户名", "Username")
    twofa_a = pick_col(a_raw, "2FA秘钥", "2FA Secret")

    a = a_raw.copy()
    a["_user"] = a[user_a].map(norm)
    a["_2fa"] = a[twofa_a].map(norm)
    # 过滤说明行/空行：用户名与 2FA 秘钥必须都非空
    a = a[(a["_user"] != "") & (a["_2fa"] != "")].reset_index(drop=True)
    if a.empty:
        sys.exit("文件 A 中没有同时具备用户名和 2FA 秘钥的账号")
    if len(a) != 100:
        print("提示: 文件 A 中带 2FA 的有效账号为 %d 个（非 100）" % len(a))

    # ---------- 读取文件 B（只读） ----------
    b_raw = read_sheet(FILE_B)
    user_b = pick_col(b_raw, "Username", "Username.1", "用户名")
    f2a_b = pick_col(b_raw, "f2a密钥", "2FA Secret", "2FA秘钥")

    b = b_raw.copy()
    b["_user"] = b[user_b].map(norm)
    b = b[b["_user"] != ""].copy()

    # 同一用户名重复出现时保留第一条，避免左连接后行数膨胀
    b_unique = b.drop_duplicates(subset="_user", keep="first").copy()

    email_col = pick_col(b_raw, "Email Address")
    email_pwd_col = pick_col(b_raw, "Email Password")
    backup_col = pick_col(b_raw, "f2a备用")
    status_col = pick_col(b_raw, "Status")

    b_slim = b_unique[["_user", email_col, email_pwd_col, backup_col, status_col]].rename(
        columns={
            email_col: "Email Address",
            email_pwd_col: "Email Password",
            backup_col: "f2a备用",
            status_col: "Status",
        }
    )

    # ---------- 左连接 ----------
    main_df = a.merge(b_slim, on="_user", how="left")

    # ---------- Cookie 状态 ----------
    main_df["Cookie状态"] = [
        COOKIE_OK if cookie_is_complete(v) else COOKIE_NEED for v in main_df["Cookie"]
    ]

    # ---------- 赛道 / 层级 / Profile 目录 ----------
    total = len(main_df)
    groups = [GROUPS[(i // 25) % len(GROUPS)] for i in range(total)]
    profiles = ["profile_%03d_%s" % (i + 1, main_df.at[i, "_user"]) for i in range(total)]

    # 每个 25 号赛道内：完整 Cookie 优先排序，前 2 个 Tier1、随后 6 个 Tier2、其余 17 个 Tier3
    tiers = ["Tier3_冷备轮换号"] * total
    for start in range(0, total, 25):
        block = list(range(start, min(start + 25, total)))
        ranked = sorted(
            block, key=lambda j: (0 if cookie_is_complete(main_df.at[j, "Cookie"]) else 1, j)
        )
        for rank, j in enumerate(ranked):
            if rank < 2:
                tiers[j] = "Tier1_主理人号"
            elif rank < 8:
                tiers[j] = "Tier2_痛点狙击灰度号"

    main_df["CPS赛道分组"] = groups
    main_df["矩阵层级"] = tiers
    main_df["独立Profile目录名"] = profiles

    # 只保留原表列 + 新增列，去掉内部辅助列
    main_df = main_df.drop(columns=["_user", "_2fa"])

    # ---------- 文件 B 中额外的带 2FA 账号 ----------
    a_users = set(a["_user"])
    b_extra = b_unique[
        (~b_unique["_user"].isin(a_users)) & (b_unique[f2a_b].map(norm) != "")
    ].copy()
    extra_df = b_extra.drop(columns=["_user"]).reset_index(drop=True)

    # ---------- 写出（不覆盖任何输入文件） ----------
    out_dir = os.path.dirname(OUT_FILE)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    if os.path.abspath(OUT_FILE) in (os.path.abspath(FILE_A), os.path.abspath(FILE_B)):
        sys.exit("输出路径与输入文件相同，已中止")

    with pd.ExcelWriter(OUT_FILE, engine="openpyxl") as writer:
        main_df.to_excel(writer, sheet_name="主表_100个带2FA账号", index=False)
        extra_df.to_excel(writer, sheet_name="额外带2FA备选号", index=False)

    # ---------- 控制台摘要（不含任何密码/2FA/Cookie/代理明文） ----------
    print("=" * 56)
    print("输入 A 有效带2FA账号数: %d" % total)
    print("成功匹配文件B资料数  : %d" % int(main_df["Email Address"].notna().sum()))
    print("Cookie可直接免登     : %d" % int((main_df["Cookie状态"] == COOKIE_OK).sum()))
    print("需账密+2FA自动登录   : %d" % int((main_df["Cookie状态"] == COOKIE_NEED).sum()))
    for group in GROUPS:
        sub = main_df[main_df["CPS赛道分组"] == group]
        if sub.empty:
            continue
        t1 = int((sub["矩阵层级"] == "Tier1_主理人号").sum())
        t2 = int((sub["矩阵层级"] == "Tier2_痛点狙击灰度号").sum())
        t3 = int((sub["矩阵层级"] == "Tier3_冷备轮换号").sum())
        print("%-24s 共%2d 个 | Tier1 %d / Tier2 %d / Tier3 %d" % (group, len(sub), t1, t2, t3))
    print("额外带2FA备选号      : %d" % len(extra_df))
    print("输出文件             : %s" % OUT_FILE)
    print("=" * 56)


if __name__ == "__main__":
    main()
