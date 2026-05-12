"""操作日志（消息中心）服务。

负责：
1. 记录每一次用户操作（登录、资产 CRUD、附件、二维码刷新等）
2. 计算字段 diff，用于"修改了哪些字段"详情展示
3. 提供查询与已读标记
"""
from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Iterable, Optional

from fastapi import Request
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from . import models


# 资产字段中文名映射（用于 diff 展示）
ASSET_FIELD_LABELS: dict[str, str] = {
    "asset_code": "资产编号",
    "asset_class": "大类",
    "category": "分类",
    "brand": "品牌",
    "model": "型号",
    "serial_number": "SN",
    "specification": "规格",
    "purchase_date": "购置日期",
    "supplier": "供应商",
    "price": "金额",
    "warranty_until": "保修至",
    "location": "存放位置",
    "owner": "使用人",
    "department": "部门",
    "status": "状态",
    "remark": "备注",
}


# 动作代码 -> 中文名（用于摘要兜底）
ACTION_LABELS: dict[str, str] = {
    "login": "登录系统",
    "logout": "退出登录",
    "asset.create": "新增资产",
    "asset.update": "修改资产",
    "asset.delete": "删除资产",
    "asset.import": "批量导入资产",
    "asset.qr.regen": "刷新二维码",
    "file.upload": "上传附件",
    "file.delete": "删除附件",
}


def _client_ip(request: Optional[Request]) -> Optional[str]:
    if request is None:
        return None
    fwd = request.headers.get("x-forwarded-for")
    if fwd:
        return fwd.split(",")[0].strip()
    if request.client:
        return request.client.host
    return None


