#!/bin/bash
# 用法: add-submodules.sh <super: ai|java> [category过滤器]
# 逐个 git submodule add；每个尝试最多 3 次，失败自动清理重试
#
# 网络要点：
#   - GitHub：全局只有 https→ssh 的 insteadOf，且 git clone 只读全局 config，会让 ssh URL 直连（绕代理、被限速）。
#     这里通过 GIT_CONFIG_COUNT/KEY/VALUE 注入反向 ssh→https 规则（仅本批次进程生效，不改全局），
#     使 GitHub clone 走 https 并经 http.proxy(Clash 127.0.0.1:7897)。
#   - Gitee：国内直连即可，SSH 不走 http.proxy，天然绕过代理；不注入 gitee 反向规则。
#   - 用 git 自带 http.lowSpeedLimit/Time + connectTimeout 让 git 自己干净中止慢/卡传输，
#     避免 `timeout` 杀父进程后孙进程(git-remote-https)变孤儿。
#   - core.longpaths 用 `git -c core.longpaths=true submodule add` 传入（-c 经 GIT_CONFIG_PARAMETERS
#     传播到内部 clone 的 checkout 阶段）。注意：GIT_CONFIG_COUNT env 注入的 longpaths 虽能被 git 读到，
#     但对 clone checkout 无效（实测），所以 env 里不注入它。add 成功后也写入子模块本地 config 兜底。
#   - .gitmodules 记录原始 ssh URL；github 子模块本地 config 写入反向规则，保证以后 fetch 走代理。
#
# 健壮性：
#   - mkdir 锁，防止两个批次并发操作同一仓库。
#   - submodule add 加 -f，兜底"git directory already exists"场景。
#   - 清理时删除工作目录和 .git/modules/<target>，并杀掉可能的残留下载子进程。
set -u
SUPER="$1"; FILTER="${2:-}"
ROOT="/d/MyWorkSpace/oss-learning"
MAN="$ROOT/scripts/manifest.tsv"
LOG="$ROOT/scripts/add-$SUPER.log"
cd "$ROOT/$SUPER" || exit 1

# 注入本批次配置（env，仅对批次进程及子进程生效）：
#   0) GitHub ssh→https（经代理）
#   1) 传输 <1000B/s 持续 60s → git 自中止（干净，无孤儿）
#   2) 连接阶段 30s 无响应 → git 自中止
#   3) Gitee https→ssh（强制直连。manifest 若记录了 https origin，经 http.proxy 会卡死）
#   (core.longpaths 不用 env 注入——实测对 clone checkout 无效，改用 `git -c` 传参，见 add_one)
export GIT_CONFIG_COUNT=5
export GIT_CONFIG_KEY_0='url.https://github.com/.insteadOf'
export GIT_CONFIG_VALUE_0='git@github.com:'
export GIT_CONFIG_KEY_1='http.lowSpeedLimit'
export GIT_CONFIG_VALUE_1='1000'
export GIT_CONFIG_KEY_2='http.lowSpeedTime'
export GIT_CONFIG_VALUE_2='60'
export GIT_CONFIG_KEY_3='http.connectTimeout'
export GIT_CONFIG_VALUE_3='30'
export GIT_CONFIG_KEY_4='url.git@gitee.com:.insteadOf'
export GIT_CONFIG_VALUE_4='https://gitee.com/'

# 并发锁
LOCK="$ROOT/scripts/.lock-$SUPER"
if ! mkdir "$LOCK" 2>/dev/null; then
  echo "[$(date +%T)] 已有批次在运行（$LOCK），退出" | tee -a "$LOG"
  exit 1
fi
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

JOBS="/tmp/jobs-$$-$SUPER.txt"
awk -F'\t' -v s="$SUPER" -v f="$FILTER" '$1==s && (f=="" || $2==f) {print $2"\t"$3"\t"$4}' "$MAN" > "$JOBS"
echo "[$(date +%T)] 本批 $(wc -l < "$JOBS") 个: $SUPER/${FILTER:-all}" | tee -a "$LOG"

# 杀掉残留的下载子进程，避免文件被锁导致 rm 失败（用中括号防误匹配）
kill_leftover() {
  pkill -9 -f 'git-remot[e]-https' 2>/dev/null
  pkill -9 -f 'git-remot[e]-http'  2>/dev/null
  pkill -9 -f 'index-[p]ack'       2>/dev/null
  pkill -9 -f 'git-upload-[p]ack'  2>/dev/null
  sleep 1
}

cleanup_target() {
  git submodule deinit -f -- "$1" 2>/dev/null
  git rm -q --cached "$1" 2>/dev/null
  kill_leftover
  # 常规删除；深路径(>260字符)删不掉的用 Windows 长路径 rmdir 兜底
  rm -rf "$1" ".git/modules/$1" 2>/dev/null
  local w1 w2
  w1="$(cygpath -w "$1" 2>/dev/null)";   [ -n "$w1" ] && cmd //c rmdir //s //q "\\\\?\\$w1" >/dev/null 2>&1
  w2="$(cygpath -w ".git/modules/$1" 2>/dev/null)"; [ -n "$w2" ] && cmd //c rmdir //s //q "\\\\?\\$w2" >/dev/null 2>&1
}

add_one() {
  local cat="$1" name="$2" origin="$3" try=0
  local target="$cat/$name"
  # 已注册且工作树存在 → 直接跳过（重跑时之前成功的）
  if git ls-files --error-unmatch "$target" >/dev/null 2>&1 && { [ -d "$target/.git" ] || [ -f "$target/.git" ]; }; then
    echo "  [已有] $target 已注册，跳过" | tee -a "$LOG"
    return 0
  fi
  # 未注册但存在残留（上次失败的深路径/半克隆）→ 先清掉，避免 add 撞残留
  if [ -e "$target" ] || [ -e ".git/modules/$target" ]; then
    cleanup_target "$target"
  fi
  while [ $try -lt 3 ]; do
    try=$((try+1))
    # -c core.longpaths=true：传播到内部 clone 的 checkout，绕开 Windows MAX_PATH 深路径问题
    if git -c core.longpaths=true submodule add -f "$origin" "$target" >> "$LOG" 2>&1; then
      # 写入子模块本地 config：a) 深路径兜底 b) GitHub 反向规则（手动 update 也走代理）
      git -C "$target" config core.longpaths true 2>/dev/null
      git -C "$target" config url.https://github.com/.insteadOf git@github.com: 2>/dev/null
      echo "  [ok] $target" | tee -a "$LOG"
      return 0
    fi
    echo "  [..] $target 第${try}次失败，清理重试" | tee -a "$LOG"
    cleanup_target "$target"
    sleep 3
  done
  echo "  [!!] 放弃 $target origin=$origin" | tee -a "$LOG"
  return 1
}

ok=0; fail=0
while IFS=$'\t' read -r cat name origin; do
  if add_one "$cat" "$name" "$origin"; then ok=$((ok+1)); else fail=$((fail+1)); fi
done < "$JOBS"
rm -f "$JOBS"
echo "[$(date +%T)] 完成: 成功 $ok 失败 $fail" | tee -a "$LOG"
