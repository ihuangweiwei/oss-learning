# oss-learning 开源学习同步项目 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 在 `D:\MyWorkSpace\oss-learning` 下创建两个 git 超级项目（`ai/`、`java/`），把所有开源学习代码以 submodule 方式注册进来，统一同步、可推送远端。

**Architecture:** 标准 submodule 工作流。初始化两个独立超级项目后，对每个开源项目执行 `git submodule add <origin> <category>/<name>`，由 git 直接在超级项目内拉取（fresh clone）。清单由扫描 learn/WorkSpace/spring-ai 生成，去重并排除个人项目。子模块跟踪上游最新（`git submodule update --remote`）。

**Tech Stack:** git submodule、bash 脚本、GitHub/Gitee。

## Global Constraints

- 父文件夹 `D:\MyWorkSpace\oss-learning` 本身**不是** git 仓库，只放说明与一次性脚本。
- 两个独立超级项目：`oss-learning/ai`、`oss-learning/java`，各有独立 `.gitmodules`，可分别 clone/push/同步。
- 子模块 URL 沿用现有 SSH origin 地址（`git@github.com:...` / `git@gitee.com:...`），不做改动。
- 子模块更新策略：跟踪上游最新（`git submodule update --remote`），不使用固定 commit 快照。
- **排除清单**（不纳入）：`eastmoney-fc` `stock-dashboard` `stock-skills` `wencai-crawler` `wx-stock-pro` `shangchu` `stock-admin` `light-food-health` `dingding-talk` `sinolink-ai-recruit`（无 remote）`marvis-office`（无 .git）以及无 `.git` 的普通文件夹。
- **去重**：同一 origin 只注册一份，重复副本（learn/AI、WorkSpace、spring-ai 之间的 dify/opencode/langchain4j/spring-ai-alibaba 等）不重复添加。
- `ai-agent-research`（ihuangweiwei 自有 AI 合集）作为子模块挂入 `ai/Research/`，其内部子模块保持自身结构（`--recursive` 拉取）。
- 旧 `learn/`、`WorkSpace/`、`spring-ai/` 保持原样，**不移动、不修改**；新机拉取、同步均以 oss-learning 为准。
- 所有 `git submodule add` 在本机执行（用户已具备这些仓库的 SSH 访问权限）。

---

### Task 1: 初始化两个超级项目仓库

**Files:**
- Create: `D:/MyWorkSpace/oss-learning/ai/.gitignore`
- Create: `D:/MyWorkSpace/oss-learning/java/.gitignore`
- Create: `D:/MyWorkSpace/oss-learning/scripts/`（存放一次性脚本）

**Interfaces:**
- Produces: 两个可提交的 git 仓库（ai、java），后续 Task 3/4 在此仓库内 `git submodule add`。

- [ ] **Step 1: 创建目录并 git init**

```bash
mkdir -p /d/MyWorkSpace/oss-learning/{ai,java,scripts}
cd /d/MyWorkSpace/oss-learning/ai && git init
cd /d/MyWorkSpace/oss-learning/java && git init
```

- [ ] **Step 2: 设置本地 user 配置与 .gitignore**

在两个仓库各写一份 `.gitignore`：

```gitignore
*.log
*.tmp
.DS_Store
Thumbs.db
```

并设置本地身份（若全局已配置可跳过）：

```bash
cd /d/MyWorkSpace/oss-learning/ai
git config user.name "ihuangweiwei"
git config user.email "ihuangweiwei@users.noreply.github.com"
cd /d/MyWorkSpace/oss-learning/java
git config user.name "ihuangweiwei"
git config user.email "ihuangweiwei@users.noreply.github.com"
```

- [ ] **Step 3: 初始提交**

```bash
cd /d/MyWorkSpace/oss-learning/ai && git add .gitignore && git commit -m "chore: init oss-learning ai super-project"
cd /d/MyWorkSpace/oss-learning/java && git add .gitignore && git commit -m "chore: init oss-learning java super-project"
```

- [ ] **Step 4: 验证**

```bash
cd /d/MyWorkSpace/oss-learning/ai && git log --oneline
cd /d/MyWorkSpace/oss-learning/java && git log --oneline
```

Expected: 各一行 `chore: init ...` 提交。

---

### Task 2: 生成子模块清单 manifest

