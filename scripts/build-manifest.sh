#!/bin/bash
# 输入 raw-manifest.tsv，输出 manifest.tsv: super<TAB>category<TAB>name<TAB>origin
# 规则：排除个人项目 → 去重（按 origin）→ 按设计文档分类
set -u
SELF="$(dirname "$0")"
IN="$SELF/raw-manifest.tsv"
OUT="$SELF/manifest.tsv"
: > "$OUT"
declare -A seen

exclude() { case "$1" in
  eastmoney-fc|stock-dashboard|stock-skills|wencai-crawler|wx-stock-pro|shangchu|stock-admin|light-food-health|dingding-talk|sinolink-ai-recruit|marvis-office) return 0;;
  # Windows 无法 checkout 的路径（含 : ? | 或尾随空格），git for windows 报 invalid path
  segmentfault-lessons|geek-nodejs|Blog|technology-talk|Spring-Boot-Reference-Guide|llm-action) return 0;;
  # 用户自己的仓库（ihuangweiwei）
  stock-admin-backend|stock-admin-frontend|stock-analysis) return 0;;
  # ai-agent-research 为私有/已删除仓库，不纳入
  ai-agent-research) return 0;;
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
    # spring-ai：仅顶层 ai-agent-research 与 lumenx；其余（含内部子模块）跳过
    spring-ai/ai-agent-research) super=ai; cat=Research;;
    spring-ai/lumenx)             super=ai; cat=Platform;;
    spring-ai/*)                  continue;;
    # learn 特殊映射
    learn/Xxl/*)                     super=java; cat=Task;;
    learn/Bobo/*|learn/Geektime/*|learn/Gupao/*) super=java; cat=Courses;;
    learn/AI/nacos|learn/Alibaba/nacos) super=java; cat=Middleware;;
    learn/Alibaba/Sentinel|learn/Distributed/Sentinel) super=java; cat=Distributed;;
    learn/AI/*|learn/Alibaba/spring-ai-alibaba) super=ai; cat="$(ai_cat "$name")";;
    # learn 其余：分类 = 现有顶层文件夹名
    learn/*)                       super=java; cat="$(echo "$rel" | cut -d/ -f2)";;
    WorkSpace/*)                   super=ai; cat="$(ai_cat "$name")";;
    *) continue;;
  esac
  [ -z "$super" ] && continue
  printf '%s\t%s\t%s\t%s\n' "$super" "$cat" "$name" "$origin" >> "$OUT"
done < "$IN"

echo "清单条数: $(wc -l < "$OUT")"
echo "java: $(awk -F'\t' '$1=="java"' "$OUT" | wc -l)  ai: $(awk -F'\t' '$1=="ai"' "$OUT" | wc -l)"
echo "--- 目标路径冲突检查（category/name 重复） ---"
awk -F'\t' '{print $2"/"$3}' "$OUT" | sort | uniq -d
echo "--- 无 origin 检查 ---"
awk -F'\t' '$4=="" {print $2"/"$3" (无origin)"}' "$OUT"
