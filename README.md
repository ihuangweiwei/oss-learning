# oss-learning

> **AI 驱动的开源学习 + 技术选型 + 企业级平台落地** 自维护仓库
>
> 用 git submodule 同步 **~315 个**高质量开源项目；AI 每晚/每周自动扫描 GitHub 新框架、
> 审阅引入、沉淀蓝图与文档、自动提 issue —— 把"学开源"变成"AI 自行规划技术栈"。

---

## 核心能力

| 能力 | 说明 | 入口 |
|---|---|---|
| 🤖 **技术雷达** | 自动扫 GitHub 新框架/飙升项目（AI/Agent、Skills/MCP、Java 微服务、短视频、RAG） | `scripts/watch-trending.py` → `docs/tech-watch/` |
| 🧩 **开源合集** | ~315 个开源项目，按 ai / java 两套 super-project 组织，跟随上游 latest | `ai/` · `java/` |
| 🏭 **企业微服务蓝图** | 10 层企业微服务架构 + 落地路线图 + 技术选型速查 | `docs/enterprise-microservice-blueprint.md` + drawio |
| 🚀 **企业 AI 平台蓝图** | 8 层 AI 平台（AI 网关→模型→RAG→Agent→MCP→技能→平台工程→变现） | `docs/enterprise-ai-platform-blueprint.md` + drawio |
| 📦 **技能资产** | 把"维护方法论 + 全部需求"沉淀为可复用 skill | `.claude/skills/oss-learning-maintainer/SKILL.md` |
| 📝 **自动提 issue** | 候选新框架用模板提 issue，形成公开讨论 | `.github/ISSUE_TEMPLATE/tech-candidate.md` |
| ⏰ **自更新** | 每晚轻量雷达 + 每周完整维护循环（定时任务） | 见"自动维护" |

## 目录结构

```
oss-learning/
├── ai/      # 企业级 AI 平台技术栈（~78 个子模块：Agent/Framework/RAG/Skills/Models/Applications…）
├── java/    # 企业级微服务技术栈（~235 个子模块：Spring/Distributed/Middleware/BigData/Examples/Go…）
├── scripts/
│   ├── manifest.tsv        # 唯一事实源：super/category/name/origin
│   ├── watch-trending.py   # 技术雷达：扫 GitHub 新框架 → 候选报告
│   ├── add-submodules.sh   # 按 manifest 批量添加子模块
│   └── build-manifest.sh   # 重建 manifest（含排除规则）
├── docs/
│   ├── enterprise-*-blueprint.md     # 企业级落地蓝图（微服务 + AI 平台）
│   ├── tech-watch/<date>.md          # 雷达候选报告（每日更新）
│   └── diagrams/*.drawio             # 分层架构图（draw.io 可编辑）
├── .claude/skills/oss-learning-maintainer/   # 自维护 skill
└── .github/ISSUE_TEMPLATE/                    # 技术候选 issue 模板
```

## 快速开始

```bash
# 拉取源码（含全部子模块）
git clone --recursive <your>/oss-learning-ai.git ai
git clone --recursive <your>/oss-learning-java.git java
# 更新到上游最新（有变更自动提交）
./sync-all.sh

# 跑一次技术雷达（扫描近 180 天 GitHub 新框架）
python scripts/watch-trending.py --days 180
# → 审阅 docs/tech-watch/YYYY-MM-DD.md，挑选候选引入
```

## 自动维护（AI 自驱动）

整套机制固化在 skill 里，每晚/每周自动执行：

```
雷达扫描 → AI 审阅候选 → 引入仓库 → 沉淀文档/蓝图 → 提 issue → 提交推送
```

- **每晚 22:47**：轻量雷达 + 更新官方页/README 更新日志 + 推送。
- **每周日 20:03**：完整循环——雷达、审阅、查重、引入、更新蓝图/README/架构图、提 issue、推送。
- **人工介入点**：AI 挑选候选后，会对照 `scripts/manifest.tsv` 查重并给出引入建议；经典项目保留不删，只引入新时代。

如何参与/复刻：读 `.claude/skills/oss-learning-maintainer/SKILL.md`，按"快速开始"跑一次完整循环即可。

## 网络说明（本机 Clash 代理场景）

- 子模块 URL 记录为上游原始 SSH 地址；**GitHub** 经 https+代理（`http.proxy=127.0.0.1:7897`），**Gitee** 走 SSH 直连。
- 脚本通过 `GIT_CONFIG_COUNT/KEY/VALUE` 注入反向规则（GitHub `ssh→https`、Gitee `https→ssh`），并带 `core.longpaths=true`（绕开 Windows 260 字符路径限制）。
- **注意**：不修改全局 `url.git@github.com:.insteadof` 规则，只在脚本/会话内生效。

## 脚本

| 脚本 | 作用 |
|------|------|
| `scripts/watch-trending.py` | 技术雷达：扫描近 N 天 GitHub 新框架/飙升项目，生成候选报告 |
| `scripts/scan.sh` | 扫描本机学习目录生成 `raw-manifest.tsv` |
| `scripts/build-manifest.sh` | 去重 + 排除 + 分类，生成 `manifest.tsv` |
| `scripts/add-submodules.sh <ai\|java>` | 按清单批量 `git submodule add`（重试/超时/锁） |

## Windows 路径不兼容排除

含 `:` `?` `|` 尾随空格等 Windows 非法字符、无法 checkout 的仓库已排除（`segmentfault-lessons`、`llm-action`、`technology-talk` 等）；用户私有/已删除仓库（`stock-admin-*`、`ai-agent-research`）不在清单。详见 `scripts/build-manifest.sh` 排除列表。