**Files:**
- Create: `D:/MyWorkSpace/oss-learning/scripts/scan.sh`
- Create: `D:/MyWorkSpace/oss-learning/scripts/build-manifest.sh`
- Create（运行产出）: `scripts/raw-manifest.tsv`、`scripts/manifest.tsv`

**Interfaces:**
- Produces: `manifest.tsv`（`super \t category \t name \t origin`），Task 3/4 据此执行 submodule add。格式示例：
  ```
  java	Distributed	Sentinel	git@github.com:alibaba/Sentinel.git
  ai	Agent	opencode	git@github.com:anomalyco/opencode.git
  ai	Research	ai-agent-research	git@github.com:ihuangweiwei/ai-agent-research.git
  ```

- [ ] **Step 1: 写扫描脚本 `scripts/scan.sh`**

```bash
#!/bin/bash
# 扫描源目录，输出 raw-manifest.tsv: name<TAB>relpath<TAB>origin
set -u
OUT="$(dirname "$0")/raw-manifest.tsv"
: > "$OUT"
scan() {
  local base="$1"
  [ -d "$base" ] || return 0
  ( cd "$base" || return
    while IFS= read -r g; do
      local dir name origin rel
      dir="$(dirname "$g")"
      name="$(basename "$dir")"
      origin="$(git -C "$dir" remote get-url origin 2>/dev/null || true)"
      rel="${dir#./}"
      printf '%s\t%s\t%s\n' "$name" "$rel" "$origin" >> "$OUT"
    done < <(find . -name .git \( -type d -o -type f \))
  )
}
scan "/d/MyWorkSpace/learn"
scan "/d/MyWorkSpace/WorkSpace"
scan "/d/MyWorkSpace/spring-ai"
echo "扫描到仓库数: $(wc -l < "$OUT")"
```

- [ ] **Step 2: 运行扫描，验证数量**

Run: `bash /d/MyWorkSpace/oss-learning/scripts/scan.sh`
Expected: 数量 ≈ 233（learn）+ 30（WorkSpace 含 .git 者）+ 6（spring-ai 含 .git 者）≈ 269。若偏差大，检查 find 深度与 `.git` 文件。

- [ ] **Step 3: 写分配脚本 `scripts/build-manifest.sh`**

```bash
#!/bin/bash
# 输入 raw-manifest.tsv，输出 manifest.tsv: super<TAB>category<TAB>name<TAB>origin
# 规则：排除个人项目 → 去重 → 按设计文档分类
set -u
IN="$(dirname "$0")/raw-manifest.tsv"
OUT="$(dirname "$0")/manifest.tsv"
: > "$OUT"
declare -A seen

exclude() { case "$1" in
  eastmoney-fc|stock-dashboard|stock-skills|wencai-crawler|wx-stock-pro|shangchu|stock-admin|light-food-health|dingding-talk|sinolink-ai-recruit|marvis-office) return 0;;
esac; return 1; }

# AI 侧名称→分类（learn/AI 与 WorkSpace 通用）
ai_cat() { case "$1" in
  opencode|openclaw|crewAI|agentscope|agentscope-java|CoPaw|HiClaw|RD-Agent|deepagents|deer-flow|oh-my-openagent|openagents|agency-agents-zh|ai-hedge-fund|SmartEngine|hermes-agent) echo Agent;;
  langchain|langchain4j|langgraph|spring-ai-alibaba|spring-ai-alibaba-examples|SpringAI-Alibaba-Quickstart) echo Framework;;
  dify|langflow|ragflow|n8n|maxkb) echo RAG;;
  llm-action|llm-cookbook|dive-into-llms|AI-Interview|awesome-mcp-servers|learn-claude-code) echo Tutorial;;
  temporal|camunda|higress|lumenx) echo Platform;;
  ai-agent-research) echo Research;;
  *) echo Agent;; esac; }

while IFS=$'\t' read -r name rel origin; do
  exclude "$name" && continue
  # 去重（按 origin；无 origin 则按 name）
  key="${origin:-$name}"
  [ -n "${seen[$key]:-}" ] && continue
  seen[$key]=1
  super=""; cat=""
  case "$rel" in
    learn/Xxl/*)            super=java; cat=Task;;
    learn/Bobo/*|learn/Geektime/*|learn/Gupao/*) super=java; cat=Courses;;
    learn/AI/nacos|learn/Alibaba/nacos) super=java; cat=Middleware;;
    learn/Alibaba/Sentinel|learn/Distributed/Sentinel) super=java; cat=Distributed;;
    learn/AI/*|learn/Alibaba/spring-ai-alibaba) super=ai; cat="$(ai_cat "$name")";;
    learn/spring-ai-alibaba) super=ai; cat=Framework;;
    learn/*) super=java; cat="$(echo "$rel" | cut -d/ -f2)";;
    WorkSpace/*) super=ai; cat="$(ai_cat "$name")";;
    spring-ai/*) case "$name" in
      ai-agent-research) super=ai; cat=Research;;
      lumenx) super=ai; cat=Platform;;
      *) continue;; esac;;
    *) continue;;
  esac
  printf '%s\t%s\t%s\t%s\n' "$super" "$cat" "$name" "$origin" >> "$OUT"
done < "$IN"
echo "清单条数: $(wc -l < "$OUT")"
echo "java: $(awk -F'\t' '$1=="java"' "$OUT" | wc -l)  ai: $(awk -F'\t' '$1=="ai"' "$OUT" | wc -l)"
```

