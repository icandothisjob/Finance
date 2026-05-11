# 企业资产管理平台

一个用于统一管理企业内资产的极简平台。前端 Vue 3，后端 FastAPI，数据库 MySQL。

```
资产管理平台/
├── Back_end/    # FastAPI + SQLAlchemy + MySQL
├── Front_end/   # Vue 3 + Vite + Element Plus
└── README.md
```

## 技术栈

| 层级   | 技术                                                                |
| ------ | ------------------------------------------------------------------- |
| 前端   | Vue 3、Vite、Vue Router、Pinia、Element Plus、Axios                 |
| 后端   | FastAPI、SQLAlchemy 2.x、Pydantic v2、PyMySQL、Uvicorn              |
| 数据库 | MySQL 8.x                                                           |

## 一键启动（开发环境）

### 1. 准备 MySQL

确保本地 MySQL 已运行，执行：

```sql
CREATE DATABASE IF NOT EXISTS asset_management
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 2. 一键启动前后端

在项目根目录直接双击 `start.bat`，或在 PowerShell 中执行：

```powershell
.\start.ps1
```

脚本会自动完成：

- 检查 Python / Node 环境
- 后端：创建 `.venv`、安装依赖、复制 `.env`
- 前端：执行 `npm install`（首次较慢）
- 分别在两个新窗口启动后端（8000）和前端（5173）

启动完成后访问：

- 前端页面：<http://localhost:5173>
- 接口文档：<http://127.0.0.1:8000/docs>

### 3. 一键停止

```powershell
.\stop.ps1
```

或者直接关掉两个新弹出的 PowerShell 窗口即可。

> 首次运行如提示 `.env` 已生成，请按需修改 `Back_end\.env` 中的 MySQL 账号密码后重新启动。

### 手动启动（可选）

如果不想用脚本，也可以分别在两个终端执行：

```powershell
# 后端
cd Back_end
copy .env.example .env
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py

# 前端
cd Front_end
npm install
npm run dev
```

## 已实现功能

- 资产 CRUD：新增 / 编辑 / 删除 / 分页查询
- 多条件搜索（关键词、状态）
- 概览页：总数、在用、闲置、维修中统计
- 侧边栏 + 顶部导航的后台布局
- Swagger / Redoc 自动 API 文档

## 生产部署（Docker Compose）

服务器（Ubuntu / CentOS 等 Linux）只需装好 Docker，然后：

```bash
git clone <你的仓库地址> asset
cd asset
cp .env.deploy.example .env
vim .env                       # 修改密码、域名、COS 等
chmod +x deploy.sh
./deploy.sh                    # 首次：构建并启动
```

浏览器访问 `http://服务器IP` 即可。常用命令：

```bash
./deploy.sh update    # git pull 后重建并重启
./deploy.sh logs      # 查看实时日志
./deploy.sh down      # 停止全部服务
```

数据库数据持久化在 `./mysql_data/` 目录，删除该目录会清空所有数据。

## 后续可扩展方向

- 用户登录与权限管理（JWT）
- 资产领用 / 归还 / 调拨流程
- 资产盘点、报废申请审批
- 操作日志与数据导入导出（Excel）
- 更细致的分类字典管理
