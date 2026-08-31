---
name: oss-learning-maintainer
description: 维护 oss-learning 开源学习仓库：AI 驱动的技术选型雷达、自动引入新框架、企业级平台蓝图、文档/wiki/官方页、自动提 issue、每日/每周自更新。当你需要"更新仓库""跑技术雷达""引入新框架""完善文档""提 issue""推送""维护这个仓库"时使用。
---

# oss-learning 仓库维护 Skill

> 把"AI 自动技术选型 + 自我学习 + 企业级平台落地 + 流量变现"这套自维护机制固化成一个可复用流程。
> 本 skill 沉淀了所有历史需求，供 AI 每晚/每周据此自动完善仓库。

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
│   ├── watch-trending.py    # 技术雷达：多维度扫 GitHub 新框架 → docs/tech-watch/<date>.md
│   ├── add-submodules.sh    # 按 manifest 批量 add 子模块
│   └── build-manifest.sh    # 重建 manifest（含排除规则）
├── docs/
│   ├── enterprise-microservice-blueprint.md   # 微服务落地蓝图
│   ├── enterprise-ai-platform-blueprint.md    # 企业 AI 平台蓝图
│   ├── tech-watch/<date>.md                   # 雷达候选报告（多维度）
│   ├── intel/<date>.md                        # AI 情报站：每日快讯（AI 撰写，遵守编辑方针）
│   ├── intel/index.md                        # 情报站枢纽页（快讯索引 + 专题 + 编辑方针 + 流量策略）
│   └── diagrams/*.drawio                      # 分层架构图（draw.io 可编辑）
├── .claude/skills/       # 本 skill（沉淀的维护方法论）
└── .github/ISSUE_TEMPLATE/tech-candidate.md   # AI/用户提"新技术候选"issue 的模板
```

## 3. 维护循环（每晚 / 每周执行一次）

整个循环是一个闭环，**每次运行都输出可感知的增量**：

```
雷达扫描 → AI 审阅候选 → 引入仓库 → 沉淀文档 → 情报站快讯 → 提 issue → 提交推送 → 更新官方页/wiki
```

### Step 1 · 技术雷达扫描（多维度）

```bash
cd oss-learning && python scripts/watch-trending.py --days 180
# 产物：docs/tech-watch/YYYY-MM-DD.md（三维度候选表）
# 可选 GITHUB_TOKEN 提升限额（未登录 ~7s/次，全程约 3 分钟）
```

雷达是**多维度**的（2026-08-31 起，堵"只搜 topic"盲区）：

- **维度① 主题标签 topic**：按分类查 `topic:X created:>N`。
- **维度② 关键词**：`X created:>N` 查名称/描述，兜住**没打标签**的仓库。
- **维度③ 跨主题飙升榜**：`created:>N stars:>2000` 按 ⭐ 排序、**不限 topic**——专门抓不按常理打标签的黑马（教训：`andrewyng/openworker` ⭐17k 但 `topics:[]`，单靠 topic 搜索会漏）。

报告每行带「标签」列，`-` = 无 topic 的黑马（重点看）。

### Step 2 · AI 审阅候选（关键决策步）

对每个候选，评估是否值得引入：

- **新技术 / 飙升 / 赋能业务 / 引流**：值得（如新 Agent 框架、MCP、短视频、文生图）。
- **查重**：对照 `scripts/manifest.tsv` 的 origin 与已注册路径，避免重复（Sentinel/sofa-boot/seata/nacos 等已在册）。
- **经典不删**：老项目保留，只增加新时代项目。

### Step 3 · 引入仓库

```bash
# 1) 追加一行到 manifest.tsv：
#    super<tab>category<tab>name<tab>origin  （origin 用 https://github.com/... 或 git@gitee.com:...）
# 2) 批量添加（跳过已注册 gitlink，3 次重试）：
bash scripts/add-submodules.sh <super>   # super ∈ {ai, java}
# 3) 校验：
git -C <super> submodule status | grep '^-'   # 应无未初始化
```

> **网络约定（必须遵守）**：Clash 127.0.0.1:7897；不得改全局 `url.git@github.com:.insteadof`；
> gitee 必须走 SSH；每次 git 命令带 `-c core.longpaths=true`；批处理用 `GIT_CONFIG_COUNT=5` 环境块。

### Step 4 · 沉淀文档（把仓库"讲好"）

- **README**（根 / ai / java）：更新子模块数、分类、亮点、雷达与蓝图入口、GitHub Pages 地址。
- **蓝图**：新框架进对应分层（微服务 10 层 / AI 8 层），补映射表、路线图、场景表。
- **drawio 架构图**：docs/diagrams/ 下按分层加 swimlane + 组件框。
- **wiki / 官方页**：GitHub Pages 站引用蓝图与雷达；wiki 放"如何自维护"说明。

### Step 4.5 · AI 情报站每日快讯（写作方向把关）

雷达跑完后，AI 撰写当日快讯 `docs/intel/YYYY-MM-DD.md` 并更新 `docs/intel/index.md` 索引。**写作方向必须把关**，遵守固定编辑方针：

1. **有选型价值**：读者看完能回答"我该不该用"。禁止纯罗列/凑数/填日期。
2. **快讯格式固定**：① 头条（1–2 条真正有增量：新模型/新框架/重大发布）→ ② 飙升项目盘点（带 ⭐、为什么涨、适合谁）→ ③ 本期接入清单（manifest 新增）→ ④ 变现提示（结尾：企业落地 / 接单 / 流量）。
3. **信息可验证**：⭐、license、owner、日期必须真实（来自 GitHub API/页面），不写"感觉值"。
4. **观点有依据**：说"值得关注"必须给理由（场景/生态/赚钱链路）；不标题党、不夸大数字。
5. **结尾挂三条变现链路**：赋能企业 / 接单交付 / 流量内容。

**流量策略**（情报站是流量盘子，别只当技术笔记）：

| 受众 | 内容 | 渠道 |
|---|---|---|
| 找 AI/开源新框架的开发者 | 技术雷达 · 每日快讯 | GitHub、掘金、知乎 |
| 企业架构师 / 技术决策者 | 微服务蓝图 · AI 平台蓝图 | 搜索引擎长尾、公众号 |
| 想做副业/接单的人 | 接单项目盘点 · 变现路径 | 掘金、知乎、公众号 |
| 备战面试的人 | 技术面试小册（二期项目） | 掘金、GitHub、公众号 |

运营节奏：每日快讯 → 每周《开源精选》汇总 → 每月《AI 开源月报》。Pages 当**内容仓库**，公众号/掘金当**分发渠道**。

### Step 5 · 自动提 issue

用 `.github/ISSUE_TEMPLATE/tech-candidate.md` 模板，把候选/计划整理成 issue：
`[技术雷达] 建议引入 <仓库>` 或 `[维护] <本周自更新摘要>`。AI 可自动开，也可整理后提示用户确认。

### Step 6 · 提交推送

```bash
git -C java add -A && git -C java commit -m "chore: <日期> 自更新摘要" && git -C java push
git -C ai  add -A && git -C ai  commit -m "chore: <日期> 自更新摘要" && git -C ai  push
git -C oss-learning add -A && git -C oss-learning commit -m "chore: <日期> 文档/雷达/skill 更新" && git -C oss-learning push
```

### Step 7 · 官方页 / wiki / 流量

- 维护 GitHub Pages 站（README 索引 + 蓝图 + 雷达 + 架构图预览）。
- 每次有亮点增量（新框架、新蓝图、新应用），在官方页和 README 顶部同步"本周新增"，利于被搜索与传播。

## 4. 需求 → 行动对照表（历史需求沉淀）

| 历史需求 | 落地产物 |
|---|---|
| 去 GitHub 看新框架、自我学习、自动技术选型 | `watch-trending.py` 雷达（多维度）+ 每轮引入 |
| "从各个维度去找各种项目"（雷达曾漏掉无 topic 的 openworker） | 雷达升级为三维度：topic + 关键词 + 跨主题飙升榜（不限 topic），报告带「标签」列标注黑马 |
| 弄个 AI 情报站、GitHub Pages 里加栏目 | `docs/intel/`（枢纽页 + 每日快讯），Pages 首页挂「情报站」入口 |
| 自己想想打造哪些流量、写作方向把关 | 情报站「编辑方针 + 流量策略」（见 index.md 与 Step 4.5） |
| AI 自动提 issue | `.github/ISSUE_TEMPLATE/tech-candidate.md` + Step 5 |
| 企业级落地、赋能企业/业务、提效 | 两份蓝图 + 两张 drawio 架构图 |
| 经典不删、只引入新时代 | 只追加 manifest 行，不删除旧模块 |
| 短视频、文生图、PCB/行业 AI、流量变现 | `ai/Applications` 类目（MoneyPrinterTurbo、ComfyUI、Fooocus、KiCAD-MCP 等） |
| java 引入"接单"实战项目（微信小程序商城等） | `java/Examples` 类目补 `newbee-mall`、`mall4j`、`yudao-mall`、`mall4cloud`、`jeecg-boot`、`RuoYi-Vue-Plus` 等"能接单赚钱"的全栈/后台/低代码项目（查重：litemall、mall-swarm、eladmin、yudao-cloud 已在册） |
| 分析云平台生态（它们多是开源项目） | `docs/cloud-ecosystem.md` 分析阿里/腾讯/华为/AWS/微软/CNCF 开源生态，并补录 etcd、KubeEdge、openGauss、openGemini、Tars、ModelScope 等到集合；云厂商新开源中间件 = 下一批"新时代项目"（每轮雷达含云生态扫描） |
| 赋能物理世界各行各业 | `ai/Applications`（PCB/EDA、硬件制造）+ 行业 AI 场景表（见 AI 蓝图）；持续扫描行业垂直开源项目 |
| 官方页面 + GitHub Pages + wiki | 官方站（Pages）+ docs 区 + 蓝图 |
| 维护过程沉淀为 skill | 本文件（含全流程） |
| README 好好维护 | Step 4（每次增量同步 README/官方页） |
| 每晚 / 每周自动完善 | 定时任务（cron）调用本 skill 的维护循环 |

## 5. 定时任务约定

- **每周一次**（推荐起点）：周日晚执行完整维护循环。
- **每晚**：可选跑雷达 + 快速 README/官方页增量。
- 每次运行结束，把"本次做了什么"写进 commit message 与官方页"更新日志"，形成公开可见的活跃度。

## 6. 注意事项 / 避坑

- **网络**：Clash 127.0.0.1:7897；改 URL 只在本脚本/会话内用 `GIT_CONFIG_COUNT=5` 环境块，**禁止改全局 insteadOf**。
- **Windows**：控制台别打印 emoji（GBK 报错）；深路径删除用 `cmd //c rmdir //s //q "\\\\?\\..."`。
- **GitHub API**：OR 链 + 日期限定易 422/403，雷达按"每个查询单查"最稳；未登录限 10 次/分。
- **雷达盲区**：`topic:` 搜索只命中**打了标签**的仓库——openworker（17k⭐、`topics:[]`）就是因此漏掉的。所以雷达必须多维度（topic + 关键词 + 跨主题飙升），且报告要标注"无标签黑马"。
- **子模块**：改名注意 gitlink 与 .gitmodules 同步；吸收/移动用 `git submodule absorbgitdirs`。
- **GitHub Pages 与子模块**：Pages「Deploy from a branch」会**递归 checkout 子模块**——gitee SSH 子模块直接构建失败（Host key verification failed）；全 GitHub 子模块太多（79/224 个）也会超时/失败。**所以 ai/java 仓库的 Pages 必须用 GitHub Actions 工作流（`.github/workflows/pages.yml`，`submodules: false`），站点只构建根目录静态内容**。三个站点：oss-learning（分支构建 · docs/）、oss-learning-ai / oss-learning-java（Actions 工作流）。
- **gitee 子模块迁移**：`scripts/gitee-to-github.py` 按 `java/gitee-mapping.tsv` 解析 gitee 子模块到 GitHub 镜像（`git ls-remote` 验证存在才接受）；无镜像标 DELETED。2026-08-31 已完成：90 个换 GitHub、11 个废弃（java 235→224 子模块）。注意 ls-remote 可能瞬断误判，DELETED 前对可疑项多试候选 owner（didi→didi、elunez→elunez、ityouknow→ityouknow、J2Cache→oschina）。
- **不要**为了"显得活跃"乱引入低质项目；保持"赋能/引流/学习"三价值取向。

## 7. 快速开始（一次完整循环）

```bash
cd /d/MyWorkSpace/oss-learning
python scripts/watch-trending.py --days 180        # 1 多维度雷达
# 2 审阅 docs/tech-watch/<today>.md  → 挑选候选（「标签」列为 - 的是无 topic 黑马，重点看）
# 3 追加 manifest.tsv → bash scripts/add-submodules.sh ai  (或 java)
# 4 更新 README / 蓝图 / 官方页
# 4.5 写情报站快讯 docs/intel/<today>.md + 更新 docs/intel/index.md 索引（遵守编辑方针）
# 5 按模板提 issue
# 6 commit + push 三个仓库
# 7 汇报本周增量
```
