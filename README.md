<!-- About 简介（推送后填写到仓库 About 栏）：
店铺运营专家：选品→上架→标题/主图优化→数据复盘，方法论与检查清单一次配齐 ｜ 一键安装：/plugin marketplace add lhg-plugs/lhg-taobao
-->
<!-- topics（推送后打）：claude-code, claude-plugin, agent-skills, taobao, ecommerce, listing-seo -->

# lhg-taobao：小白一句话 → 淘宝店铺运营全流程

> **一句话介绍**：给 AI 助手装上"店铺运营专家"——选品、上架、标题/主图优化、数据复盘一条龙，产出可直接用的单品资产包，18 条确定性规则先审后上架。
>
> **一键安装**：在 Claude Code 里运行
> ```
> /plugin marketplace add lhg-plugs/lhg-taobao
> /plugin install lhg-taobao@lhg-plugs
> ```

> **合规声明（置顶）**：平台规则变化快，本插件提供**方法论与检查清单**，**不承诺实时数据、流量与排名效果**；不提供任何刷单、补单、好评返现等违规操作指导。遇到不确定的新规，请以官方最新规则为准。

## 它是什么

`lhg-taobao` 是一个 Claude Code 插件（plugin 为主、skill 为辅）：

- **4 个命令**（小白入口）：`taobao` 一句话跑通全流程，`listing` 单品打磨，`review` 数据复盘，`audit` 店铺体检
- **4 个平台中立 skill**（方法论，可移植到豆包/Workbuddy 等）：选品、单品优化、数据复盘、合规红线
- **2 个专家 agent**：单品优化、店铺审计
- **2 个硬门 hooks**：commit 前资产审计拦截、写入极限词/违禁词/刷单表述时警告（均可一键豁免）
- **18 条确定性自查规则**：纯 Python、零第三方依赖，秒出结果

## 4 个命令用法

| 命令 | 作用 | 示例 |
|---|---|---|
| `/lhg-taobao:taobao` | 一句话跑通：选品→上架→优化→复盘 | `/lhg-taobao:taobao "陶瓷马克杯"` |
| `/lhg-taobao:listing` | 单品打磨：标题/主图/SKU/详情页逐项落实 | `/lhg-taobao:listing "陶瓷马克杯"` |
| `/lhg-taobao:review` | 数据复盘：漏斗定位→归因→改进行动 | `/lhg-taobao:review 周 "马克杯"` |
| `/lhg-taobao:audit` | 店铺体检（脚本 + 人工评审清单） | `/lhg-taobao:audit ./taobao-pack` |

## 自查说明

自查 = 确定性脚本（机器）+ 人工评审清单（人）：

1. 先跑 `scripts/audit/taobao_audit.py`（18 条规则），零 LLM 成本；
2. 发现分三级：**blocker**（必须修：标题违禁词/极限词、SKU 缺关键属性、详情页承诺性用语、刷单表述）、**warning**（修或写豁免理由）、**nit**（顺手修）；
3. 再按 skill 的评审清单过一遍脚本抓不到的（标题顺不顺、主图购买理由清不清晰、图文一致吗）。

blocker 清零才算做完；为清零改规则算作弊，不许。

## 目录结构

```
lhg-taobao/
├── .claude-plugin/          # plugin.json（插件清单）+ marketplace.json（本仓即市场）
├── commands/                # 4 个命令：taobao / listing / review / audit
├── skills/                  # 4 个平台中立 skill（选品/单品优化/数据复盘/合规红线）
├── agents/                  # 2 个专家 agent（listing-optimizer / shop-auditor）
├── hooks/                   # 2 个硬门（commit 前审计拦截 / 极限词违禁词写入警告）+ 豁免说明
├── scripts/audit/           # 18 条确定性自查规则（零第三方依赖）
├── fixtures/                # 冒烟测试用例（坏/好对照）
├── smoke_test.py            # 一键冒烟测试
├── ATTRIBUTION.md           # 灵感来源与许可声明
└── LICENSE                  # MIT
```

## 什么时候用 / 什么时候不用（FAQ）

**什么时候用：**

- 你想开淘宝店，不知道卖什么、怎么上架时 → 用 `/lhg-taobao:taobao` 跑完全流程
- 标题不知道怎么写、主图不知道怎么排时 → 用 `/lhg-taobao:listing` 逐项打磨
- 流量掉了、转化掉了，想定位原因时 → 用 `/lhg-taobao:review`（记得准备好真实后台数据）
- 标题/详情页写完怕踩红线时 → 跑 `/lhg-taobao:audit`，极限词/违禁词/刷单表述会被拦下来

**什么时候不用：**

