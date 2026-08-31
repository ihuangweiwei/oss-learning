---
name: oss-introduce
description: 按 manifest 把新仓库引入为子模块，并同步计数/README。当你需要"引入这个仓库""加子模块""更新子模块数""新增框架到合集"时使用。产物：子模块落地 + 计数更新。网络约定：Clash 代理 + GIT_CONFIG_COUNT 环境块，禁止改全局 insteadOf。
---

# oss-introduce · 引入仓库 Skill

> 把选定的仓库按唯一事实源 `scripts/manifest.tsv` 引入 ai / java 子模块集合，并同步计数。
> 本技能承接 oss-learning-maintainer 维护循环的 Step 3–4。

## 1. 追加 manifest.tsv（唯一事实源）

格式：`super<TAB>category<TAB>name<TAB>origin`，origin 用 `https://github.com/...` 或 `git@gitee.com:...`。

```
ai<TAB>Agent<TAB>openworker<TAB>https://github.com/andrewyng/openworker.git
java<TAB>Middleware<TAB>xxl-job<TAB>https://github.com/xuxueli/xxl-job.git
```

分类归属参考 `docs/index.md` 的分类表（ai：Agent/RAG/MCP/Skills/Framework/Models/Platform/Applications…；java：Spring/Distributed/Middleware/BigData/Examples/Go…）。

## 2. 批量添加子模块

```bash
bash scripts/add-submodules.sh <super>   # super ∈ {ai, java}（跳过已注册 gitlink，3 次重试）
# 校验：
git -C <super> submodule status | grep '^-'   # 应无未初始化
```

## 3. 更新计数（README / docs）

- `java/README.md` / `ai/README.md`：`共 N 个子模块`；
- 根 `README.md` + `docs/index.md`：`~N 个（ai X + java Y）`；
- 若引入的是"能接单/变现"项目，顺手补进 README 的 Examples 亮点行与情报站快讯。

## 4. gitee 子模块迁移（历史参考）

`scripts/gitee-to-github.py` 按 `java/gitee-mapping.tsv` 解析 gitee 子模块到 GitHub 镜像（`git ls-remote` 验证存在才接受），无镜像标 DELETED。
2026-08-31 已完成：90 个换 GitHub、11 个废弃（java 235→224）。
**注意**：ls-remote 可能瞬断误判，DELETED 前对可疑项多试候选 owner（didi→didi、elunez→elunez、ityouknow→ityouknow、J2Cache→oschina）。

## 5. 网络约定（必须遵守）

- Clash 代理 `http://127.0.0.1:7897`；**不得改全局 `url.git@github.com:.insteadof`**；
- gitee 必须走 SSH（https 会挂）；每次 git 命令带 `-c core.longpaths=true`（Windows 深路径）；
- 批处理用 `GIT_CONFIG_COUNT=5` 环境块（github ssh→https、低带宽阈值、gitee https→ssh）。

## 6. 避坑

- 改名注意 gitlink 与 .gitmodules 同步；吸收/移动用 `git submodule absorbgitdirs`。
- Windows 无法 checkout 的仓库（文件名含 `:` `?` `|` 或尾随空格）已在 `build-manifest.sh` 排除，不要手工补。
