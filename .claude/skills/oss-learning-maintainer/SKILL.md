---
name: oss-learning-maintainer
description: 编排 oss-learning 自维护循环：愿景、仓库结构、每周/每晚维护流程、分技能调度、定时任务约定。当你需要"更新仓库""跑完整维护""自更新""维护这个仓库"时使用。各步骤由分技能执行：oss-radar（雷达）、oss-introduce（引入）、oss-intel（情报站）、oss-release（发布）。
---

# oss-learning 仓库维护 Skill（编排）

> 把"AI 自动技术选型 + 自我学习 + 企业级平台落地 + 流量变现"这套自维护机制固化成一个**可编排流程**。
> 本技能是编排入口，具体步骤由 4 个分技能执行（各分技能是可单独调用的工作流）：

| 分技能 | 承接步骤 | 何时用 |
|---|---|---|
| `oss-radar` | Step 1–2 技术雷达 + 审阅候选 | "跑雷达找新框架" |
| `oss-introduce` | Step 3–4 引入仓库 + 更新计数 | "引入这个仓库" |
| `oss-intel` | Step 4.5 情报站每日快讯 | "写今日快讯" |
| `oss-release` | Step 5–7 提 issue + 提交推送 + 官方页 | "发布维护结果" |

## 1. 愿景与目标（来自需求沉淀）

**总目标**（2026-08-31 用户定调）：技术 → **赋能企业 / 赋能个人接单 / 赋能物理世界各行各业** → 最终**赚钱**。

本仓库不是普通的"开源代码收藏"，而是一个**AI 自行规划技术选型、自我学习、自动维护、对外输出影响力**的自驱动项目：

1. **技术选型雷达**：AI 定期扫 GitHub，感知新框架/飙升项目，自动评估是否引入。
2. **自我学习**：引入后沉淀为文档（蓝图、架构图、README、wiki、GitHub Pages）。
3. **企业级落地**：把技术组合成"赋能企业、赋能业务、提效"的平台方案（微服务 + 企业 AI 平台）。
4. **流量与变现**：引入短视频生成、文生图、行业 AI（如 PCB）等"贴合生活、能带来收益"的应用。
5. **自动提 issue**：AI 可将候选/更新以 issue 形式提出，形成公开记录与讨论。
6. **经典不删**：老技术保留用于学习，只做"引入新时代"，不做大删除。
7. **赚钱是终点**（2026-08-31 用户点题）：技术赋能企业 → 最终是为了赚钱。选型/引入时优先考虑"能变现"的链路：
   - **赋能企业** → 提效/省成本 → 企业愿意付费（企业 AI 平台、微服务蓝图）；
   - **接单/交付** → 微信小程序商城、后台管理、低代码等"接单能赚钱"的实战项目（java/Examples）；
   - **流量/内容** → 短视频、文生图、AI 应用（ai/Applications）培养流量与收益。

## 2. 仓库结构速览

```
oss-learning/
├── ai/                  # 企业级 AI 平台技术栈（子模块集合）
├── java/                # 企业级微服务技术栈（子模块集合）
├── scripts/
│   ├── manifest.tsv     # 唯一事实源：super<TAB>category<TAB>name<TAB>origin
│   ├── watch-trending.py    # 技术雷达（oss-radar 用）
│   ├── add-submodules.sh    # 按 manifest 批量 add 子模块（oss-introduce 用）
│   └── build-manifest.sh    # 重建 manifest（含排除规则）
├── docs/
│   ├── enterprise-microservice-blueprint.md   # 微服务落地蓝图
│   ├── enterprise-ai-platform-blueprint.md    # 企业 AI 平台蓝图
│   ├── tech-watch/<date>.md                   # 雷达候选报告（oss-radar 产物）
│   ├── intel/<date>.md                        # AI 情报站每日快讯（oss-intel 产物）
│   ├── intel/index.md                         # 情报站枢纽页（索引+编辑方针+流量策略）
│   └── diagrams/*.drawio                      # 分层架构图
├── .claude/skills/
│   ├── oss-learning-maintainer/SKILL.md   # 本编排技能
│   ├── oss-radar/SKILL.md                 # 雷达+审阅
│   ├── oss-introduce/SKILL.md             # 引入仓库
│   ├── oss-intel/SKILL.md                 # 情报站
│   └── oss-release/SKILL.md               # 提issue+推送+官方页
└── .github/ISSUE_TEMPLATE/tech-candidate.md   # 新技术候选 issue 模板
```

