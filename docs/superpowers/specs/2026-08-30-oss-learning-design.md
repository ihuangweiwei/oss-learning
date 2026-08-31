# oss-learning 开源学习代码同步项目 — 设计文档

日期：2026-08-30
状态：已确认（待用户最终审阅）

## 目标

把分散在以下位置的 GitHub/Gitee 开源学习代码，整理到一个统一管理的项目结构中，以 git submodule 方式注册、统一同步，用于日常学习：

- `D:\MyWorkSpace\learn` — 233 个仓库，已有 28 个分类文件夹
- `D:\MyWorkSpace\WorkSpace` — 32 个仓库，其中约 23 个 AI/Agent 开源学习项目
- `D:\MyWorkSpace\spring-ai\ai-agent-research` — 用户自有的 AI 研究合集（内含 30+ 子模块）

## 核心决策（已与用户确认）

1. 新建独立父文件夹 `D:\MyWorkSpace\oss-learning`，本身**不是** git 仓库，只放说明文档。
2. 内部两个**独立** git 超级项目：
   - `ai/` — AI/Agent 学习
   - `java/` — 传统技术学习（Java/中间件为主）
   各有自己的 `.gitmodules`，可分别 clone / push / 同步。
3. WorkSpace 只纳入 AI/Agent 学习类项目；用户个人项目不纳入。
4. `ai-agent-research`（用户自有 AI 合集）作为嵌套子模块挂入 `ai/Research/`，用 `git submodule update --init --recursive` 递归拉取。
5. 子模块更新策略：**跟踪上游最新**（`git submodule update --remote`），效果等同现有 `pull.sh`。
6. 两个超级项目推送到用户自己的 GitHub/Gitee（如 `ihuangweiwei/oss-learning-ai`、`ihuangweiwei/oss-learning-java`），子模块 URL 沿用现有 SSH 地址。

## 目录结构

```
D:\MyWorkSpace\oss-learning\
├─ ai\                              ← git 仓库①：AI/Agent 学习
│   ├─ .gitmodules
│   ├─ Agent\
│   ├─ Framework\
│   ├─ RAG\
│   ├─ Tutorial\
│   ├─ Platform\
│   └─ Research\                    ← ai-agent-research（嵌套超级项目）
├─ java\                            ← git 仓库②：传统技术学习
│   ├─ .gitmodules
│   └─ Base\ Distributed\ Middleware\ Spring\ BigData\ Task\
│      Transaction\ Util\ Netflix\ Alibaba\ Alipay\ Go\ Courses\
│      Framework\ Manager\ Examples\ chaos\ metric\ itstack\ …
└─ README.md                        ← 使用说明（如何同步、新机如何拉取）
```

## 分类规则

### ai/ 分类（新建）

| 分类 | 内容示例 |
|------|----------|
| `Agent` | opencode, crewAI, agentscope, agentscope-java, openagents, oh-my-openagent, deepagents, deer-flow, openclaw, HiClaw, CoPaw, RD-Agent, hermes-agent |
| `Framework` | langchain, langchain4j, langgraph, spring-ai-alibaba, spring-ai-alibaba-examples, SpringAI-Alibaba-Quickstart, SmartEngine |
| `RAG` | ragflow, dify, langflow, n8n, ai-hedge-fund |
| `Tutorial` | llm-action, llm-cookbook, dive-into-llms, AI-Interview, awesome-mcp-servers |
| `Platform` | temporal, camunda, higress |
| `Research` | ai-agent-research（用户自有嵌套超级项目） |

### java/ 分类（沿用 learn 现有 28 分类 + 少量合并）

- **保留原分类**：Base, Distributed, Middleware, Spring, Framework, BigData, Task, Transaction, Util, Netflix, Alibaba, Alipay, Go, Vertx, Nepxion, chaos, metric, itstack, Manager, Examples, Knowledge, Good
- **合并**：
  - `Bobo` + `Geektime` + `Gupao` → `Courses`（课程类）
  - `Xxl` → `Task`
- **跨分类调整**：
  - `learn/AI/nacos` → `java/Middleware`
  - `learn/Alibaba/Sentinel` → `java/Distributed`
  - `learn/Alibaba/spring-ai-alibaba` → `ai/Framework`
- 大部分仓库留在原分类，改动最小；映射以"现有分类文件夹"为准，实现时逐仓库核对。

## 迁移与去重

- **move 而非 copy**：把仓库 move 进 `oss-learning/<ai|java>/<分类>/`，然后 `git submodule add <origin> <path>` 原地注册。因已有 clone 且 origin 一致，git 会原地注册、不重新下载。
- **去重**：同一 origin 出现在多处（如 dify、opencode、langchain4j、spring-ai-alibaba 在 learn/AI、WorkSpace、spring-ai 均有）→ 只注册一份（优先完整/最新的副本），其余副本不搬动。
- **排除清单**（不纳入）：
  - 用户个人项目：eastmoney-fc, stock-dashboard, stock-skills, wencai-crawler, wx-stock-pro, shangchu(niuba), stock-admin, light-food-health, dingding-talk
  - `sinolink-ai-recruit`：无 remote，无法作为子模块，留在 WorkSpace 并标注
  - `marvis-office`（无 .git）：不纳入
  - `spring-ai` 下与 WorkSpace/learn 重复的 agentscope-java、deer-flow、spring-ai-alibaba：靠去重处理
  - `alibaba/lumenx`：可纳入 `ai/`（待用户最终确认）