- 你要实时数据、流量预测、排名保证 → 插件只提供方法论与检查清单，不承诺实时数据、流量与排名效果
- 你想让 AI 帮你刷单、补单、写好评返现话术 → 不提供任何违规操作指导，这种需求请绕道
- 你的主战场是拼多多/抖音小店 → 规则按淘宝设计，方法论通用但合规清单需要自己对

## lhg-plugs 插件矩阵

| 插件 | 一句话 | 安装 |
|---|---|---|
| [lhg-fullstack](https://github.com/lhg-plugs/lhg-fullstack) | 小白一句话 → 高质量全栈应用 | `/plugin install lhg-fullstack@lhg-plugs` |
| [lhg-video-edit](https://github.com/lhg-plugs/lhg-video-edit) | 一句话把口播素材剪成爆款短视频（+口播脚本子命令） | `/plugin install lhg-video-edit@lhg-plugs` |
| [lhg-wechat-article](https://github.com/lhg-plugs/lhg-wechat-article) | 公众号写作专家：选题到排版一气呵成 | `/plugin install lhg-wechat-article@lhg-plugs` |
| [lhg-xiaohongshu](https://github.com/lhg-plugs/lhg-xiaohongshu) | 小红书种草专家：卖点到爆款笔记一键生成 | `/plugin install lhg-xiaohongshu@lhg-plugs` |
| [lhg-resume](https://github.com/lhg-plugs/lhg-resume) | 简历优化专家：ATS诊断到模拟面试一条龙 | `/plugin install lhg-resume@lhg-plugs` |
| [lhg-ppt](https://github.com/lhg-plugs/lhg-ppt) | PPT制作专家：述职融资答辩一键成稿 | `/plugin install lhg-ppt@lhg-plugs` |
| [lhg-excel](https://github.com/lhg-plugs/lhg-excel) | 表格数据专家：清洗透视图表一条龙 | `/plugin install lhg-excel@lhg-plugs` |
| [lhg-thesis](https://github.com/lhg-plugs/lhg-thesis) | 毕业论文助手：开题到盲审的写作流水线 | `/plugin install lhg-thesis@lhg-plugs` |
| [lhg-miniprogram](https://github.com/lhg-plugs/lhg-miniprogram) | 小程序开发专家：一句话生成微信小程序 | `/plugin install lhg-miniprogram@lhg-plugs` |
| [lhg-contract](https://github.com/lhg-plugs/lhg-contract) | 合同审查助手：风险条款标红+修改建议 | `/plugin install lhg-contract@lhg-plugs` |
| [lhg-geo](https://github.com/lhg-plugs/lhg-geo) | AI搜索优化专家：品牌AI可见性诊断与优化 | `/plugin install lhg-geo@lhg-plugs` |
| [lhg-poster](https://github.com/lhg-plugs/lhg-poster) | 海报设计专家：一句话→版式→Canvas精确绘制 | `/plugin install lhg-poster@lhg-plugs` |
| [lhg-shopify](https://github.com/lhg-plugs/lhg-shopify) | 独立站建站专家：建站流程标准化一键生成 | `/plugin install lhg-shopify@lhg-plugs` |
| [lhg-fiction](https://github.com/lhg-plugs/lhg-fiction) | 网文写作专家：题材→大纲→逐章→一致性检测 | `/plugin install lhg-fiction@lhg-plugs` |
| [lhg-drama-script](https://github.com/lhg-plugs/lhg-drama-script) | 短剧剧本专家：分集大纲→单集剧本→时长检测 | `/plugin install lhg-drama-script@lhg-plugs` |
| [lhg-lit-review](https://github.com/lhg-plugs/lhg-lit-review) | 文献综述专家：文献→框架→写作→引用校验 | `/plugin install lhg-lit-review@lhg-plugs` |
| [lhg-salary-talk](https://github.com/lhg-plugs/lhg-salary-talk) | 薪酬谈判专家：策略→话术演练→底线清单 | `/plugin install lhg-salary-talk@lhg-plugs` |
| [lhg-biz-report](https://github.com/lhg-plugs/lhg-biz-report) | 商业分析专家：数据→洞察→图文报告/PPT | `/plugin install lhg-biz-report@lhg-plugs` |
| [lhg-study-abroad](https://github.com/lhg-plugs/lhg-study-abroad) | 留学文书专家：PS/推荐信结构化写作 | `/plugin install lhg-study-abroad@lhg-plugs` |
| [lhg-meal-plan](https://github.com/lhg-plugs/lhg-meal-plan) | 营养食谱专家：营养素测算→一周食谱→采购清单 | `/plugin install lhg-meal-plan@lhg-plugs` |
| [lhg-headline](https://github.com/lhg-plugs/lhg-headline) | 爆款标题专家：多平台标题公式生成+合规检测 | `/plugin install lhg-headline@lhg-plugs` |
| [lhg-logo](https://github.com/lhg-plugs/lhg-logo) | Logo设计专家：品牌概念→几何规范→多尺寸导出 | `/plugin install lhg-logo@lhg-plugs` |
| [lhg-ecom-design](https://github.com/lhg-plugs/lhg-ecom-design) | 电商视觉专家：卖点到高点击主图一键策划 | `/plugin install lhg-ecom-design@lhg-plugs` |
| [lhg-ecom-report](https://github.com/lhg-plugs/lhg-ecom-report) | 电商复盘专家：店铺数据到周/月复盘报告 | `/plugin install lhg-ecom-report@lhg-plugs` |
| [lhg-lesson-plan](https://github.com/lhg-plugs/lhg-lesson-plan) | 课程设计专家：课标对齐→教案课件→覆盖校验 | `/plugin install lhg-lesson-plan@lhg-plugs` |
| [lhg-dashboard](https://github.com/lhg-plugs/lhg-dashboard) | 数据看板专家：指标体系→看板布局→图表规范校验 | `/plugin install lhg-dashboard@lhg-plugs` |
| [lhg-competitor](https://github.com/lhg-plugs/lhg-competitor) | 竞品分析专家：维度框架→对比矩阵→差异化建议 | `/plugin install lhg-competitor@lhg-plugs` |
| [lhg-social-ops](https://github.com/lhg-plugs/lhg-social-ops) | 社媒运营专家：账号定位→内容日历→数据复盘 | `/plugin install lhg-social-ops@lhg-plugs` |
| [lhg-book-translate](https://github.com/lhg-plugs/lhg-book-translate) | 书籍翻译专家：术语锁定→章节翻译→一致性审计 | `/plugin install lhg-book-translate@lhg-plugs` |
| [lhg-infographic](https://github.com/lhg-plugs/lhg-infographic) | 信息图表专家：数据→图表选型→Canvas绘制→可读性审计 | `/plugin install lhg-infographic@lhg-plugs` |
| [lhg-live-script](https://github.com/lhg-plugs/lhg-live-script) | 直播话术专家：留人/转粉/逼单话术→开播脚本 | `/plugin install lhg-live-script@lhg-plugs` |
| [lhg-course-create](https://github.com/lhg-plugs/lhg-course-create) | 课程制作专家：大纲→讲义→习题→试听课脚本 | `/plugin install lhg-course-create@lhg-plugs` |
| [lhg-exam-maker](https://github.com/lhg-plugs/lhg-exam-maker) | 出题组卷专家：知识点→蓝图→组卷→覆盖率校验 | `/plugin install lhg-exam-maker@lhg-plugs` |
| [lhg-weekly-review](https://github.com/lhg-plugs/lhg-weekly-review) | 周报复盘专家：记录→结构化周报→亮点→风险预警 | `/plugin install lhg-weekly-review@lhg-plugs` |
| [lhg-money-plan](https://github.com/lhg-plugs/lhg-money-plan) | 理财规划助手：收支→预算→储蓄目标（非投资建议） | `/plugin install lhg-money-plan@lhg-plugs` |
| [lhg-finmodel](https://github.com/lhg-plugs/lhg-finmodel) | 财务建模专家：假设→三表搭建→勾稽校验→敏感性分析 | `/plugin install lhg-finmodel@lhg-plugs` |
| [lhg-mini-game](https://github.com/lhg-plugs/lhg-mini-game) | H5游戏专家：一句话生成可玩H5小游戏 | `/plugin install lhg-mini-game@lhg-plugs` |
| [lhg-browser-ext](https://github.com/lhg-plugs/lhg-browser-ext) | 浏览器插件专家：一句话想法生成MV3插件 | `/plugin install lhg-browser-ext@lhg-plugs` |
| [lhg-bp](https://github.com/lhg-plugs/lhg-bp) | 商业计划书专家：九章BP→投资人自检→路演版 | `/plugin install lhg-bp@lhg-plugs` |
| [lhg-survey](https://github.com/lhg-plugs/lhg-survey) | 问卷分析专家：清洗→统计→图表→结论报告 | `/plugin install lhg-survey@lhg-plugs` |
| [lhg-community](https://github.com/lhg-plugs/lhg-community) | 社群运营专家：定位→入群SOP→内容日历→转化话术→流失召回 | `/plugin install lhg-community@lhg-plugs` |
| [lhg-taobao](https://github.com/lhg-plugs/lhg-taobao) | 店铺运营专家：选品→上架→标题/主图优化→数据复盘 | `/plugin install lhg-taobao@lhg-plugs` |

## 出品：刘洪光

本插件由真人出镜 IP「刘洪光」（安徽合肥）出品，归属 [lhg-skills](https://github.com/lhg-skills)。

- GitHub 主页：https://github.com/lhg-skills —— 全部 skill 开源在此，欢迎 star
- 抖音：搜「刘老师讲AI实战」
- 微信：lhgsmsw
