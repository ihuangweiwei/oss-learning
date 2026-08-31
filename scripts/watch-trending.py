#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术雷达 watch-trending.py — 多维度扫描 GitHub 新框架/飙升项目，生成候选报告。

用法：
    python scripts/watch-trending.py [--days 180] [--output docs/tech-watch/YYYY-MM-DD.md]
    # 可选：设 GITHUB_TOKEN 提升 API 限额（未登录搜索 10 次/分，脚本会限速到 ~7s/次）

产物：
    docs/tech-watch/YYYY-MM-DD.md  —— 多维度候选报告（markdown），
    供 AI 审阅后决定是否引入 oss-learning 集合；也是「AI 情报站」（docs/intel/）的雷达原料。

多维度方法论（2026-08-31 起，堵"只搜 topic"的盲区）：
    维度① 主题标签 topic   —— 只命中「打了标签」的仓库；
    维度② 关键词          —— 名称/描述含关键词、但可能没打标签的仓库；
    维度③ 跨主题飙升榜     —— `created>N stars>M` 按 stars 排序、不限 topic，
                               专门抓「没打标签但暴涨」的黑马（如 andrewyng/openworker：17k⭐ 但 topics=[]）。
    教训：单靠 topic 搜索会漏掉 openworker 这类不按常理打标签的仓库，必须多维度兜底。

设计注意：
    - GitHub 搜索的 OR 链 + 日期限定组合偶发 422/403，因此按「每个查询单独查」，再按 stars 去重合并。
    - 网络断流有 3 次重试。
