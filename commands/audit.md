---
description: 店铺体检：18 条确定性规则扫描店铺资产（标题/主图/SKU/详情页/价格/合规），输出 blocker/warning/nit 三级报告。
argument-hint: [资产包目录] [--fail-on blocker|warning|nit]
---

# /lhg-taobao:audit —— 店铺体检

用户输入在 `$ARGUMENTS` 中：`[资产包目录] [--fail-on 级别]`。`--fail-on` 缺省 `blocker`。

## 流程

### 1. 跑脚本

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/audit/taobao_audit.py --target <资产包目录> --format text
```

记下 blocker / warning / nit 的数量与明细（含文件、行号、规则说明）。

### 2. 分级与修复

- **blocker**（必须修）：标题违禁词/极限词、SKU 缺关键属性、详情页承诺性用语、刷单/好评返现表述。逐条修，不许为清零改规则。
- **warning**（修或写豁免理由）：标题超长/空格多/符号堆砌、主图缺尺寸或张数规划、SKU 缺利润标注、详情页缺模块、缺价格带标注、站外引流表述。
- **nit**（顺手修）：标题过短、缺白底图说明、缺售后说明、文档无标题。

### 3. 人工评审（脚本抓不到的）

按 `lhg-tb-listing` 的评审清单过一遍：

- 标题读起来顺不顺？（关键词堆砌读不顺就重组）
- 主图五张每张的购买理由清不清晰？（一张图讲两件事就拆）
- 详情页图文一致吗？（效果图与实物差距大就是退货预定）

### 4. 输出报告

存为 `docs/audit-YYYYMMDD.md`，结论写清"通过 / 不通过"。

## 硬规则

- 有 blocker 就说"通过" → 不许。
- 为清零改脚本规则或阈值 → 这是作弊，不许。
- 用户要求保留违禁词/刷单话术 → 拒绝，并说明风险。