- [ ] **Step 4: 运行分配，人工核对关键条目**

Run: `bash /d/MyWorkSpace/oss-learning/scripts/build-manifest.sh`
Expected: java + ai 条数 ≈ 269 − 排除（约 10）− 去重（约 10）≈ 245。
人工核对（grep 抽查）：
```bash
grep -P '^(ai\t(Research|Agent)\t(ai-agent-research|opencode|dify)\t)' /d/MyWorkSpace/oss-learning/scripts/manifest.tsv
grep -P 'Sentinel\t' /d/MyWorkSpace/oss-learning/scripts/manifest.tsv
grep -P '\tXxl' /d/MyWorkSpace/oss-learning/scripts/manifest.tsv   # 应无（Xxl 已并入 Task，但项目名保留 xxl-job 等）
```
确认：`ai-agent-research` → `ai/Research`；`Sentinel` → `java/Distributed`；个人项目全部不在清单内。

---

### Task 3: 在 java/ 超级项目中逐个 submodule add（分批）

**Files:**
- 执行环境：`D:/MyWorkSpace/oss-learning/java/`
- 依赖：Task 2 的 `scripts/manifest.tsv`（java 部分）

**Interfaces:**
- Consumes: `manifest.tsv` 中 `super=java` 的行。
- Produces: java/ 仓库的 `.gitmodules` + 已注册子模块 + 一次"加入全部子模块"的提交。

- [ ] **Step 1: 写并运行批量添加脚本（java 分批）**

创建 `scripts/add-submodules.sh`：

```bash
#!/bin/bash
# 用法: add-submodules.sh <super: ai|java> [category过滤器]
set -u
SUPER="$1"; FILTER="${2:-}"
ROOT="/d/MyWorkSpace/oss-learning"
MAN="$ROOT/scripts/manifest.tsv"
cd "$ROOT/$SUPER" || exit 1
awk -F'\t' -v s="$SUPER" -v f="$FILTER" '$1==s && (f=="" || $2==f) {print $2"\t"$3"\t"$4}' "$MAN" > /tmp/jobs.txt
echo "本批 $(wc -l < /tmp/jobs.txt) 个: $SUPER/${FILTER:-all}"
while IFS=$'\t' read -r cat name origin; do
  printf '  [%s/%s] %s\n' "$SUPER" "$cat" "$name"
  mkdir -p "$cat"
  if git submodule add "$origin" "$cat/$name" 2>&1 | tail -1; then
    :
  else
    echo "  !! 失败: $name"
  fi
done < /tmp/jobs.txt
```

Run（按分类分批，便于中途核对）：
```bash
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Base
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Distributed
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Middleware
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Spring
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Framework
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Task
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Transaction
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Util
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java BigData
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Courses
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Netflix
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Alibaba
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Alipay
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Go
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Vertx
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Nepxion
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java chaos
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java metric
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java itstack
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Manager
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Examples
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Knowledge
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh java Good
```

注：整个 java 批次的 clone 需要网络与时间（可放后台运行并监控）。任何单仓库失败不影响其他，失败条目记录后重试。

- [ ] **Step 2: 验证 java 子模块注册数量**

