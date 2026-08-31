# 企业级 AI 平台落地蓝图（基于 oss-learning-ai）

> 用 `oss-learning/ai`（65 个子模块）+ 少量 java 侧组件，组装一套**企业级 AI 平台**参考架构，
> 目标是"技术栈 → 平台能力 → 赋能业务"，每个能力层都给出集合内的**对应仓库路径**。
> 日期：2026-08-31

## 1. 总体分层

```
┌──────────────────────────────────────────────────────────────┐
│ 业务接入  业务系统 / 前端 / 工单 / 客服 / 知识库入口            │
├──────────────────────────────────────────────────────────────┤
│ ① AI 网关层  统一鉴权 · 模型路由 · 限流/计费 · 缓存           │
│    LiteLLM · Higress · Vercel AI SDK · Spring AI             │
├──────────────────────────────────────────────────────────────┤
│ ② 模型层   DeepSeek-R1/V3 · (Qwen/Llama，权重走 ModelScope/HF) │
├──────────────────────────────────────────────────────────────┤
│ ③ RAG 知识库层  文档解析 · 向量检索 · 记忆                    │
│    Dify · RAGFlow · LlamaIndex · Haystack · Mem0             │
├──────────────────────────────────────────────────────────────┤
│ ④ Agent 编排层  工作流 · 多智能体 · 编码/操作 Agent            │
│    LangGraph · LangChain · AutoGen · CrewAI · OpenCode        │
├──────────────────────────────────────────────────────────────┤
│ ⑤ 工具/MCP 层  工具注册 · 浏览器/API · MCP 服务器             │
│    Composio · awesome-mcp-servers · browser-use              │
├──────────────────────────────────────────────────────────────┤
│ ⑥ 技能资产层   SKILL.md 技能库 · 提示词库                     │
│    anthropic-skills · superpowers · awesome-claude-skills     │
├──────────────────────────────────────────────────────────────┤
│ ⑦ 平台工程  可观测 · 评估 · 安全 · 多租户                     │
│    (对标 Dify/RAGFlow 自带面板) + java 侧 SkyWalking/Grafana   │
└──────────────────────────────────────────────────────────────┘
```

## 2. 能力层 → 仓库映射

| 层 | 能力 | 对应仓库（oss-learning 内） |
|---|---|---|
| **① AI 网关** | LLM 统一路由/代理/计费 | `ai/Framework/litellm` |
| | 前端/服务端 AI SDK | `ai/Framework/vercel-ai` |
| | 平台流量网关 | `ai/Platform/higress` |
| | Java 侧 AI 框架（企业 Spring 系） | `java/Spring/spring-ai` + `ai/Framework/spring-ai-alibaba` |
| **② 模型** | 开源模型代码（推理/训练脚本） | `ai/Models/DeepSeek-R1`、`ai/Models/DeepSeek-V3` |
| | 权重部署 | ModelScope / HF（不在本集合） |
| **③ RAG 知识库** | 企业知识库平台（开箱即用） | `ai/RAG/dify`、`ai/RAG/ragflow` |
| | RAG 框架（深度定制） | `ai/RAG/llama_index`、`ai/RAG/haystack` |
| | 记忆层（长期记忆/会话） | `ai/RAG/mem0` |
| **④ Agent 编排** | 图/工作流编排 | `ai/Framework/langgraph`、`ai/Framework/langchain` |
| | 多智能体协作 | `ai/Agent/autogen`、`ai/Agent/crewAI`、`ai/Agent/agno`、`ai/Agent/AutoGPT`、`ai/Agent/metaGPT` |
| | 编码/操作 Agent（研发提效） | `ai/Agent/opencode`、`ai/Agent/codex`、`ai/Agent/openclaw`、`ai/Agent/OpenHands`、`ai/Agent/cline`、`ai/Agent/aider` |
| | 企业级框架（微软/阿里） | `ai/Framework/semantic-kernel`、`ai/Framework/spring-ai-alibaba`、`ai/Agent/SmartEngine` |
| | 轻量/研究 | `ai/Framework/smolagents`、`ai/Agent/deepagents`、`ai/Agent/RD-Agent` |
| | 提示词工程 | `ai/Framework/dspy` |
| **⑤ 工具/MCP** | Agent 工具集成 | `ai/Agent/composio` |
| | 浏览器自动化 | `ai/Agent/browser-use` |
| | MCP 服务器清单 | `ai/Tutorial/awesome-mcp-servers` |
| **⑥ 技能资产** | 官方技能包 | `ai/Skills/anthropic-skills`、`ai/Skills/superpowers` |
| | 大厂/社区技能库 | `ai/Skills/microsoft-skills`、`ai/Skills/huggingface-skills`、`ai/Skills/antfu-skills` |
| | 技能索引（可检索 50k+） | `ai/Skills/awesome-claude-skills`、`ai/Skills/awesome-agent-skills`、`ai/Skills/awesome-claude-code` |
| **⑦ 平台工程** | 可视化工作流（产品级） | `ai/RAG/n8n`、`ai/RAG/Flowise`、`ai/RAG/langflow` |
| | 可观测（跨 super 复用） | `java/Middleware/grafana`、`java/Distributed/skywalking` |
| | 模型/场景评测 | ⚠️ 缺口：建议自建或引入 `langchain-ai/langsmith`、`confident-ai/deepeval`（后续可加） |