"""
import argparse
import datetime
import json
import os
import sys
import time
import urllib.parse
import urllib.request

# 分类雷达：名称 -> (topics, 关键词兜底)（每个查询单独一查）
CATEGORIES = [
    ("AI · Agent · LLM",       ["ai", "agent", "llm"],               ["llm-agents", "claude-code"]),
    ("Agent · Skills · MCP",   ["agent-skills", "mcp", "claude-skills"], ["agent-skills", "mcp"]),
    ("Java · 微服务 · 中间件",  ["java", "microservices", "spring-cloud"], ["mall", "lowcode", "admin"]),
    ("视频 · 内容 · 变现",      ["short-video", "video-generation", "content-creation"], ["text-to-video", "video"]),
    ("RAG · 搜索 · 记忆",      ["rag", "vector-database", "memory"],   ["vector-search", "rag"]),
]

MIN_STARS = 200          # 低于此星数不报（过滤纯玩具）
PER_TOPIC = 15           # 每个查询取前 N
TOP_OUTPUT = 15          # 每个分类最终报前 N
SURGE_STARS = 2000       # 维度③：跨主题飙升榜门槛
SURGE_PER_PAGE = 100     # 维度③：每档取前 100 再与上方去重
SURGE_PER_BRACKET = 3    # 维度③：每档上榜前 N（保证中量级黑马不被巨型新星淹没）
# 维度③ 星级分档：单查 stars:>2000 按 ⭐ 排序，前 100 全是 30k+ 巨型新星，
# 会漏掉 17k 的 openworker —— 分档查询保证每个量级都有黑马被看到。
SURGE_BRACKETS = [
    (100000, 999999999),   # >100k 巨型新星
    (30000, 100000),       # 30k–100k
    (10000, 30000),        # 10k–30k（openworker 17k 所在档）
    (5000, 10000),         # 5k–10k
    (2000, 5000),          # 2k–5k（门槛档）
]


def api(q, per_page=PER_TOPIC, token=""):
    params = urllib.parse.urlencode({"q": q, "sort": "stars", "order": "desc", "per_page": per_page})
    url = f"https://api.github.com/search/repositories?{params}"
    for attempt in range(3):
        req = urllib.request.Request(url)
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("User-Agent", "oss-learning-tech-radar")
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 422):
                return {"error": f"HTTP {e.code}", "items": []}
            if attempt == 2:
                return {"error": f"HTTP {e.code}", "items": []}
        except Exception:  # noqa: BLE001
            if attempt == 2:
                return {"error": "net", "items": []}
        time.sleep(2 + attempt * 2)
    return {"error": "unknown", "items": []}


def row_line(i, r):
    """渲染一行表格：仓库 | ⭐ | 语言 | 创建 | 标签 | 简介（无标签显式标注）。"""
    fn = r.get("full_name", "")
    topics = r.get("topics") or []
    tag = ("，".join(topics[:2])) if topics else "-"  # "-" = 没打标签（黑马，靠维度②③兜住）
    desc = (r.get("description") or "").replace("|", "\\|").strip()[:80]
    return (
        f"| {i} | [{fn}](https://github.com/{fn}) | {r.get('stargazers_count',0)} | "
        f"{r.get('language') or '-'} | {(r.get('created_at') or '')[:10]} | {tag} | {desc} |"
    )


def surge_velocity(r):
    """飙升速度：⭐/天（creation 至今），比绝对星数更接近"飙升"的含义。"""
    stars = r.get("stargazers_count", 0)
    created = (r.get("created_at") or "")[:10]
    days = 1
    if created:
        try:
            days = max((datetime.date.today() - datetime.date.fromisoformat(created)).days, 1)
        except ValueError:
            pass
    return stars / days


def main():
    ap = argparse.ArgumentParser(description="GitHub 技术雷达：多维度扫新框架/飙升项目")
    ap.add_argument("--days", type=int, default=180, help="只看近 N 天创建的项目（默认 180）")
    ap.add_argument("--output", default="", help="输出 md 路径（默认 docs/tech-watch/<今天>.md）")
    ap.add_argument("--min-stars", type=int, default=MIN_STARS)
    ap.add_argument("--surge-stars", type=int, default=SURGE_STARS, help="维度③跨主题飙升榜门槛")
    ap.add_argument("--sleep", type=float, default=7.0, help="未登录限速间隔秒（默认 7）")
    args = ap.parse_args()

    since = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat()
    token = os.environ.get("GITHUB_TOKEN", "")
    sleep_s = 0.0 if token else args.sleep

    lines = [
        f"# 技术雷达 · GitHub 新框架候选  {datetime.date.today().isoformat()}",
        "",
        "> 多维度扫描：**① 主题标签(topic) + ② 关键词(名称/描述) + ③ 跨主题飙升榜(不限 topic)**。",
        f"> 扫描窗口：近 {args.days} 天创建；维度①② 星数 ≥ {args.min_stars}，维度③ ≥ {args.surge_stars}。"
        "由 `scripts/watch-trending.py` 自动生成，也是「AI 情报站」雷达原料。",
        "",
        "> 每行「标签」列为 `-` 表示**未打标签**的仓库——单靠 topic 搜索会漏掉它们，"
        "正是开放雷达多维度兜底的原因。",
        "",
    ]
    grand = set()
    # 维度①②：按分类合并 topic + 关键词查询
    for label, topics, keywords in CATEGORIES:
        seen = {}
        errs = []
        for t in topics:
            data = api(f"topic:{t} created:>{since}", token=token)
            if data.get("error"):
                errs.append(f"topic:{t}({data['error']})")
            for r in data.get("items", []):
                if r.get("stargazers_count", 0) >= args.min_stars:
                    seen[r.get("full_name")] = r
            if sleep_s:
                time.sleep(sleep_s)
        for k in keywords:
            data = api(f"{k} created:>{since}", token=token)
            if data.get("error"):
                errs.append(f"kw:{k}({data['error']})")
            for r in data.get("items", []):
                if r.get("stargazers_count", 0) >= args.min_stars:
                    seen[r.get("full_name")] = r
            if sleep_s:
                time.sleep(sleep_s)
        items = sorted(seen.values(), key=lambda r: -r.get("stargazers_count", 0))[:TOP_OUTPUT]
        lines.append(f"### {label}  · 主题 + 关键词双维度")
        if errs:
            lines.append(f"> ⚠️ 部分查询失败：{'、'.join(errs)}")
        if not items:
            lines.append("_暂无候选_")
        else:
            lines.append("| # | 仓库 | ⭐ | 语言 | 创建 | 标签 | 简介 |")
            lines.append("|---|------|----|------|------|------|------|")
            for i, r in enumerate(items, 1):
                fn = r.get("full_name", "")
                grand.add(fn)
                lines.append(row_line(i, r))
        lines.append("")
        lines.append("---")
        lines.append("")

    # 维度③：跨主题飙升榜（不限 topic，抓未打标签的黑马）
    lines += [
        "## 维度③ 跨主题飙升榜（不限 topic，专门抓没打标签的黑马）",
        "",
        f"> 查询：`created:>{since} stars:{args.surge_stars}..100000+` **按星级分档、每档取前 {SURGE_PER_BRACKET}**，"
        "确保各量级黑马都上榜（如 openworker 17k）；跳过上方已出现过的仓库",
        "",
    ]
    surge_seen = {}  # fn -> (repo, 档位 label)
    surge_errs = []
    for lo, hi in SURGE_BRACKETS:  # 元组为 (下界, 上界)
        if lo < args.surge_stars:  # 门槛上调时不查低于门槛的档
            continue
        data = api(f"created:>{since} stars:{lo}..{hi}", per_page=SURGE_PER_PAGE, token=token)
        if data.get("error"):
            surge_errs.append(f"stars:{lo}..{hi}({data['error']})")
        bl = f"{lo // 1000}k+" if hi >= 10**9 else f"{lo // 1000}k~{hi // 1000}k"
        for r in data.get("items", []):
            fn = r.get("full_name")
            if fn and fn not in grand:
                surge_seen[fn] = (r, bl)
        if sleep_s:
            time.sleep(sleep_s)
    if surge_errs:
        lines.append(f"> ⚠️ 部分飙升档失败：{'、'.join(surge_errs)}")
    # 每档取前 N；档内按「飙升速度(⭐/天)」排序 + 无标签黑马优先——
    # 绝对星数会把 openworker(17k) 这类中量级黑马挤掉，而它速度其实是档内第一。
    by_bracket = {}
    for r, bl in surge_seen.values():
        by_bracket.setdefault(bl, []).append(r)
    surge_rows = []
    for bl in sorted(by_bracket, reverse=True):
        bucket = sorted(
            by_bracket[bl],
            key=lambda x: (-surge_velocity(x), -(0 if (x.get("topics") or []) else 1)),
        )[:SURGE_PER_BRACKET]
        for r in bucket:
            surge_rows.append((r, bl))
    if not surge_rows:
        lines.append("_暂无候选_")
    else:
        lines.append("| # | 仓库 | ⭐ | ⭐/天 | 档位 | 语言 | 创建 | 标签 | 简介 |")
        lines.append("|---|------|----|------|------|------|------|------|------|")
        for i, (r, bl) in enumerate(surge_rows, 1):
            fn = r.get("full_name", "")
            grand.add(fn)
            topics = r.get("topics") or []
            tag = ("，".join(topics[:2])) if topics else "-"
            desc = (r.get("description") or "").replace("|", "\\|").strip()[:80]
            lines.append(
                f"| {i} | [{fn}](https://github.com/{fn}) | {r.get('stargazers_count',0)} | "
                f"{surge_velocity(r):.0f} | {bl} | {r.get('language') or '-'} | "
                f"{(r.get('created_at') or '')[:10]} | {tag} | {desc} |"
            )
    lines.append("")
    lines.append("---")
    lines.append("")

    lines += [
        "## 行动建议",
        "",
        "1. 审阅上表，挑选 **新技术 / 飙升 / 赋能业务** 的仓库（`标签` 列为 `-` 的是主题盲区黑马，重点看）。",
        "2. 用 `.github/ISSUE_TEMPLATE/tech-candidate.md` 模板提 issue（或直接让 AI 评估引入）。",
        "3. 确认后：追加 `scripts/manifest.tsv` 行 → 跑 `scripts/add-submodules.sh` → 更新蓝图文档 → 提交推送。",
        "4. 亮点已选入「AI 情报站」每日快讯：`docs/intel/`。",
        "",
        "---",
        "",
        f"共 {len(grand)} 个候选（多维度去重）。",
    ]

    out = args.output or os.path.join("docs", "tech-watch", f"{datetime.date.today().isoformat()}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[OK] 报告已写入 {out}（共 {len(grand)} 个候选）")


if __name__ == "__main__":
    sys.exit(main())
