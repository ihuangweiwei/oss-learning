#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gitee-to-github.py — 把 gitee 子模块解析为 GitHub 镜像（有镜像换 GitHub，无镜像标 DELETED）。

背景：GitHub Pages 构建时会递归 clone 子模块，gitee 的 SSH 地址在 GitHub runner 上
无认证（Host key verification failed）→ 构建失败 → 站点 404。所以 gitee 子模块必须
换成 GitHub（有镜像时）或删除（无镜像时）。

用法：
    python scripts/gitee-to-github.py [--super java] [--dry-run]
    # --dry-run 只输出解析结果不写文件；去掉则生成 <super>.gitmodules.new 映射建议

每个候选都经 `git ls-remote <url> HEAD` 验证存在才接受（避免 wrong-origin）。
"""
import argparse
import os
import re
import subprocess
import sys

# gitee owner -> 候选 github owner（按优先级）。owner 相同的不必列。
OWNER_MAP = {
    "xuxueli0323":      ["xuxueli"],
    "bugstack_cn":      ["fuzhengwei"],
    "seata-io":         ["seata"],
    "arthas":           ["alibaba"],
    "OpenSkywalking":   ["apache"],
    "Sharding-Sphere":  ["apache"],
    "didiopensource":   ["didi"],
    "smallc":           ["chillzhuang", "smallbun"],
    "keepbx":           ["jiangzeyin"],
    "roncoocom":        ["roncoo"],
    "jd-platform-opensource": ["jd-opensource"],
    "other_alibaba_projects": ["alibaba"],
    "netflix":          ["Netflix"],
    # 不确定的 owner：给多个候选尝试，全失败则 DELETED
    "my_tony":          ["my_tony", "robertzml"],
    "gupaoedu-tom":     ["gupaoedu-tom"],
    "geektime-geekbang":["geektime-geekbang"],
    "Jay_git":          ["Jay_git"],
    "zto_express":      ["zto_express"],
    "fuyang_lipengjun": ["fuyang_lipengjun"],
    "sanshengshui":     ["sanshengshui"],
    "ld":               ["ld"],
}

# gitee repo (owner/repo) -> github 候选（owner, repo）。用于重命名/改名/大写修正。
REPO_MAP = {
    "mirrors/Nacos":                   [("alibaba", "nacos")],
    "mirrors/Hystrix":                 [("Netflix", "Hystrix")],
    "mirrors/ribbon":                  [("Netflix", "ribbon")],
    "mirrors/JetCache":                [("alibaba", "JetCache")],
    "mirrors/spring-cloud-netflix":    [("spring-cloud", "spring-cloud-netflix")],
    "mirrors/elastic-job-lite":        [("apache", "shardingsphere-elasticjob")],
    "mirrors/transmittable-thread-local": [("alibaba", "transmittable-thread-local")],
    "mirrors/JCTools":                 [("JCTools", "JCTools")],
    "mirrors/EasyTransaction":         [("QNJR-GROUP", "EasyTransaction")],
    "mirrors/RocketMQ-Externals":      [("apache", "rocketmq-externals")],
    "mirrors/OpenAPI-Generator":       [("OpenAPITools", "openapi-generator")],
    "mirrors/zipkin":                  [("openzipkin", "zipkin")],
    "mirrors/ff4j":                    [("ff4j", "ff4j")],
    "mirrors/cobarclient":             [("alibaba", "cobarclient")],
    "mirrors/X-Pipe":                  [("ctripcorp", "x-pipe")],
    "mirrors/gnet":                    [("panjf2000", "gnet")],
    "mirrors/Dubbo-Spring-Boot-Project": [("apache", "dubbo-spring-boot-project")],
    "mirrors/light-task-scheduler":    [("ltsopensource", "light-task-scheduler")],
    "mirrors/FEBS-Shiro":              [("febsteam", "FEBS-Shiro")],
    "OpenSkywalking/sky-walking":      [("apache", "skywalking")],
    "Sharding-Sphere/sharding-sphere": [("apache", "shardingsphere")],
}

PROXY = os.environ.get("HTTP_PROXY", "http://127.0.0.1:7897")


def exists(url):
    """git ls-remote 验证仓库存在。"""
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        r = subprocess.run(
            ["git", "-c", f"http.proxy={PROXY}", "-c", "http.lowSpeedLimit=500",
             "-c", "http.lowSpeedTime=10", "-c", "http.connectTimeout=15",
             "ls-remote", url, "HEAD"],
            capture_output=True, timeout=25, env=env,
        )
        return r.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def parse_submodules(path):
    mods = []
    cur = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        m = re.match(r'\[submodule "(.*)"\]', line)
        if m:
            if cur:
                mods.append(cur)
            cur = {"path": m.group(1)}
            continue
        m = re.match(r"url = (.*)", line)
        if m:
            cur["url"] = m.group(1)
    if cur:
        mods.append(cur)
    return mods


def candidates(gitee_owner, gitee_repo):
    key = f"{gitee_owner}/{gitee_repo}"
    if key in REPO_MAP:
        for o, r in REPO_MAP[key]:
            yield f"https://github.com/{o}/{r}.git"
    owners = [gitee_owner] + OWNER_MAP.get(gitee_owner, [])
    seen = set()
    for o in owners:
        u = f"https://github.com/{o}/{gitee_repo}.git"
        if u not in seen:
            seen.add(u)
            yield u


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--super", default="java", help="super 目录（java/ai）")
    ap.add_argument("--dry-run", action="store_true", help="只输出不落盘")
    args = ap.parse_args()

    gm = os.path.join(args.super, ".gitmodules")
    mods = parse_submodules(gm)
    gitee = [x for x in mods if "gitee" in x["url"]]
    print(f"共 {len(mods)} 个子模块，gitee {len(gitee)} 个")

    results = []  # (path, gitee_url, github_url|None)
    for x in gitee:
        m = re.match(r"git@gitee\.com:([^/]+)/([^/]+)\.git", x["url"])
        if not m:
            results.append((x["path"], x["url"], None))
            continue
        owner, repo = m.group(1), m.group(2)
        hit = None
        for c in candidates(owner, repo):
            print(f"  验证 {x['path']}: {c}", flush=True)
            if exists(c):
                hit = c
                break
        results.append((x["path"], x["url"], hit))

    # 汇总
    resolved = [r for r in results if r[2]]
    dead = [r for r in results if not r[2]]
    print("\n==== 解析结果 ====")
    print(f"有 GitHub 镜像: {len(resolved)}  |  无镜像(待删除): {len(dead)}")
    print("\n--- 无镜像（删除）---")
    for path, url, _ in dead:
        print(f"  {path}\t{url}")
    print("\n--- 有镜像 ---")
    for path, url, gh in resolved:
        print(f"  {path}\t{gh}")

    out = os.path.join(args.super, "gitee-mapping.tsv")
    if not args.dry_run:
        with open(out, "w", encoding="utf-8") as f:
            for path, url, gh in results:
                f.write(f"{path}\t{gh or 'DELETED'}\n")
        print(f"\n映射已写入 {out}")


if __name__ == "__main__":
    sys.exit(main())
