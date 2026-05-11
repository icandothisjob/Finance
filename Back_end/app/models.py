"""ORM 模型定义。"""
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    """系统登录用户。"""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, comment="登录账号"
    )
    password_hash: Mapped[str] = mapped_column(String(255), comment="bcrypt 密码哈希")
    nickname: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="昵称"
    )
    is_active: Mapped[bool] = mapped_column(default=True, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )


class Asset(Base):
    """企业资产。"""

    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_code: Mapped[str] = mapped_column(
        String(64), unique=True, index=True,
        comment="资产编号，例如 DG-IT-2026-000123-X",
    )
    public_token: Mapped[str | None] = mapped_column(
        String(48), unique=True, index=True, nullable=True,
        comment="公开访问 token，用于二维码 URL",
    )
    asset_class: Mapped[str] = mapped_column(
        String(8), index=True, comment="资产大类代码，例如 IT/OF/VH",
    )
    category: Mapped[str] = mapped_column(
        String(64), index=True, comment="资产分类，例如 笔记本电脑/显示器/办公家具"
    )
    brand: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True, comment="品牌"
    )
    model: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="型号"
    )
    serial_number: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True, comment="SN / 序列号"
    )
    specification: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="规格配置，例如 R7-7840U/16GB/512GB"
    )
    purchase_date: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="购置日期"
    )
    supplier: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="供应商/采购渠道"
    )
    price: Mapped[float | None] = mapped_column(
        Numeric(12, 2), nullable=True, comment="采购金额"
    )
    warranty_until: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, comment="保修到期日期"
    )
    location: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="存放位置"
    )
    owner: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True, comment="使用人"
    )
    department: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="所属部门"
    )
    status: Mapped[str] = mapped_column(
        String(32), default="在用", index=True,
        comment="状态：在用/闲置/维修/报废",
    )
    remark: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="备注"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="创建时间"
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="更新时间",
    )


class AssetFile(Base):
    """资产关联的附件（存储于腾讯云 COS）。"""

    __tablename__ = "asset_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("assets.id", ondelete="CASCADE"),
        index=True,
        comment="所属资产 ID",
    )
    filename: Mapped[str] = mapped_column(
        String(255), comment="原始文件名（含扩展名）"
    )
    object_key: Mapped[str] = mapped_column(
        String(512), unique=True, comment="COS 对象 Key"
    )
    file_url: Mapped[str] = mapped_column(
        String(1024), comment="COS 公开访问 URL"
    )
    content_type: Mapped[str | None] = mapped_column(
        String(128), nullable=True, comment="MIME 类型"
    )
    size: Mapped[int] = mapped_column(
        BigInteger, default=0, comment="文件大小（字节）"
    )
    uploader: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="上传人用户名"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), comment="上传时间"
    )


class ActivityLog(Base):
    """系统操作日志（消息中心数据源）。

    每一条记录代表一次"用户对系统做了什么"，例如：
    - 登录 / 登出
    - 新增 / 修改 / 删除 资产
    - 上传 / 删除 资产附件
    - 刷新二维码 token
    """

    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    actor: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True, comment="操作人用户名"
    )
    actor_nickname: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="操作人昵称（冗余，便于展示）"
    )
    action: Mapped[str] = mapped_column(
        String(32), index=True,
        comment="动作代码：login/logout/asset.create/asset.update/asset.delete/"
                "asset.qr.regen/file.upload/file.delete",
    )
    target_type: Mapped[str | None] = mapped_column(
        String(32), nullable=True, index=True,
        comment="目标类型：asset/file/auth",
    )
    target_id: Mapped[int | None] = mapped_column(
        Integer, nullable=True, index=True, comment="目标对象的数据库 ID"
    )
    target_label: Mapped[str | None] = mapped_column(
        String(255), nullable=True, comment="目标对象的可读名称（如资产编号、文件名）"
    )
    summary: Mapped[str] = mapped_column(
        String(255), comment="一句话摘要，用于列表展示"
    )
    detail: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="JSON 字符串，详细信息：字段变更 diff、上下文等",
    )
    ip: Mapped[str | None] = mapped_column(
        String(64), nullable=True, comment="操作时的客户端 IP"
    )
    is_read: Mapped[bool] = mapped_column(
        Boolean, default=False, index=True,
        comment="是否已读（针对全员消息，未读用于红点提醒）",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), index=True, comment="发生时间"
    )


class ActivityLogRead(Base):
    """单个用户对消息的已读标记（per-user read state）。"""

    __tablename__ = "activity_log_reads"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    log_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("activity_logs.id", ondelete="CASCADE"),
        index=True,
    )
    username: Mapped[str] = mapped_column(String(64), index=True)
    read_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
