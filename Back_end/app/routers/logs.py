"""消息中心：操作日志查询接口。"""
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from .. import activity, models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/api/logs",
    tags=["消息中心"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "",
    response_model=schemas.ActivityLogListOut,
    summary="查询操作日志（消息中心）",
)
def list_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    scope: str = Query("all", description="all=全员视图 / mine=仅自己"),
    keyword: Optional[str] = Query(None, description="按摘要/对象/操作人模糊搜索"),
    action: Optional[str] = Query(None, description="按动作过滤"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    total, unread, items = activity.list_logs(
        db,
        page=page,
        page_size=page_size,
        scope=scope,
        current_user=current_user,
        keyword=keyword,
        action=action,
    )
    return {"total": total, "unread": unread, "items": items}


@router.get(
    "/unread-count",
    response_model=schemas.UnreadCountOut,
    summary="获取当前用户未读消息数",
)
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    return {"unread": activity.unread_count(db, current_user)}


@router.post(
    "/mark-read",
    response_model=schemas.UnreadCountOut,
    summary="标记消息已读（不传 ids 则全部已读）",
)
def mark_logs_read(
    payload: schemas.MarkReadIn,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    activity.mark_read(db, current_user, payload.ids)
    return {"unread": activity.unread_count(db, current_user)}
