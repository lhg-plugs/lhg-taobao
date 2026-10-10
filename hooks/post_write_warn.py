#!/usr/bin/env python3
"""lhg-taobao 硬门②（警告级，不拦截）：写入标题/详情文案命中极限词、违禁词时提醒。

触发：PostToolUse / Write|Edit。检测写入的 .md/.txt 是否含极限词、
违禁词、刷单类表述；命中只做提醒，永远 exit 0、不拦截写入。

逃生方式：LHG_TB_HOOKS_OFF=1（环境变量）可关闭本提醒；
或 /plugin disable lhg-taobao 停用整个插件。
零第三方依赖。
"""

import json
import os
import re
import sys

RISKY_RES = [
    re.compile(r"最畅销|第一名|首家|顶级|国家级|全球第一|销量第一|全网第一|最火爆"),
    re.compile(r"假一赔十|假一罚万|原单|高仿|A货|专柜验货|支持验货|海关罚没|尾单"),
    re.compile(r"刷单|补单|好评返现|返现好评"),
]
RISKY_LABEL = {
    0: "极限词（最畅销/第一名/首家/顶级等）",
    1: "违禁词（假一赔十/原单/高仿等）",
    2: "刷单/好评返现类（平台明令打击）",
}
TEXT_EXTS = {".md", ".txt", ".markdown"}


def main() -> int:
    if os.environ.get("LHG_TB_HOOKS_OFF") == "1":
        return 0

    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        return 0

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "") or ""
    if not file_path:
        return 0
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in TEXT_EXTS:
        return 0
    if not os.path.isfile(file_path):
        return 0

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return 0

    hits = [RISKY_LABEL[i] for i, rx in enumerate(RISKY_RES) if rx.search(text)]
    if not hits:
        return 0

    msg = (
        "合规提醒（lhg-taobao）：%s 命中高风险表述：%s。\n"
        "极限词违反广告法、违禁词/刷单表述会被平台下架扣分，建议删掉或换成可验证的具体卖点；"
        "确认无误可忽略本提醒。\n"
        "跑 /lhg-taobao:audit 可做全量检查；关闭本提醒：export LHG_TB_HOOKS_OFF=1。"
    ) % (file_path, "、".join(hits))
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }
    sys.stdout.write(json.dumps(out, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