```bash
cd /d/MyWorkSpace/oss-learning/java
git submodule status | wc -l
awk -F'\t' '$1=="java"' /d/MyWorkSpace/oss-learning/scripts/manifest.tsv | wc -l
```

Expected: 两数相等。抽查 `git submodule status | head`。

- [ ] **Step 3: 提交 java 全部子模块指针**

```bash
cd /d/MyWorkSpace/oss-learning/java
git add .gitmodules && git add -A
git commit -m "feat: register all java learning submodules"
```

---

### Task 4: 在 ai/ 超级项目中逐个 submodule add

**Files:**
- 执行环境：`D:/MyWorkSpace/oss-learning/ai/`
- 依赖：Task 2 的 `scripts/manifest.tsv`（ai 部分）

**Interfaces:**
- Consumes: `manifest.tsv` 中 `super=ai` 的行。
- Produces: ai/ 仓库的 `.gitmodules` + 已注册子模块 + 一次"加入全部子模块"的提交。

- [ ] **Step 1: 分批 submodule add（ai）**

```bash
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh ai Agent
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh ai Framework
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh ai RAG
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh ai Tutorial
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh ai Platform
bash /d/MyWorkSpace/oss-learning/scripts/add-submodules.sh ai Research
```

`ai/Research/ai-agent-research` 是嵌套超级项目，注册后**不要**在 ai 里处理它的内部子模块；它们由 `--recursive` 拉取。

- [ ] **Step 2: 验证 ai 子模块注册数量**

```bash
cd /d/MyWorkSpace/oss-learning/ai
git submodule status | wc -l
awk -F'\t' '$1=="ai"' /d/MyWorkSpace/oss-learning/scripts/manifest.tsv | wc -l
```

Expected: 两数相等。

- [ ] **Step 3: 提交 ai 全部子模块指针**

```bash
cd /d/MyWorkSpace/oss-learning/ai
git add .gitmodules && git add -A
git commit -m "feat: register all ai learning submodules"
```

---

### Task 5: 同步脚本与说明文档

**Files:**
- Create: `D:/MyWorkSpace/oss-learning/ai/sync.sh`
- Create: `D:/MyWorkSpace/oss-learning/java/sync.sh`
- Create: `D:/MyWorkSpace/oss-learning/sync-all.sh`
- Create: `D:/MyWorkSpace/oss-learning/README.md`

**Interfaces:**
- Consumes: Task 3/4 注册好的子模块。
- Produces: 可一键同步的脚本与顶层使用说明。

- [ ] **Step 1: 写 ai/sync.sh 与 java/sync.sh（内容相同，放各仓库根）**

```bash
#!/bin/bash
# 同步所有子模块到上游最新，并提交新指针
set -e
git submodule update --remote --merge
git add -A
if ! git diff --cached --quiet; then
  git commit -m "chore: sync submodules to upstream latest [$(date +%F)]"
  git push
else
  echo "无更新"
fi
```

并 `chmod +x ai/sync.sh java/sync.sh`。

- [ ] **Step 2: 写顶层 `oss-learning/sync-all.sh`**

```bash
#!/bin/bash
set -e
echo "=== 同步 ai ===" && (cd "$(dirname "$0")/ai" && ./sync.sh)
echo "=== 同步 java ===" && (cd "$(dirname "$0")/java" && ./sync.sh)
```

并 `chmod +x`。

- [ ] **Step 3: 写 `oss-learning/README.md`**

内容须包含：
- 结构说明（ai/ 与 java/ 是两个独立 git 仓库，父目录不是仓库）
- 首次拉取（新机）：
  ```bash
  git clone <ai 远端> oss-learning-ai && cd oss-learning-ai && git submodule update --init --recursive
  git clone <java 远端> oss-learning-java && cd oss-learning-java && git submodule update --init --recursive
  ```
- 日常同步：`bash sync-all.sh`
- 分类说明与排除说明
- 引用设计文档路径 `docs/superpowers/specs/2026-08-30-oss-learning-design.md`

- [ ] **Step 4: 提交脚本与文档**

```bash
cd /d/MyWorkSpace/oss-learning/ai && git add sync.sh && git commit -m "chore: add submodule sync script"
cd /d/MyWorkSpace/oss-learning/java && git add sync.sh && git commit -m "chore: add submodule sync script"
```