## 3. 维护循环（每晚 / 每周执行一次）

整个循环是闭环，**每次运行都输出可感知的增量**：

```
雷达扫描 → AI 审阅候选 → 引入仓库 → 沉淀文档 → 情报站快讯 → 提 issue → 提交推送 → 更新官方页/wiki
```

| Step | 内容 | 由谁执行 |
|---|---|---|
| Step 1–2 | 多维度雷达扫描 + AI 审阅候选 | **oss-radar** |
| Step 3–4 | 引入仓库（manifest+子模块+计数） | **oss-introduce** |
| Step 4.5 | 情报站每日快讯（编辑方针+流量策略） | **oss-intel** |
| Step 5–7 | 提 issue + 提交推送 + 官方页/wiki | **oss-release** |

**执行方式**：逐 step 调用对应分技能（`Skill` 工具），不要在编排技能里重复实现细节。

## 4. 需求 → 行动对照表（历史需求沉淀）

| 历史需求 | 落地产物 |
|---|---|
| 去 GitHub 看新框架、自我学习、自动技术选型 | `watch-trending.py` 雷达（多维度）+ 每轮引入 |
| "从各个维度去找各种项目"（雷达曾漏掉无 topic 的 openworker） | 雷达升级为三维度：topic + 关键词 + 跨主题飙升榜，报告带「标签」列标注黑马（见 oss-radar） |
| 弄个 AI 情报站、GitHub Pages 里加栏目 | `docs/intel/`（枢纽页 + 每日快讯），Pages 首页挂「情报站」入口（见 oss-intel） |
| 自己想想打造哪些流量、写作方向把关 | 情报站「编辑方针 + 流量策略」（见 oss-intel） |
| AI 自动提 issue | `.github/ISSUE_TEMPLATE/tech-candidate.md`（见 oss-release） |
| 企业级落地、赋能企业/业务、提效 | 两份蓝图 + 两张 drawio 架构图 |
| 经典不删、只引入新时代 | 只追加 manifest 行，不删除旧模块 |
| 短视频、文生图、PCB/行业 AI、流量变现 | `ai/Applications` 类目（MoneyPrinterTurbo、ComfyUI、Fooocus、KiCAD-MCP 等） |
| java 引入"接单"实战项目 | `java/Examples` 类目补 newbee-mall、mall4j、jeecg-boot、RuoYi-Vue-Plus 等"能接单赚钱"项目 |
| 分析云平台生态 | `docs/cloud-ecosystem.md` 分析阿里/腾讯/华为/AWS/微软/CNCF 开源生态 |
| 赋能物理世界各行各业 | `ai/Applications`（PCB/EDA、硬件制造）+ 行业 AI 场景表 |
| 官方页面 + GitHub Pages + wiki | 三个 Pages 站（总站 + AI 站 + 微服务站），2026-08-31 全部 200 |
| 维护过程沉淀为 skill | 本编排技能 + 4 个分技能 |
| 每晚 / 每周自动完善 | 定时任务（cron）调用本技能编排维护循环 |

## 5. 定时任务约定

- **每晚 22:47**（夜间轻量）：跑多维度雷达 → 快速 README/官方页增量。
- **每周日 20:03**（周度完整）：完整循环——雷达 → 审阅 → 引入 → 情报站 → 提 issue → 推送。
- 每次运行结束，把"本次做了什么"写进 commit message 与官方页"更新日志"，形成公开可见的活跃度。

## 6. 快速开始（一次完整循环）

```bash
cd /d/MyWorkSpace/oss-learning
# 1 调用 oss-radar：python scripts/watch-trending.py --days 180 → 审阅 docs/tech-watch/<today>.md
# 2 调用 oss-introduce：追加 manifest.tsv → bash scripts/add-submodules.sh ai|java → 更新计数
# 3 调用 oss-intel：写 docs/intel/<today>.md 快讯 + 更新 docs/intel/index.md
# 4 调用 oss-release：提 issue → 三仓库 commit+push（带 GIT_CONFIG_COUNT 网络块）→ 更新官方页
# 5 汇报本周增量
```

> 各分技能内含完整细节与避坑，编排时按 Step 逐个调用即可。
