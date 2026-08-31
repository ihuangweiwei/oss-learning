---
layout: default
title: oss-learning · AI 驱动的开源学习与技术选型
---

# 🚀 oss-learning

**AI 驱动的开源学习 · 技术选型 · 企业级平台落地 · 流量变现**

> 用 git submodule 同步 **~315 个高质量开源项目**，AI 每晚/每周自动扫描 GitHub 新框架、
> 审阅引入、沉淀蓝图与文档、自动提 issue —— 把"学开源"变成"AI 自行规划技术栈"。
> 技术赋能企业，最终为了赚钱：**企业落地 / 接单交付 / 流量变现** 三条变现链路。

---

## 📊 现在

| 指标 | 值 |
|---|---|
| 开源项目合集 | **~316 个**（ai 79 + java 235） |
| 企业微服务蓝图 | 10 层架构 + 4 阶段路线图 |
| 企业 AI 平台蓝图 | 8 层架构 + 4 阶段路线图 |
| 技术雷达 | 每晚自动扫描 GitHub 新框架 |
| 定时自维护 | 每晚 22:47 + 每周日 20:03 |
| 沉淀 Skill | `oss-learning-maintainer` |

## 🧭 核心能力

| | 能力 | 入口 |
|---|---|---|
| 🤖 | **技术雷达**：自动扫 GitHub 新框架/飙升项目（多维度：topic + 关键词 + 跨主题飙升） | [雷达报告](tech-watch/2026-08-31.md) |
| 📡 | **AI 情报站**：每日快讯 + 飙升盘点 + 专题收藏（编辑把关 + 流量策略） | [情报站](intel/index.md) |
| 🧩 | **开源合集**：ai（企业 AI 平台栈）+ java（微服务栈 + 接单项目 + 云生态） | `ai/` · `java/`（独立仓库） |
| 🏭 | **企业微服务蓝图**：网关→框架→注册→治理→数据→中间件→可观测→安全→云原生→AI | [蓝图](enterprise-microservice-blueprint.md) · [架构图](diagrams/microservice-architecture.drawio) |
| 🚀 | **企业 AI 平台蓝图**：AI 网关→模型→RAG→Agent→工具/MCP→技能→平台工程→变现 | [蓝图](enterprise-ai-platform-blueprint.md) · [架构图](diagrams/ai-platform.drawio) |
| ☁️ | **云平台生态分析**：阿里/腾讯/华为/AWS/微软/CNCF 开源生态映射 | [云生态](cloud-ecosystem.md) |
| 💰 | **变现链路**：企业落地 / 接单项目（小程序商城·后台·低代码）/ 短视频·文生图 | `ai/Applications` · `java/Examples` |
| 📦 | **自维护 skill**：全部方法论与需求沉淀 | [skill 入口](skills/) |
| 📝 | **自动提 issue**：候选新框架用模板提 issue | `.github/ISSUE_TEMPLATE/tech-candidate.md` |

## 📅 技术雷达（最新）

最新候选报告：`tech-watch/`（每晚更新）+ [AI 情报站每日快讯](intel/index.md)。近期亮点：

- **deepseek-harness** ⭐205k —— DeepSeek "Everything is a Plugin" 工具链（2026-08-13 新建）
- **claw-code** ⭐195k —— Rust 写的 agent 基础设施（无 topic 黑马，多维度雷达抓获）
- **openworker** ⭐17k —— Andrew Ng 出品，无 topic 黑马，雷达升级后引入（见[快讯](intel/2026-08-31.md)）
- **OpenMontage** ⭐54k —— 开源智能视频制作系统（AI 短视频）
- **DeepSeek-Reasonix** ⭐35k —— DeepSeek 原生终端编程 Agent
- **融光 ai-fusion-video** —— 基于 Agent 的全流程 AI 短剧/漫剧创作（Java）
- **ReachAI** —— 企业级智能体改造 OA/ERP/CRM（赋能企业）
- **caveman** ⭐101k —— Claude Code 技能（省 token）

## 📖 文档

- [AI 情报站（每日快讯 · 专题 · 编辑方针）](intel/index.md)
- [企业微服务落地蓝图](enterprise-microservice-blueprint.md)
- [企业 AI 平台落地蓝图](enterprise-ai-platform-blueprint.md)
- [云平台生态分析](cloud-ecosystem.md)
- [自维护 Skill（全部方法论与需求）](skills/)
- [设计文档与实施说明](superpowers/specs/2026-08-30-oss-learning-design.md)

## 🔄 如何自维护（AI 自驱动）

```
雷达扫描 → AI 审阅候选 → 引入仓库 → 沉淀文档/蓝图 → 提 issue → 提交推送
```

- **每晚 22:47**：轻量雷达 + 更新本页更新日志 + 推送。
- **每周日 20:03**：完整循环（雷达、审阅、查重、引入、更新蓝图/README/架构图、提 issue、推送）。
- **经典不删**：老技术保留用于学习，只引入新时代。
- 复刻方法：读 [oss-learning-maintainer skill](skills/)，按"快速开始"跑一次完整循环。

## 📝 更新日志

- **2026-08-31**：二期启动——新增 ai Applications（短视频/文生图/PCB）、Agent 新框架、Skills 技能库、modelscope；
  java 新增微服务框架 + 6 接单项目（newbee-mall/mall4j/mall4cloud/jeecg-boot/RuoYi-Vue-Plus）+ 5 云生态（etcd/kubeedge/openGauss/openGemini/Tars）；
  企业蓝图 + drawio 架构图 + 云生态分析；技术雷达上线；自维护 skill + 每晚/每周定时任务；README 全面重写；根仓库建站。
- 历史：一期完成 ai/java 两个 super-project 同步与清单化（manifest.tsv）。

## 🔗 源码仓库（各自独立 GitHub Pages）

| 仓库 | 说明 | GitHub Pages |
|---|---|---|
| `oss-learning` | 本页 + 文档 + 脚本 + skill（根仓库） | [本站](https://ihuangweiwei.github.io/oss-learning/) |
| `oss-learning-ai` | 企业 AI 平台技术栈（78 子模块） | [AI 平台站](https://ihuangweiwei.github.io/oss-learning-ai/) |
| `oss-learning-java` | 企业微服务技术栈（235 子模块） | [微服务站](https://ihuangweiwei.github.io/oss-learning-java/) |