def _to_display(value: Any) -> Optional[str]:
    """把任意值转为可读字符串，用于 diff 展示。"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")
    if isinstance(value, bool):
        return "是" if value else "否"
    if isinstance(value, float):
        if value.is_integer():
            return str(int(value))
        return f"{value:.2f}"
    return str(value)


def diff_asset(
    before: dict[str, Any], after: dict[str, Any]
) -> list[dict[str, Optional[str]]]:
    """生成资产更新前后的字段差异（仅包含真正变化的字段）。"""
    changes: list[dict[str, Optional[str]]] = []
    for field, label in ASSET_FIELD_LABELS.items():
        b = before.get(field)
        a = after.get(field)
        if b == a:
            continue
        # 浮点 / Decimal 等比较容差
        try:
            if b is not None and a is not None and float(b) == float(a):
                continue
        except (TypeError, ValueError):
            pass
        changes.append(
            {
                "field": field,
                "label": label,
                "before": _to_display(b),
                "after": _to_display(a),
            }
        )
    return changes


def asset_to_dict(asset: models.Asset) -> dict[str, Any]:
    return {f: getattr(asset, f, None) for f in ASSET_FIELD_LABELS}


def log(
    db: Session,
    *,
    action: str,
    actor: Optional[models.User] = None,
    target_type: Optional[str] = None,
    target_id: Optional[int] = None,
    target_label: Optional[str] = None,
    summary: Optional[str] = None,
    changes: Optional[list[dict[str, Any]]] = None,
    extra: Optional[dict[str, Any]] = None,
    request: Optional[Request] = None,
) -> models.ActivityLog:
    """写入一条操作日志。"""
    if not summary:
        action_zh = ACTION_LABELS.get(action, action)
        if target_label:
            summary = f"{action_zh} {target_label}"
        else:
            summary = action_zh

    detail_payload: dict[str, Any] = {}
    if changes:
        detail_payload["changes"] = changes
    if extra:
        detail_payload["extra"] = extra
    detail_str = json.dumps(detail_payload, ensure_ascii=False) if detail_payload else None

    record = models.ActivityLog(
        actor=actor.username if actor else None,
        actor_nickname=(actor.nickname if actor else None) or (actor.username if actor else None),
        action=action,
        target_type=target_type,
        target_id=target_id,
        target_label=target_label,
        summary=summary,
        detail=detail_str,
        ip=_client_ip(request),
        is_read=False,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def _serialize(
    log_row: models.ActivityLog, read_username: Optional[str] = None,
    read_ids: Optional[set[int]] = None,
) -> dict[str, Any]:
    changes: list[dict[str, Any]] = []
    if log_row.detail:
        try:
            payload = json.loads(log_row.detail)
            changes = payload.get("changes") or []
        except (ValueError, TypeError):
            changes = []
    is_read = log_row.is_read
    if read_ids is not None:
        is_read = log_row.id in read_ids
    return {
        "id": log_row.id,
        "actor": log_row.actor,
        "actor_nickname": log_row.actor_nickname,
        "action": log_row.action,
        "target_type": log_row.target_type,
        "target_id": log_row.target_id,
        "target_label": log_row.target_label,
        "summary": log_row.summary,
        "changes": changes,
        "ip": log_row.ip,
        "is_read": is_read,
        "created_at": log_row.created_at,
    }


def list_logs(
    db: Session,
    *,
    page: int = 1,
    page_size: int = 20,
    scope: str = "all",
    current_user: Optional[models.User] = None,
    keyword: Optional[str] = None,
    action: Optional[str] = None,
) -> tuple[int, int, list[dict[str, Any]]]:
    """查询日志列表。

    scope=all  -> 所有用户的操作（共享视图）
    scope=mine -> 仅当前用户自己的操作

    返回 (total, unread_count_for_current_user, items)
    """
    stmt = select(models.ActivityLog)
    if scope == "mine" and current_user:
        stmt = stmt.where(models.ActivityLog.actor == current_user.username)
    if action:
        stmt = stmt.where(models.ActivityLog.action == action)
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(
            or_(
                models.ActivityLog.summary.like(like),
                models.ActivityLog.target_label.like(like),
                models.ActivityLog.actor.like(like),
                models.ActivityLog.actor_nickname.like(like),
            )
        )

    total = db.execute(
        select(func.count()).select_from(stmt.subquery())
    ).scalar_one()

    page_stmt = (
        stmt.order_by(models.ActivityLog.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    rows = list(db.execute(page_stmt).scalars().all())

    # 当前用户的已读 ID
    read_ids: set[int] = set()
    if current_user and rows:
        ids = [r.id for r in rows]
        read_ids = set(
            db.execute(
                select(models.ActivityLogRead.log_id).where(
                    and_(
                        models.ActivityLogRead.username == current_user.username,
                        models.ActivityLogRead.log_id.in_(ids),
                    )
                )
            ).scalars()
        )

    items = [_serialize(r, read_ids=read_ids) for r in rows]

    unread = unread_count(db, current_user) if current_user else 0
    return total, unread, items


def unread_count(db: Session, current_user: Optional[models.User]) -> int:
    """计算当前用户的未读消息数。

    口径：用户账号创建之后产生的日志中，未在 ActivityLogRead 表标记为已读的条数。
    （避免新建账号一登录就显示几百条历史"未读"。）
    """
    if not current_user:
        return 0
    baseline = current_user.created_at
    visible_stmt = select(models.ActivityLog.id)
    if baseline is not None:
        visible_stmt = visible_stmt.where(models.ActivityLog.created_at >= baseline)
    visible_total = db.execute(
        select(func.count()).select_from(visible_stmt.subquery())
    ).scalar_one()

    read_stmt = select(models.ActivityLogRead.log_id).where(
        models.ActivityLogRead.username == current_user.username
    )
    if baseline is not None:
        read_stmt = read_stmt.join(
            models.ActivityLog,
            models.ActivityLog.id == models.ActivityLogRead.log_id,
        ).where(models.ActivityLog.created_at >= baseline)
    read = db.execute(
        select(func.count()).select_from(read_stmt.subquery())
    ).scalar_one()
    return max(int(visible_total) - int(read), 0)


def mark_read(
    db: Session, current_user: models.User, ids: Optional[Iterable[int]] = None
) -> int:
    """把指定 ID（或全部）日志标记为当前用户已读。返回新增已读条数。"""
    if not current_user:
        return 0

    if ids is None:
        target_ids = list(
            db.execute(select(models.ActivityLog.id)).scalars()
        )
    else:
        target_ids = list({int(i) for i in ids})
    if not target_ids:
        return 0

    already = set(
        db.execute(
            select(models.ActivityLogRead.log_id).where(
                and_(
                    models.ActivityLogRead.username == current_user.username,
                    models.ActivityLogRead.log_id.in_(target_ids),
                )
            )
        ).scalars()
    )
    new_ids = [i for i in target_ids if i not in already]
    if not new_ids:
        return 0
    db.add_all(
        [
            models.ActivityLogRead(log_id=i, username=current_user.username)
            for i in new_ids
        ]
    )
    db.commit()
    return len(new_ids)
