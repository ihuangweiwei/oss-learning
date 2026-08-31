---
name: oss-release
description: 把维护结果提 issue、提交推送到三个仓库，并维护官方页/wiki。当你需要"提 issue""提交推送""发布维护结果""更新 GitHub Pages 官方站""本周增量汇报"时使用。含网络/Windows/Pages 避坑。
---

# oss-release · 发布 Skill

> 把雷达、引入、情报站的成果变成公开可见的增量：提 issue → 提交推送 → 更新官方页。
> 本技能承接 oss-learning-maintainer 维护循环的 Step 5–7。

## 1. 自动提 issue

用 `.github/ISSUE_TEMPLATE/tech-candidate.md` 模板，把候选/计划整理成 issue：
`[技术雷达] 建议引入 <仓库>` 或 `[维护] <本周自更新摘要>`。AI 可自动开，也可整理后提示用户确认。

## 2. 提交推送三个仓库

```bash
# 每个仓库先 add+commit，再带网络块 push：
git -C java add -A && git -C java commit -m "chore: <日期> 自更新摘要"
git -C ai   add -A && git -C ai   commit -m "chore: <日期> 自更新摘要"
git -C oss-learning add -A && git -C oss-learning commit -m "chore: <日期> 文档/雷达/skill 更新"
```

**推送网络块**（必须带，否则 schannel/代理会挂；失败就重试）：

```bash
GIT_CONFIG_COUNT=5 \
GIT_CONFIG_KEY_0='url.https://github.com/.insteadOf' GIT_CONFIG_VALUE_0='git@github.com:' \
GIT_CONFIG_KEY_1=http.lowSpeedLimit GIT_CONFIG_VALUE_1=1000 \
GIT_CONFIG_KEY_2=http.lowSpeedTime GIT_CONFIG_VALUE_2=60 \
GIT_CONFIG_KEY_3=http.connectTimeout GIT_CONFIG_VALUE_3=30 \
GIT_CONFIG_KEY_4='url.ssh://git@gitee.com/.insteadOf' GIT_CONFIG_VALUE_4='https://gitee.com/' \
git -c core.longpaths=true -c http.proxy=http://127.0.0.1:7897 push origin master
```

**注意**：oss-learning 根仓库 origin 是 `git@github.com:ihuangweiwei/oss-learning.git`（靠 KEY_0 转 https）；ai/java 是 https。push 前确认 `git status -sb` 不再 ahead 才算成功。

## 3. 官方页 / wiki / 流量

- 三个 GitHub Pages 站：oss-learning（总站，分支构建 docs/）、oss-learning-ai、oss-learning-java（Actions 工作流）。
- 每次有亮点增量（新框架、新蓝图、新应用），在官方页和 README 顶部同步"本周新增"，利于被搜索与传播。
- wiki 放"如何自维护"说明（承接本技能与 oss-learning-maintainer）。

## 4. 避坑

- **网络**：Clash 127.0.0.1:7897；改 URL 只在本脚本/会话内用 `GIT_CONFIG_COUNT=5` 环境块，**禁止改全局 insteadOf**。
- **Windows**：控制台别打印 emoji（GBK 报错）；深路径删除用 `cmd //c rmdir //s //q "\\\\?\\..."`。
- **GitHub Pages 与子模块**：Pages「Deploy from a branch」会**递归 checkout 子模块**——gitee SSH 直接构建失败；子模块太多（79/224 个）也超时/失败。**ai/java 的 Pages 必须用 GitHub Actions 工作流（`.github/workflows/pages.yml`，`submodules: false`）**；如遇设置项为 "Deploy from a branch"，让用户切到 "GitHub Actions"。
- **push 失败**：schannel SSL / access rights 报错多为瞬断，重试即可。
