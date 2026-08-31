# 📦 技能资产（Skills）

本目录汇总 oss-learning 自维护方法论与可复用技能。**权威版本**放在 `.claude/skills/`（Claude Code 可直接调用），
本目录为公开站展示入口与说明。

## 自维护 Skill（核心）

| Skill | 路径 | 说明 |
|---|---|---|
| **oss-learning-maintainer** | `.claude/skills/oss-learning-maintainer/SKILL.md` | 全自动维护方法论：技术雷达→AI 审阅→引入→文档/蓝图→issue→推送→官方页；沉淀了全部历史需求（技术选型/自我学习/企业落地/接单/短视频·文生图·PCB/流量变现/经典不删/每晚每周自完善） |

## 维护循环（速览）

```
雷达扫描(watch-trending.py) → AI 审阅候选(查重 manifest.tsv)
→ 引入仓库(add-submodules.sh) → 沉淀文档(README/蓝图/drawio)
→ 提 issue(tech-candidate.md) → 提交推送 → 更新官方页
```

- **每晚 22:47**：轻量雷达 + 更新日志 + 推送
- **每周日 20:03**：完整维护循环
- **定时任务持久化**，7 天自动过期需续期

## 其他可复用技能库（ai/Skills 子模块）

`ai/Skills/` 下收录：anthropic-skills、superpowers、microsoft-skills、huggingface-skills、antfu-skills、
awesome-claude-skills、awesome-agent-skills、awesome-claude-code、caveman、khazix-skills（社区/大厂技能合集）。