---

### Task 6: 全量验证（关键）

**Files:**
- 验证目标：`oss-learning/ai`、`oss-learning/java`

- [ ] **Step 1: 逐个仓库完整性抽查**

```bash
cd /d/MyWorkSpace/oss-learning/java
git submodule status | awk '{print $1}' | grep -c '^-' || true    # 期望 0（无未初始化）
find . -maxdepth 2 -name .git -type d | wc -l                     # 期望 = 子模块数
```
对 ai/ 执行同样命令。检查是否存在"空目录"或"只含 .gitmodules 但无代码"的子模块：
```bash
git -C /d/MyWorkSpace/oss-learning/java submodule foreach 'test -f .git && echo "empty: $sm_path"' 2>/dev/null | grep empty || true
```

- [ ] **Step 2: 全新 clone + recursive 拉取冒烟测试（本地路径模拟）**

```bash
rm -rf /d/tmp/verify-ai && git clone /d/MyWorkSpace/oss-learning/ai /d/tmp/verify-ai
cd /d/tmp/verify-ai && git submodule update --init --recursive 2>&1 | tail -3
git submodule status | wc -l    # 期望与 Task 4 相等
```
对 java 执行同样操作。验证 `ai/Research/ai-agent-research` 的内部子模块也被拉取（`ls ai/Research/ai-agent-research | head`）。

- [ ] **Step 3: 冒烟测试后清理**

```bash
rm -rf /d/tmp/verify-ai /d/tmp/verify-java
```

---

### Task 7: 推送远端并收尾

**Files:**
- 远端仓库（用户 GitHub/Gitee）：`oss-learning-ai`、`oss-learning-java`
- 提交：设计文档与计划文档

- [ ] **Step 1: 确认远端仓库名与平台（需用户确认）**

默认：GitHub `git@github.com:ihuangweiwei/oss-learning-ai.git`、`git@github.com:ihuangweiwei/oss-learning-java.git`。执行前用 AskUserQuestion 向用户确认平台与名称，若已选 Gitee 则用 `git@gitee.com:...`。

- [ ] **Step 2: 创建远端仓库并推送**

若 `gh` 已登录：
```bash
gh repo create ihuangweiwei/oss-learning-ai --private --source /d/MyWorkSpace/oss-learning/ai --push
gh repo create ihuangweiwei/oss-learning-java --private --source /d/MyWorkSpace/oss-learning/java --push
```
否则：
```bash
cd /d/MyWorkSpace/oss-learning/ai && git remote add origin git@github.com:ihuangweiwei/oss-learning-ai.git && git push -u origin HEAD
cd /d/MyWorkSpace/oss-learning/java && git remote add origin git@github.com:ihuangweiwei/oss-learning-java.git && git push -u origin HEAD
```

- [ ] **Step 3: 提交设计文档与计划到 java/（作为文档仓库）**

```bash
cd /d/MyWorkSpace/oss-learning/java
mkdir -p docs/superpowers
cp /d/MyWorkSpace/oss-learning/docs/superpowers/specs/2026-08-30-oss-learning-design.md docs/superpowers/specs/
cp /d/MyWorkSpace/oss-learning/docs/superpowers/plans/2026-08-30-oss-learning.md docs/superpowers/plans/
git add docs && git commit -m "docs: add oss-learning design and plan" && git push
```

- [ ] **Step 4: 收尾说明**

在 `oss-learning/README.md` 顶部加入已推送的远端地址。提醒用户：旧 `learn/`、`WorkSpace/` 已不被本项目引用，确认后自行归档或删除。

---

## Self-Review

- **Spec 覆盖**：目标（Task 1 初始化）✓；两个超级项目（Task 1）✓；WorkSpace 仅 AI 学习类（Task 2 映射）✓；ai-agent-research → ai/Research（Task 2/4）✓；跟踪上游最新（Task 5 sync.sh）✓；推送远端（Task 7）✓；排除/去重（Task 2）✓；旧目录不动（Global Constraints + Task 7 Step 4）✓。
- **占位扫描**：无 TBD；远端仓库名是唯一待确认项（Task 7 Step 1 显式询问）。
- **类型一致性**：manifest 字段 `super/category/name/origin` 在 Task 2/3/4 间一致；脚本路径一致。
