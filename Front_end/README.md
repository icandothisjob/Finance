# 资产管理平台 - 前端 (Vue 3 + Vite + Element Plus)

## 目录结构

```
Front_end/
├── index.html
├── package.json
├── vite.config.js
├── public/
│   └── favicon.svg
└── src/
    ├── main.js
    ├── App.vue
    ├── styles/main.css
    ├── router/index.js
    ├── api/
    │   ├── request.js     # axios 实例 + 全局错误处理
    │   └── assets.js      # 资产相关 API
    ├── layouts/
    │   └── MainLayout.vue # 侧边栏 + 顶部导航布局
    └── views/
        ├── Dashboard.vue  # 概览页（统计卡片）
        ├── Assets.vue     # 资产管理页（增删改查）
        └── NotFound.vue   # 404
```

## 快速开始

```powershell
cd Front_end
npm install
npm run dev
```

启动后访问 http://localhost:5173

## 与后端联调

`vite.config.js` 中已配置代理：所有以 `/api` 开头的请求会被转发到 `http://127.0.0.1:8000`。

请确保后端服务已经启动（默认端口 8000）。

## 构建

```powershell
npm run build
```

产物输出在 `dist/` 目录。
