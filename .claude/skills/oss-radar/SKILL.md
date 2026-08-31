---
name: oss-radar
description: 跑多维度技术雷达，扫描 GitHub 新框架/飙升项目并 AI 审阅候选。当你需要"找新框架""跑技术雷达""选技术栈""看最近 GitHub 又火了什么""找黑马项目"时使用。产物：docs/tech-watch/YYYY-MM-DD.md 候选报告，并提炼亮点给 oss-intel 情报站用。
---

# oss-radar · 技术雷达 Skill

> 多维度扫描 GitHub 新框架/飙升项目 → 生成候选报告 → AI 审阅 → 提炼亮点。
> 本技能承接 oss-learning-maintainer 维护循环的 Step 1–2。

## 1. 跑雷达

```bash
cd /d/MyWorkSpace/oss-learning
python scripts/watch-trending.py --days 180
# 产物：docs/tech-watch/YYYY-MM-DD.md（三维度候选表）
# 可选：GITHUB_TOKEN 提升限额（未登录 ~7s/次，全程约 3 分钟）
```

## 2. 三维度方法论（堵"只搜 topic"的盲区）

- **维度① 主题标签 topic**：按分类查 `topic:X created:>N`——只命中「打了标签」的仓库。
- **维度② 关键词**：`X created:>N` 查名称/描述，兜住**没打标签**的仓库。
- **维度③ 跨主题飙升榜**：`created:>N stars:>2000` **按星级分档**（100k+/30-100k/10-30k/5-10k/2-5k）、每档按 ⭐/天 速度取前 3、不限 topic——专门抓不按常理打标签的黑马。

**教训**：`andrewyng/openworker`（⭐17k 但 `topics:[]`）曾被单靠 topic 搜索漏掉。报告每行带「标签」列，`-` = 无 topic 的黑马（重点看）。

## 3. AI 审阅候选（关键决策步）

对候选报告逐条评估是否值得引入：

- **值得**：新技术 / 飙升 / 赋能业务 / 引流（新 Agent 框架、MCP、短视频、文生图、行业 AI）。
- **查重**：对照 `scripts/manifest.tsv` 的 origin 与已注册路径，避免重复（Sentinel/sofa-boot/seata/nacos/openworker 等已在册）。
- **经典不删**：老项目保留用于学习，只做"引入新时代"。
- **三价值取向**：赋能企业 / 赋能接单 / 引流学习——不为了"显得活跃"乱引入低质项目。

## 4. 选中的下一步

1. 把亮点交给 `oss-intel`（写今日快讯）；
2. 需要引入的交给 `oss-introduce`（按 manifest 加子模块）；
3. 值得公开讨论的交给 `oss-release`（提 issue）。

## 5. 避坑

- **GitHub API**：OR 链 + 日期限定易 422/403，雷达按"每个查询单查"最稳；未登录限 10 次/分，可设 `GITHUB_TOKEN` 提速。
- **黑马盲区**：`topic:` 只命中打了标签的仓库——必须多维度兜底，报告要显式标注"无标签黑马"。
