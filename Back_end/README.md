# 资产管理平台 - 后端 (FastAPI + MySQL)

基于 FastAPI + SQLAlchemy 2.x + MySQL 的资产管理后端服务。

## 目录结构

```
Back_end/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI 应用入口
│   ├── config.py          # 配置（读取 .env）
│   ├── database.py        # 数据库连接与会话
│   ├── models.py          # ORM 模型（Asset）
│   ├── schemas.py         # Pydantic 请求/响应结构
│   ├── crud.py            # 数据库操作
│   └── routers/
│       └── assets.py      # 资产相关 API
├── requirements.txt
├── run.py                 # 本地启动脚本
├── init.sql               # 数据库初始化脚本
├── .env.example           # 环境变量示例
└── README.md
```

## 快速开始

### 1. 准备 MySQL

确保本地有 MySQL 8.x，执行 `init.sql` 创建数据库：

```sql
SOURCE init.sql;
```

或者手动执行：

```sql
CREATE DATABASE IF NOT EXISTS asset_management
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env`，根据本机 MySQL 调整账号密码：

```bash
copy .env.example .env
```

### 3. 安装依赖并启动

建议使用虚拟环境：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py
```

启动后访问：

- API 根路径：http://127.0.0.1:8000/
- Swagger 文档：http://127.0.0.1:8000/docs
- Redoc 文档：http://127.0.0.1:8000/redoc

## 主要 API

| 方法   | 路径                    | 说明           |
| ------ | ----------------------- | -------------- |
| GET    | `/api/assets`           | 资产分页查询   |
| GET    | `/api/assets/{id}`      | 资产详情       |
| POST   | `/api/assets`           | 新增资产       |
| PUT    | `/api/assets/{id}`      | 更新资产       |
| DELETE | `/api/assets/{id}`      | 删除资产       |

## 说明

- 启动时会通过 `Base.metadata.create_all` 自动建表，开发期使用方便。
- 生产环境建议引入 Alembic 进行数据库迁移管理。
- 默认开启了对前端 `http://localhost:5173` 的 CORS 放通。
