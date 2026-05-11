# =========================================================
# 前端镜像：Vue3 构建 -> Nginx 静态托管 + /api 反向代理到后端
# =========================================================

# ---------- Stage 1: 构建静态资源 ----------
FROM node:20-alpine AS builder

WORKDIR /app

# 用国内镜像加速 npm
RUN npm config set registry https://registry.npmmirror.com

# 先装依赖
COPY package*.json ./
RUN npm install

# 再复制源码并构建
COPY . .
RUN npm run build

# ---------- Stage 2: Nginx 托管 ----------
FROM nginx:1.27-alpine

# 时区
RUN apk add --no-cache tzdata \
 && ln -snf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
 && echo "Asia/Shanghai" > /etc/timezone

# 自定义 Nginx 配置：托管 SPA + 反代 /api
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 构建产物
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
