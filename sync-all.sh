#!/bin/bash
# 一键同步 ai 与 java 两个超级项目的所有子模块
set -e
echo "=== 同步 ai ==="
(cd "$(dirname "$0")/ai" && ./sync.sh)
echo "=== 同步 java ==="
(cd "$(dirname "$0")/java" && ./sync.sh)
