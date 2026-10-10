#!/usr/bin/env python3
"""lhg-taobao 确定性店铺资产审计：18 条规则，零第三方依赖。

扫描目标目录的店铺运营资产（标题.txt / 主图.md / sku.md / 详情.md /
价格.md 等文本文件），检查标题合规、主图规范、SKU 完整性、详情页模块、
价格标注与平台红线；有 blocker 时以 exit code 2 退出（供 hooks 与 CI 使用）。

用法：
    python3 taobao_audit.py --target <目录> [--format json|text] [--fail-on blocker|warning|nit]

规则文案均为本项目原创（思路受 cedric123123/get-some-cash-ai-workbench 的
"商品事实-素材策略-合规审核"流水线、qwqess121/ecommerce-ai-skills
lyt-image-patterns 的主图标签与因果护栏、newxhy/ecom-hero-detail-image-pro
的"按买家决策顺序排详情屏"启发，未复制任何第三方原文）。

合规声明：平台规则变化快，本脚本提供方法论与检查清单层面的确定性检查，
不承诺实时数据、流量与排名效果。
"""

import argparse
import json
import os
import re
import sys

VERSION = "1.0.0"
TOOL = "lhg-taobao/taobao-audit"

SKIP_DIRS = {
    "node_modules", ".git", "__pycache__", "dist", "build", ".next",
    "fixtures", "coverage", "vendor",
}
SCAN_EXTS = {".md", ".txt", ".markdown"}


class Finding:
    __slots__ = ("rule_id", "severity", "category", "title", "file", "line", "snippet", "detail")

    def __init__(self, rule_id, severity, category, title, file, line, snippet, detail):
        self.rule_id = rule_id
        self.severity = severity
        self.category = category
        self.title = title
        self.file = file
        self.line = line
        self.snippet = snippet
        self.detail = detail

    def to_dict(self):
        return {
            "rule_id": self.rule_id, "severity": self.severity,
            "category": self.category, "title": self.title,
            "file": self.file, "line": self.line,
            "snippet": self.snippet, "detail": self.detail,
        }


def collect_files(target):
    out = []
    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            _, ext = os.path.splitext(f)
            if ext.lower() in SCAN_EXTS:
                out.append(os.path.join(root, f))
    return sorted(out)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


RULES = []
_RULE_BY_ID = {}


def rule(rule_id, severity, category, title, detail):
    def deco(fn):
        r = {"id": rule_id, "severity": severity,
             "category": category, "title": title, "detail": detail}
        _RULE_BY_ID[rule_id] = r
        r["check"] = fn
        RULES.append(r)
        return fn
    return deco


def _mk(rule_id, path, line, snippet):
    r = _RULE_BY_ID[rule_id]
    return Finding(r["id"], r["severity"], r["category"], r["title"],
                   path, line, snippet[:160], r["detail"])


def _any_hit(text, words):
    return any(w in text for w in words)


def _is_title_file(path):
    return "标题" in os.path.basename(path)


def _is_image_file(path):
    b = os.path.basename(path)
    return "主图" in b or "图片" in b


def _is_sku_file(path):
    return "sku" in os.path.basename(path).lower()


def _is_detail_file(path):
    return "详情" in os.path.basename(path)


def _cjk_len(text):
    return len(re.findall(r"[\u4e00-\u9fff]", text))


# ---------------- 标题 ----------------

@rule("TB-TITLE-001", "blocker", "标题", "标题含违禁词",
      "标题含违禁词（假一赔十/原单/高仿/专柜验货等）。这类词一上架就可能被下架扣分，整句删掉重写。")
def r_title_001(files, texts, path, ctx):
    words = ["假一赔十", "假一罚万", "原单", "高仿", "A货", "专柜验货",
             "支持验货", "海关罚没", "尾单"]
    out = []
    for p, t in texts.items():
        if not _is_title_file(p):
            continue
        for i, ln in enumerate(t.split("\n")):
            if _any_hit(ln, words):
                out.append(_mk("TB-TITLE-001", p, i + 1, ln.strip()))
    return out


@rule("TB-TITLE-002", "blocker", "标题", "标题含极限词",
      "标题含极限词（最畅销/第一名/首家/顶级等）。广告法明文禁止，先下掉，换成可验证的具体卖点。")
def r_title_002(files, texts, path, ctx):
    words = ["最畅销", "第一名", "首家", "顶级", "国家级", "全球第一",
             "销量第一", "全网第一", "最火爆"]
    out = []
    for p, t in texts.items():
        if not _is_title_file(p):
            continue
        for i, ln in enumerate(t.split("\n")):
            if _any_hit(ln, words):
                out.append(_mk("TB-TITLE-002", p, i + 1, ln.strip()))
    return out


@rule("TB-TITLE-003", "warning", "标题", "标题超长",
      "标题超过 30 个汉字。淘宝标题上限 30 字，超了会被截断，核心词尽量往前放。")
