#!/usr/bin/env bash
# =========================================================
# 服务器一键部署/更新脚本
# 用法：
#   首次：  ./deploy.sh            # 拉代码（如已在仓库内）+ 构建 + 启动
#   更新：  ./deploy.sh update     # git pull + 重新构建 + 重启
#   日志：  ./deploy.sh logs
#   停止：  ./deploy.sh down
# =========================================================
set -euo pipefail

cd "$(dirname "$0")"

ACTION="${1:-up}"

if [ ! -f .env ]; then
    echo "[!] 未找到 .env，正在从 .env.deploy.example 复制..."
    cp .env.deploy.example .env
    echo "[!] 请先编辑 .env 后再运行本脚本！"
    exit 1
fi

case "$ACTION" in
    up)
        docker compose up -d --build
        echo
        docker compose ps
        ;;
    update)
        git pull
        docker compose up -d --build
        echo
        docker compose ps
        ;;
    logs)
        docker compose logs -f --tail=200
        ;;
    down)
        docker compose down
        ;;
    restart)
        docker compose restart
        ;;
    *)
        echo "用法：$0 [up|update|logs|down|restart]"
        exit 1
        ;;
esac
