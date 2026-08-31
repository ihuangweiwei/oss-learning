#!/bin/bash
# 扫描源目录，输出 raw-manifest.tsv: name<TAB>source_relpath(带来源前缀)<TAB>origin
set -u
OUT="$(dirname "$0")/raw-manifest.tsv"
: > "$OUT"
scan() {
  local base="$1"
  [ -d "$base" ] || return 0
  local prefix
  prefix="$(basename "$base")"
  ( cd "$base" || return
    while IFS= read -r g; do
      local dir name origin rel
      dir="$(dirname "$g")"
      name="$(basename "$dir")"
      origin="$(git -C "$dir" remote get-url origin 2>/dev/null || true)"
      rel="${dir#./}"
      printf '%s\t%s/%s\t%s\n' "$name" "$prefix" "$rel" "$origin" >> "$OUT"
    done < <(find . -name .git \( -type d -o -type f \))
  )
}
scan "/d/MyWorkSpace/learn"
scan "/d/MyWorkSpace/WorkSpace"
scan "/d/MyWorkSpace/spring-ai"
echo "扫描到仓库数: $(wc -l < "$OUT")"
echo "--- 按来源统计 ---"
awk -F'\t' '{split($2,a,"/"); print a[1]}' "$OUT" | sort | uniq -c
