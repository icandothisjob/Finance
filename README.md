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

### 国内服务器无法访问 GitHub 时的镜像加速

国内云服务器（腾讯云 / 阿里云等）`git pull` 经常出现：

```
fatal: unable to access 'https://github.com/...': GnuTLS recv error (-110)
fatal: Failed to connect to github.com port 443 after 135545 ms: Couldn't connect to server
```

这是网络问题，不是代码问题。把 git remote 换成国内可访问的代理镜像即可：

```bash
cd ~/asset
git remote set-url origin https://ghfast.top/https://github.com/icandothisjob/Finance.git
./deploy.sh update
```

> 仓库地址：<https://github.com/icandothisjob/Finance.git>
> 当前可用镜像：`https://ghfast.top/`（前缀拼上完整 GitHub URL 即可）

如果 `ghfast.top` 哪天也失效了，可用如下命令测试其他镜像可用性：

```bash
curl -m 5 -sI https://ghproxy.com/ -o /dev/null -w "ghproxy: %{http_code}\n"
curl -m 5 -sI https://ghfast.top/ -o /dev/null -w "ghfast:  %{http_code}\n"
curl -m 5 -sI https://kkgithub.com/ -o /dev/null -w "kkgithub: %{http_code}\n"
curl -m 5 -sI https://bgithub.xyz/ -o /dev/null -w "bgithub: %{http_code}\n"
```

返回 `200` / `301` / `302` 即可用，`000` 表示不通。

- `ghproxy` 类型（拼接 GitHub URL）：`ghproxy.com`、`ghfast.top`、`gh-proxy.com`
  ```bash
  git remote set-url origin https://ghfast.top/https://github.com/icandothisjob/Finance.git
  ```
- 域名替换类型（直接换主域名）：`kkgithub.com`、`bgithub.xyz`
  ```bash
  git remote set-url origin https://kkgithub.com/icandothisjob/Finance.git
  ```

恢复原始 remote：

```bash
git remote set-url origin https://github.com/icandothisjob/Finance.git
```

### 兜底：网络完全不通时手动同步单个文件

若所有镜像都不通且只改了少量文件，可从本机 scp 直传：

```powershell
# 在本机 Windows PowerShell 中执行
cd e:\AAA_DAIL\资产管理平台
scp Front_end/nginx.conf ubuntu@1.14.63.96:~/asset/Front_end/nginx.conf
```

然后到服务器只重建对应容器：

```bash
cd ~/asset
docker compose up -d --build frontend
```

> 注意：直接 scp 会让 git 工作区处于"有未提交修改"状态，下次能连 GitHub 时用 `git stash && git pull && git stash pop` 同步。

## 后续可扩展方向

- 用户登录与权限管理（JWT）
- 资产领用 / 归还 / 调拨流程
- 资产盘点、报废申请审批
- 操作日志与数据导入导出（Excel）
- 更细致的分类字典管理