- **安全**：每份代码的 origin URL 都记录进 `.gitmodules`，即使搬错也可按 URL 重新 clone，move 操作安全。按分类分批迁移、每批验证 `git submodule status`。

## 同步工作流

- 为 `ai/`、`java/` 各提供 `sync.sh`：
  1. `git submodule update --remote`（把每个子模块拉到上游默认分支最新）
  2. `git add -A && git commit`（记录新的子模块指针）
  3. `git push`（推送到远端）
- 新机拉取：
  ```
  git clone <ai远端> oss-learning-ai && cd oss-learning-ai
  git submodule update --init --recursive
  ```
  （java/ 同理）

## 远端与善后

- 在用户 GitHub/Gitee 账号下新建两个仓库：`oss-learning-ai`、`oss-learning-java`（最终名以用户确认为准），子模块 URL 沿用现有 SSH 地址不变。
- 旧 `learn/` 迁移后只剩脚本（down_project.sh、pull.sh、git.log 等）；脚本保留并移入 oss-learning 作为工具。
- 迁移验证完成后，旧空目录由用户自行清理。

## 风险与注意事项

- 批量迁移 250+ 仓库需分步执行、逐步验证，不要一次性全部 move。
- 部分仓库分支名不是 `master`（如 `main`），`git submodule update --remote` 依据远端默认分支，可正确处理。
- 嵌套超级项目（ai-agent-research）内的子模块不纳入本项目的 `.gitmodules`，保持其自身结构。

## 实施说明（最终状态与偏差，2026-08-31）

最终注册：**java 210 个子模块、ai 34 个子模块**，全部 `git submodule status` 正常，`manifest.tsv` 为唯一真源。

与设计的偏差：

1. **ai-agent-research 不纳入**。其 origin `ihuangweiwei/ai-agent-research` 在 github 为 404（私有或已删除），无法匿名 clone；用户确认不纳入，本地 `D:\MyWorkSpace\spring-ai\ai-agent-research` 原样保留。
2. **用户自己的仓库不纳入**：`stock-admin-backend`、`stock-admin-frontend`、`stock-analysis`（ihuangweiwei 私有项目），用户确认全部排除。
3. **Windows 路径不兼容排除**（文件名含 `:` `?` `|` 或尾随空格，git-for-windows 报 `invalid path`，`core.longpaths` 无效）：`segmentfault-lessons`、`geek-nodejs`、`Blog`、`technology-talk`、`Spring-Boot-Reference-Guide`、`llm-action`。
4. **`Spring-Cloud-Alibaba` 改用 github 官方源** `alibaba/spring-cloud-alibaba`（原 gitee 镜像 `mirrors/Spring-Cloud-Alibaba` 已删除，API 404）。
5. **origin 规范化**：manifest 中 6 个 gitee https origin（xxl 家族）统一改为 ssh（https 经代理会卡死）。
6. **深路径修复**：`core.longpaths` 用 `git -c core.longpaths=true` 传参（实测 env `GIT_CONFIG_COUNT` 注入对 clone checkout 无效），add 成功后也写入子模块本地 config 兜底。
7. **Gitee 兜底规则**：脚本 env 注入 `url.git@gitee.com:.insteadOf=https://gitee.com/`（https→ssh 直连）。

---

## 二期 · 新时代引入 + AI 自维护（2026-08-31）

用户明确"经典不删，引入新时代"，并要把仓库打造成 **AI 自维护的"火爆项目"**。二期落地：

### 计数与类目

- **ai**：34 → **65** → **78**（Applications 7 + Agent 精选 DeepSeek-Reasonix/openclaude/EnterpriseAgentFramework + Skills caveman/khazix-skills + modelscope）。
- **java**：210 → **225** → **235**（接单 6：newbee-mall/mall4j/mall4cloud/jeecg-boot/RuoYi-Vue-Plus；云生态 5：etcd/kubeedge/openGauss/openGemini/tars；yudao-mall 未单独开源已移除）。
- **ai 新增类目** `Applications/`：`short-video`（MoneyPrinterTurbo/OpenMontage/ai-fusion-video）、`text-to-image`（ComfyUI/Fooocus）、`pcb-eda`（Agent_PCB/kicad-mcp）——对应"短视频、文生图、PCB 行业 AI，最快见效"的需求。
- **ai 新增**：Agent（codex/openai-agents-python/browser-use/AutoGPT/autogen/agno/composio/cline/aider/metaGPT/MetaGPT/OpenHands/hermes-agent/DeepSeek-Reasonix/openclaude/EnterpriseAgentFramework）、Framework（semantic-kernel/llama_index/dspy/smolagents/litellm/vercel-ai）、Skills（anthropic-skills/superpowers/microsoft-skills/huggingface-skills/antfu-skills/awesome-claude-skills/awesome-agent-skills/awesome-claude-code/caveman/khazix-skills）、RAG（mem0/haystack/Flowise）、Models（DeepSeek-R1/DeepSeek-V3）。
- **java 新增**：quarkus/micronaut-core/armeria/helidon/spring-ai、shardingsphere/skywalking、shenyu、Sa-Token、caffeine、dynamic-datasource、dapr、grafana、yudao-cloud、mall-swarm 等。