## 3. 落地路线图（4 阶段）

**Phase 0 · 跑通（1–2 周）**
1. LLM 网关：LiteLLM 统一接入多家模型（`ai/Framework/litellm`）
2. 快速知识库：部署 Dify（`ai/RAG/dify`）接 DeepSeek，出第一个"企业知识问答"MVP

**Phase 1 · RAG 深化（3–6 周）**
3. 私有化数据接入：RAGFlow 处理多格式文档（`ai/RAG/ragflow`）
4. 深度定制检索：LlamaIndex/Haystack + Mem0 记忆（`ai/RAG/llama_index`、`mem0`）
5. Java 业务系统集成：Spring AI / spring-ai-alibaba（`java/Spring/spring-ai`）

**Phase 2 · Agent 化（1–3 月）**
6. 编排：LangGraph 搭建业务 Agent 工作流（`ai/Framework/langgraph`）
7. 多智能体：AutoGen/CrewAI 协同（`ai/Agent/autogen`、`crewAI`）
8. 工具/MCP：Composio + browser-use 让 Agent 操作业务系统（`ai/Agent/composio`、`browser-use`）
9. 技能资产库沉淀 SKILL.md（`ai/Skills/*`）

**Phase 3 · 平台化（3–6 月）**
10. 网关治理：Higress 统一流量/限流/灰度（`ai/Platform/higress`）
11. 评测/可观测：接 LLM 评测 + Grafana/SkyWalking（跨 super）
12. 多租户/计费/安全：参考 Dify 产品实现 + Sa-Token（`java/Framework/Sa-Token`）

## 4. 典型业务赋能场景

| 业务场景 | 用到的层 | 组合示例 |
|---|---|---|
| 智能客服 | ①+③+④ | LiteLLM + Dify + LangGraph（多轮/工单） |
| 研发提效 | ④+⑤+⑥ | OpenCode/Codex + MCP + Skills |
| 知识管理 | ①+③ | RAGFlow + Mem0 + spring-ai 集成 OA |
| 数据智能问答 | ②+③+⑦ | DeepSeek + LlamaIndex + Dify 报表 |
| 文档处理 Agent | ④+⑤+⑥ | superpowers/docx + n8n 工作流 |

## 5. 选型速查（生产 vs 学习）

- **开箱即用平台**：Dify、RAGFlow（二选一即可，别都学）
- **深度开发**：LlamaIndex/Haystack + LangGraph + LiteLLM + Spring AI
- **Agent 产品**：OpenCode/OpenHands 看研发场景；AutoGen/CrewAI 看多智能体研究
- **避坑**：n8n/Flowise/Langflow 三者定位重叠，选一个玩即可

## 6. 维护约定

- 同 `enterprise-microservice-blueprint.md`：文档型参考，落地时按 LICENSE 合规、按版本复核。
- 模型权重不入库（走 ModelScope/HF），本集合只保留模型代码仓库。
- 后续可补：LLM 评测（LangSmith/deepeval）、LLMOps、向量库（Milvus/Chroma）——按需追加进 `ai/`。