def r_title_003(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_title_file(p):
            continue
        body = t.strip()
        if _cjk_len(body) > 30:
            out.append(_mk("TB-TITLE-003", p, 1,
                           "共 %d 个汉字（上限 30）" % _cjk_len(body)))
    return out


@rule("TB-TITLE-004", "warning", "标题", "标题空格过多",
      "标题空格超过 10 个。空格不占搜索权重还浪费字数，删掉多余空格，把位置留给关键词。")
def r_title_004(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_title_file(p):
            continue
        n = t.count(" ") + t.count("　")
        if n > 10:
            out.append(_mk("TB-TITLE-004", p, 1, "共 %d 个空格" % n))
    return out


@rule("TB-CONV-WARN", "warning", "标题", "标题特殊符号堆砌",
      "标题特殊符号（【】★⚡等）超过 4 个。有标题党嫌疑，影响点击与平台印象，精简到 2 个以内。")
def r_conv_warn(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_title_file(p):
            continue
        n = len(re.findall(r"[【】★⚡™®※✦✧♦♠♥♣]", t))
        if n > 4:
            out.append(_mk("TB-CONV-WARN", p, 1, "共 %d 个特殊符号" % n))
    return out


@rule("TB-TITLE-005", "nit", "标题", "标题过短信息量不足",
      "标题不足 10 个字。标题是免费搜索流量的入口，太短等于浪费一半关键词位，按品类词加属性词加卖点词补齐。")
def r_title_005(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_title_file(p):
            continue
        if t.strip() and _cjk_len(t) < 10:
            out.append(_mk("TB-TITLE-005", p, 1, t.strip()[:60]))
    return out


# ---------------- 主图 ----------------

@rule("TB-IMG-001", "warning", "主图", "缺少主图尺寸规范",
      "主图规划里没写尺寸规范。淘宝主图标准 800×800，尺寸不对会变形、被降权，先定规范。")
def r_img_001(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_image_file(p):
            continue
        if not _any_hit(t, ["800×800", "800x800", "800*800", "尺寸规范"]):
            out.append(_mk("TB-IMG-001", p, 1, os.path.basename(p)))
    return out


@rule("TB-IMG-002", "warning", "主图", "缺少主图张数规划",
      "主图规划没写张数。建议 5 张：白底首图、场景、卖点、细节、套装或服务，每张承载一个购买理由。")
def r_img_002(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_image_file(p):
            continue
        if not _any_hit(t, ["5张", "五张", "主图规划", "第一张", "首图"]):
            out.append(_mk("TB-IMG-002", p, 1, os.path.basename(p)))
    return out


@rule("TB-IMG-003", "nit", "主图", "缺少白底图说明",
      "主图规划没提白底图。首图建议白底（搜索页展示更干净），记得写进规范。")
def r_img_003(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_image_file(p):
            continue
        if not _any_hit(t, ["白底"]):
            out.append(_mk("TB-IMG-003", p, 1, os.path.basename(p)))
    return out


# ---------------- SKU ----------------

@rule("TB-SKU-001", "blocker", "SKU", "SKU 缺少关键属性",
      "SKU 规划里没有颜色/尺码/规格/款式等关键属性。属性缺失会导致买家选错、退货率飙升，上架前必须补齐。")
def r_sku_001(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_sku_file(p):
            continue
        if not _any_hit(t, ["颜色", "尺码", "规格", "款式", "尺寸"]):
            out.append(_mk("TB-SKU-001", p, 1, os.path.basename(p)))
    return out


@rule("TB-SKU-002", "warning", "SKU", "SKU 缺少价格/利润标注",
      "SKU 规划没有成本/利润/价格带标注。不算账就定价，活动一打折就亏。每个 SKU 标注：成本价、售价、毛利。")
def r_sku_002(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_sku_file(p):
            continue
        if not _any_hit(t, ["成本", "利润", "毛利", "价格带"]):
            out.append(_mk("TB-SKU-002", p, 1, os.path.basename(p)))
    return out


# ---------------- 详情页 ----------------

@rule("TB-DETAIL-001", "warning", "详情页", "详情页缺少必备模块",
      "详情页必备模块（参数表/实拍图/尺码表/售后说明）缺 2 个以上。买家决策靠详情页补信息，缺模块等于把订单往外推。")
def r_detail_001(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_detail_file(p):
            continue
        hit = sum(1 for w in ["参数", "实拍", "尺码表", "售后"] if w in t)
        if hit < 2:
            out.append(_mk("TB-DETAIL-001", p, 1,
                           "仅命中 %d/4 个必备模块" % hit))
    return out


@rule("TB-DETAIL-002", "blocker", "详情页", "详情页含承诺性用语",
      "详情页含承诺性用语（假一赔十/百分百正品）。写上去容易，举证难，纠纷时全是你的责任，删掉。")
def r_detail_002(files, texts, path, ctx):
    words = ["假一赔十", "假一罚万", "百分百正品", "100%正品"]
    out = []
    for p, t in texts.items():
        if not _is_detail_file(p):
            continue
        for i, ln in enumerate(t.split("\n")):
            if _any_hit(ln, words):
                out.append(_mk("TB-DETAIL-002", p, i + 1, ln.strip()))
    return out


@rule("TB-DETAIL-003", "nit", "详情页", "缺少售后说明",
      "详情页没写售后说明（退换/运费险）。售后写清楚，转化率更高、纠纷更少。")
def r_detail_003(files, texts, path, ctx):
    out = []
    for p, t in texts.items():
        if not _is_detail_file(p):
            continue
        if not _any_hit(t, ["售后", "退换", "运费险"]):
            out.append(_mk("TB-DETAIL-003", p, 1, os.path.basename(p)))
    return out


# ---------------- 价格与合规 ----------------

@rule("TB-PRICE-001", "warning", "价格", "缺少价格带标注",
      "资产包里没做价格带标注（成本价/利润/定价策略）。不先算账，活动报名、直通车一开就亏。")
def r_price_001(files, texts, path, ctx):
    if _any_hit(ctx["corpus"], ["成本价", "利润", "定价策略", "毛利率"]):
        return []
    return [_mk("TB-PRICE-001", path, 1, os.path.basename(path))]


@rule("TB-COMP-001", "blocker", "合规", "含刷单/好评返现表述",
      "发现刷单/补单/好评返现表述。这是平台明令打击项，一抓一个准，相关文案全部删掉。")
def r_comp_001(files, texts, path, ctx):
    words = ["刷单", "补单", "好评返现", "返现好评"]
    out = []
    for p, t in texts.items():
        for i, ln in enumerate(t.split("\n")):
            if _any_hit(ln, words):
                out.append(_mk("TB-COMP-001", p, i + 1, ln.strip()))
    return out


@rule("TB-COMP-002", "warning", "合规", "含站外引流表述",
      "发现加微信/站外交易等表述。平台禁止站外引流，抓到扣分降权，交易务必留在站内。")
def r_comp_002(files, texts, path, ctx):
    words = ["加微信", "微信号", "站外交易", "私下交易"]
    out = []
    for p, t in texts.items():
        for i, ln in enumerate(t.split("\n")):
            if _any_hit(ln, words):
                out.append(_mk("TB-COMP-002", p, i + 1, ln.strip()))
    return out


# ---------------- 格式 ----------------

@rule("TB-FMT-001", "nit", "格式", "文档缺少一级标题",
      "这个 Markdown 文件没有一级标题。资产包里的文档都该有个标题，方便检索和归档。")
def r_fmt_001(files, texts, path, ctx):
    t = texts[path]
    if not path.endswith(".md"):
        return []
    if re.search(r"^# .+", t, re.M):
        return []
    return [_mk("TB-FMT-001", path, 1, os.path.basename(path))]


SEV_ORDER = {"blocker": 0, "warning": 1, "nit": 2}


def audit(target):
    files = collect_files(target)
    texts = {p: read_text(p) for p in files}
    corpus = "\n".join(texts.values())
    ctx = {"corpus": corpus}
    findings = []
    anchor = files[0] if files else target
    for r in RULES:
        for p in files:
            try:
                for f in r["check"](files, texts, p, ctx) or []:
                    findings.append(f)
            except Exception:
                continue
    seen, uniq = set(), []
    for f in findings:
        key = (f.rule_id, f.file, f.line)
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    corpus_rules = {"TB-PRICE-001"}
    final = [f for f in uniq
             if f.rule_id not in corpus_rules or f.file == anchor]
    final.sort(key=lambda f: (SEV_ORDER[f.severity], f.file, f.line))
    return final


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", required=True)
    ap.add_argument("--format", choices=["json", "text"], default="text")
    ap.add_argument("--fail-on", choices=["blocker", "warning", "nit"], default="blocker")
    args = ap.parse_args()

    findings = audit(args.target)
    summary = {"tool": TOOL, "version": VERSION, "target": args.target,
               "rules_run": len(RULES),
               "blocker": sum(1 for f in findings if f.severity == "blocker"),
               "warning": sum(1 for f in findings if f.severity == "warning"),
               "nit": sum(1 for f in findings if f.severity == "nit")}

    if args.format == "json":
        print(json.dumps({"summary": summary,
                          "findings": [f.to_dict() for f in findings]},
                         ensure_ascii=False, indent=2))
    else:
        print("== %s v%s ==" % (TOOL, VERSION))
        print("目标：%s｜规则 %d 条｜blocker %d / warning %d / nit %d" % (
            args.target, summary["rules_run"], summary["blocker"],
            summary["warning"], summary["nit"]))
        for f in findings:
            print("[%s][%s] %s:%d %s" % (
                f.severity, f.rule_id, f.file, f.line, f.title))
            print("    %s" % f.detail)

    levels = ["blocker", "warning", "nit"]
    threshold = levels.index(args.fail_on)
    bad = any(levels.index(f.severity) <= threshold for f in findings)
    return 2 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