### 企业级平台蓝图（新增）

- `docs/enterprise-microservice-blueprint.md` —— 10 层微服务架构（网关→框架→注册→治理→数据→中间件→可观测→安全→云原生→AI），4 阶段落地路线图 + 选型速查。
- `docs/enterprise-ai-platform-blueprint.md` —— 8 层 AI 平台（AI 网关→模型→RAG→Agent→工具/MCP→技能资产→平台工程→应用变现），赋能客服/研发/知识库/内容等业务场景。
- `docs/diagrams/microservice-architecture.drawio`、`docs/diagrams/ai-platform.drawio` —— draw.io 分层架构图。

### AI 自维护体系（新增）

- `scripts/watch-trending.py` —— GitHub 技术雷达：按 topic 单查（规避 OR 链 422/403），输出 `docs/tech-watch/<date>.md` 候选报告。
- `.claude/skills/oss-learning-maintainer/SKILL.md` —— 沉淀全部维护需求：雷达→审阅→引入→文档→issue→推送→官方页，每晚/每周循环。
- 定时任务：每晚 22:47 轻量雷达 + 每周日 20:03 完整维护循环（持久化，7 天过期需续期）。
- `.github/ISSUE_TEMPLATE/tech-candidate.md`（ai/java 各一）—— 候选新框架提 issue 模板。
- **GitHub Pages 官方站 + wiki**：待用户创建根仓库 `oss-learning` 后，以 `docs/` 作为 Pages 源，首页对齐 README 核心能力表。

### 待办（二期收尾）

1. 等待 java(225)/ai(77) 两个 add 批次跑完，验证 `git submodule status` 无 `-` 前缀。
2. 提交并推送 ai、java 两超项目（含 README 更新、CoPaw→qwenpaw 改名、issue 模板、MetaGPT 修正）。
3. 创建根仓库 → GitHub Pages 官方站 + wiki。
4. 后续项目（用户另行启动）：技术面试小册（AI 自维护，见记忆）。

---

## 三期：多维度雷达 + AI 情报站（2026-08-31）

用户连续点题："你要分析下为啥你没把他找出来（openworker）"、"从各个维度去找各种项目"、
"弄个 AI 情报站，GitHub Pages 里加个栏目"、"自己想想打造哪些流量"、"写作方向等都得把关"。三期落地：

### 雷达多维度升级（堵 topic 盲区）

- **根因**：旧雷达只按 `topic:X` 搜索，`andrewyng/openworker`（⭐17k）**没打任何 topic**（`topics:[]`）→ 永远搜不到。
- **修复**（`scripts/watch-trending.py`）：
  - 维度① 主题标签 topic（原有）；
  - 维度② 关键词搜索（名称/描述命中，兜住没打标签的仓库）；
  - 维度③ 跨主题飙升榜：`created>N` + **星级分档**（100k+/30k-100k/10k-30k/5k-10k/2k-5k），**每档取前 3**——避免巨型新星挤掉中量级黑马。
- **验证**：`stars:10000..30000` 档命中 openworker 17076⭐；候选从 ~40 → **74 个**。
- 报告每行带「标签」列，`-` = 无 topic 黑马（重点看）。

### AI 情报站栏目（GitHub Pages 新栏目）

- `docs/intel/index.md` —— 枢纽页：每日快讯索引 + 雷达归档 + 专题收藏 + **编辑方针** + **流量策略**。
- `docs/intel/<date>.md` —— 每日快讯（AI 撰写）：①头条 → ②飙升盘点 → ③接入清单 → ④变现提示。
- `docs/index.md` 首页挂「📡 AI 情报站」入口 + 雷达亮点（openworker/deepseek-harness/claw-code）。

### 流量策略与写作把关（用户点名）

- **流量盘子**：开发者（雷达/快讯→GitHub/掘金/知乎）、企业架构师（蓝图→搜索长尾/公众号）、副业接单（接单盘点→掘金/知乎/公众号）、面试者（小册→二期）。
- **运营节奏**：每日快讯 → 每周《开源精选》→ 每月《AI 开源月报》；Pages 当内容仓库，公众号/掘金当分发渠道。
- **编辑方针**：有选型价值 / 格式固定 / 信息可验证 / 观点有依据 / 结尾挂三条变现链路。
- 定时任务已更新：每晚 22:47（雷达+快讯+日志+推送）、每周日 20:03（完整循环），持久化、7 天过期需续期。

### 三期计数

- **ai**：78 → **79**（+Agent/openworker，Andrew Ng 出品，无 topic 黑马）。
- 全部已提交推送（ai 37e4f1f 重推成功；root 雷达/情报站/skill 文档待推）。
