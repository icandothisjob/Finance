"""FastAPI 应用入口。"""
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from .config import get_settings
from .database import Base, SessionLocal, engine
from .routers import assets, auth, logs, public
from . import models
from .security import hash_password

settings = get_settings()

app = FastAPI(
    title="企业资产管理平台",
    description="基于 FastAPI + MySQL 的资产管理后端服务",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _check_db_or_exit() -> None:
    """启动前测一次数据库连通，失败时给出人话提示并退出。"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except OperationalError as e:
        msg = str(e.orig) if getattr(e, "orig", None) else str(e)
        print("\n" + "=" * 60, flush=True)
        print("[X] 无法连接 MySQL，请检查 Back_end/.env 中的账号密码/主机端口", flush=True)
        print(f"    当前配置: user={settings.mysql_user} "
              f"host={settings.mysql_host}:{settings.mysql_port} "
              f"database={settings.mysql_database}", flush=True)
        print(f"    MySQL 返回: {msg}", flush=True)
        print("=" * 60 + "\n", flush=True)
        sys.exit(1)


def _migrate_assets_table_if_needed() -> None:
    """开发期辅助：根据 assets 表与模型差异自动迁移。
    - 仅缺少「可空」新字段：ALTER ADD COLUMN（不丢数据）
    - 其他差异（字段不可空 / 多余字段 / 类型变化）：DROP 重建
    生产环境请改用 Alembic。
    """
    from sqlalchemy.schema import CreateColumn

    inspector = inspect(engine)
    if not inspector.has_table("assets"):
        return

    existing_cols = {c["name"] for c in inspector.get_columns("assets")}
    expected = {c.name: c for c in models.Asset.__table__.columns}
    missing = set(expected.keys()) - existing_cols
    obsolete = existing_cols - set(expected.keys())

    if not missing and not obsolete:
        return

    can_alter = (
        not obsolete
        and missing
        and all(expected[m].nullable for m in missing)
    )
    if can_alter:
        with engine.begin() as conn:
            for name in missing:
                col = expected[name]
                ddl = str(CreateColumn(col).compile(dialect=engine.dialect))
                conn.execute(text(f"ALTER TABLE assets ADD COLUMN {ddl}"))
        print(
            f"[migrate] 已为 assets 安全添加新字段: {missing}（数据保留）",
            flush=True,
        )
        return

    print(
        f"[migrate] assets 表结构差异较大 (缺少: {missing or '无'}, "
        f"多余: {obsolete or '无'})，将 DROP 重建（数据将清空）。",
        flush=True,
    )
    models.Asset.__table__.drop(bind=engine)


DEFAULT_ADMINS: list[tuple[str, str, str]] = [
    # (username, password, nickname)
    ("xingzheng", "xingzheng888", "超级管理员"),
]


def _ensure_default_admin() -> None:
    """确保超级管理员账号存在：
    - 主管理员（settings.default_admin_username）若不存在则创建，且支持从旧 admin 一次性迁移
    - DEFAULT_ADMINS 列表中的其他超级管理员，仅在不存在时创建（已存在不修改，避免覆盖手动改过的密码）
    """
    db = SessionLocal()
    try:
        primary_username = settings.default_admin_username
        primary_password = settings.default_admin_password
        existing = (
            db.query(models.User)
            .filter(models.User.username == primary_username)
            .first()
        )
        if not existing:
            legacy = (
                db.query(models.User)
                .filter(models.User.username == "admin")
                .first()
            )
            if legacy and primary_username != "admin":
                legacy.username = primary_username
                legacy.password_hash = hash_password(primary_password)
                legacy.nickname = "超级管理员"
                legacy.is_active = True
                db.commit()
                print(
                    f"[init] 已将旧管理员账号 admin 迁移为: {primary_username} / {primary_password}",
                    flush=True,
                )
            else:
                db.add(
                    models.User(
                        username=primary_username,
                        password_hash=hash_password(primary_password),
                        nickname="超级管理员",
                        is_active=True,
                    )
                )
                db.commit()
                print(
                    f"[init] 已创建默认管理员账号: {primary_username} / {primary_password}",
                    flush=True,
                )

        # 其他内置超级管理员账号：仅在不存在时创建
        for username, password, nickname in DEFAULT_ADMINS:
            if not username or username == primary_username:
                continue
            exists = (
                db.query(models.User)
                .filter(models.User.username == username)
                .first()
            )
            if exists:
                continue
            db.add(
                models.User(
                    username=username,
                    password_hash=hash_password(password),
                    nickname=nickname or "超级管理员",
                    is_active=True,
                )
            )
            db.commit()
            print(
                f"[init] 已创建超级管理员账号: {username} / {password}",
                flush=True,
            )
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    """启动时自动建表（开发期方便，生产建议用 Alembic 迁移）。"""
    _check_db_or_exit()
    _migrate_assets_table_if_needed()
    Base.metadata.create_all(bind=engine)
    _ensure_default_admin()


@app.get("/", tags=["健康检查"], summary="服务存活检查")
def root():
    return {"app": "asset-management", "status": "ok"}


app.include_router(auth.router)
app.include_router(assets.router)
app.include_router(logs.router)
app.include_router(public.router)
