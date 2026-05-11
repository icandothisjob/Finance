"""认证相关路由。"""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from .. import activity, models, schemas
from ..database import get_db
from ..security import (
    create_access_token,
    get_current_user,
    verify_password,
)

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login", response_model=schemas.TokenOut, summary="账号密码登录")
def login(payload: schemas.LoginIn, request: Request, db: Session = Depends(get_db)):
    user = (
        db.query(models.User)
        .filter(models.User.username == payload.username)
        .first()
    )
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号或密码错误",
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="账号已被禁用"
        )
    token, expires_in = create_access_token(subject=user.username)
    activity.log(
        db,
        action="login",
        actor=user,
        target_type="auth",
        target_id=user.id,
        target_label=user.username,
        summary=f"{user.username} 登录系统",
        request=request,
    )
    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": expires_in,
        "user": user,
    }


@router.get("/me", response_model=schemas.UserOut, summary="获取当前登录用户")
def me(current: models.User = Depends(get_current_user)):
    return current


@router.post("/logout", summary="退出登录（仅记录日志，前端清理 token 即可）")
def logout(
    request: Request,
    db: Session = Depends(get_db),
    current: models.User = Depends(get_current_user),
):
    activity.log(
        db,
        action="logout",
        actor=current,
        target_type="auth",
        target_id=current.id,
        target_label=current.username,
        summary=f"{current.username} 退出登录",
        request=request,
    )
    return {"ok": True}
