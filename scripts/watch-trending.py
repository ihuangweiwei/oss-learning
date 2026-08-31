#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术雷达 watch-trending.py — 自动扫描 GitHub 新框架/飙升项目，生成候选报告。

用法：
    python scripts/watch-trending.py [--days 180] [--output docs/tech-watch/YYYY-MM-DD.md]
    # 可选：设 GITHUB_TOKEN 提升 API 限额（未登录搜索 10 次/分，脚本会限速到 ~7s/次）

产物：
    docs/tech-watch/YYYY-MM-DD.md  —— 分类候选表（markdown），
    供 AI 审阅后决定是否引入 oss-learning 集合；也可据此开 GitHub issue。

设计注意：
    - GitHub 搜索的 OR 链 + 日期限定组合偶发 422/403，因此按「每个 topic 单独查」，
      再按 stars 去重合并，最稳。
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

# 分类雷达：名称 -> topic 列表（每个 topic 单独一查）
CATEGORIES = [
    ("AI · Agent · LLM",   ["ai", "agent", "llm"]),
    ("Agent · Skills · MCP", ["agent-skills", "mcp", "claude-skills"]),
    ("Java · 微服务 · 中间件", ["java", "microservices", "spring-cloud"]),
    ("视频 · 内容 · 变现",  ["short-video", "video-generation", "content-creation"]),
    ("RAG · 搜索 · 记忆",  ["rag", "vector-database", "memory"]),
]

MIN_STARS = 200          # 低于此星数不报（过滤纯玩具）
PER_TOPIC = 15           # 每个 topic 取前 N
TOP_OUTPUT = 15          # 每个分类最终报前 N


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


def main():
    ap = argparse.ArgumentParser(description="GitHub 技术雷达：扫新框架/飙升项目")
    ap.add_argument("--days", type=int, default=180, help="只看近 N 天创建的项目（默认 180）")
    ap.add_argument("--output", default="", help="输出 md 路径（默认 docs/tech-watch/<今天>.md）")
    ap.add_argument("--min-stars", type=int, default=MIN_STARS)
    ap.add_argument("--sleep", type=float, default=7.0, help="未登录限速间隔秒（默认 7）")
    args = ap.parse_args()

    since = (datetime.date.today() - datetime.timedelta(days=args.days)).isoformat()
    token = os.environ.get("GITHUB_TOKEN", "")
    sleep_s = 0.0 if token else args.sleep

    lines = [
        f"# 技术雷达 · GitHub 新框架候选  {datetime.date.today().isoformat()}",
        "",
        f"> 扫描窗口：近 {args.days} 天创建，星数 ≥ {args.min_stars}。由 `scripts/watch-trending.py` 自动生成。",
        "",
    ]
    grand = set()
    for label, topics in CATEGORIES:
        seen = {}
        errs = []
        for t in topics:
            data = api(f"topic:{t} created:>{since}", token=token)
            if data.get("error"):
                errs.append(f"{t}({data['error']})")
            for r in data.get("items", []):
                fn = r.get("full_name")
                if r.get("stargazers_count", 0) >= args.min_stars:
                    seen[fn] = r
            if sleep_s:
                time.sleep(sleep_s)
        items = sorted(seen.values(), key=lambda r: -r.get("stargazers_count", 0))[:TOP_OUTPUT]
        lines.append(f"### {label}")
        if errs:
            lines.append(f"> ⚠️ 部分 topic 失败：{'、'.join(errs)}")
        if not items:
            lines.append("_暂无候选_")
        else:
            lines.append("| # | 仓库 | ⭐ | 语言 | 创建 | 简介 |")
            lines.append("|---|------|----|------|------|------|")
            for i, r in enumerate(items, 1):
                fn = r.get("full_name", "")
                grand.add(fn)
                desc = (r.get("description") or "").replace("|", "\\|").strip()[:80]
                lines.append(
                    f"| {i} | [{fn}](https://github.com/{fn}) | {r.get('stargazers_count',0)} | "
                    f"{r.get('language') or '-'} | {(r.get('created_at') or '')[:10]} | {desc} |"
                )
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## 行动建议",
        "",
        "1. 审阅上表，挑选 **新技术 / 飙升 / 赋能业务** 的仓库。",
        "2. 用 `.github/ISSUE_TEMPLATE/tech-candidate.md` 模板提 issue（或直接让 AI 评估引入）。",
        "3. 确认后：追加 `scripts/manifest.tsv` 行 → 跑 `scripts/add-submodules.sh` → 更新蓝图文档 → 提交推送。",
        "",
        "---",
        "",
        f"共 {len(grand)} 个候选。",
    ]

    out = args.output or os.path.join("docs", "tech-watch", f"{datetime.date.today().isoformat()}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[OK] 报告已写入 {out}（共 {len(grand)} 个候选）")


if __name__ == "__main__":
    sys.exit(main())
