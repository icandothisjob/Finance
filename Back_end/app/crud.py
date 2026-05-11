"""资产 CRUD 操作。"""
import secrets
from datetime import datetime
from typing import Optional, Tuple

from fastapi import HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from . import asset_code as code_util
from . import models, schemas
from .config import get_settings


def _new_public_token() -> str:
    return secrets.token_urlsafe(16)


def list_assets(
    db: Session,
    page: int = 1,
    page_size: int = 10,
    keyword: Optional[str] = None,
    status: Optional[str] = None,
    category: Optional[str] = None,
    asset_class: Optional[str] = None,
) -> Tuple[int, list[models.Asset]]:
    stmt = select(models.Asset)
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(
            or_(
                models.Asset.asset_code.like(like),
                models.Asset.brand.like(like),
                models.Asset.model.like(like),
                models.Asset.serial_number.like(like),
                models.Asset.owner.like(like),
            )
        )
    if status:
        stmt = stmt.where(models.Asset.status == status)
    if category:
        stmt = stmt.where(models.Asset.category == category)
    if asset_class:
        stmt = stmt.where(models.Asset.asset_class == asset_class.upper())

    total = len(db.execute(stmt).scalars().all())
    stmt = (
        stmt.order_by(models.Asset.id.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    items = db.execute(stmt).scalars().all()
    return total, list(items)


def get_asset(db: Session, asset_id: int) -> Optional[models.Asset]:
    return db.get(models.Asset, asset_id)


def get_asset_by_code(db: Session, asset_code: str) -> Optional[models.Asset]:
    return db.execute(
        select(models.Asset).where(models.Asset.asset_code == asset_code)
    ).scalar_one_or_none()


def get_asset_by_public_token(
    db: Session, token: str
) -> Optional[models.Asset]:
    if not token:
        return None
    return db.execute(
        select(models.Asset).where(models.Asset.public_token == token)
    ).scalar_one_or_none()


def ensure_public_token(db: Session, asset: models.Asset) -> models.Asset:
    """如果资产没有 public_token 就生成一个并保存。"""
    if asset.public_token:
        return asset
    asset.public_token = _new_public_token()
    db.commit()
    db.refresh(asset)
    return asset


def regenerate_public_token(db: Session, asset: models.Asset) -> models.Asset:
    """强制刷新 public_token，使旧二维码失效。"""
    asset.public_token = _new_public_token()
    db.commit()
    db.refresh(asset)
    return asset


def create_asset(db: Session, payload: schemas.AssetCreate) -> models.Asset:
    settings = get_settings()
    data = payload.model_dump()

    asset_class = (data.get("asset_class") or "").upper().strip()
    if not asset_class:
        raise HTTPException(status_code=400, detail="资产大类不能为空")
    data["asset_class"] = asset_class

    code = (data.get("asset_code") or "").strip().upper()
    if not code:
        year = (
            data["purchase_date"].year
            if data.get("purchase_date")
            else datetime.now().year
        )
        code = code_util.generate_next_code(
            db, settings.org_code, asset_class, year
        )
    else:
        if not code_util.is_valid_code(code):
            raise HTTPException(
                status_code=400,
                detail="资产编号格式或校验位不正确，请使用「自动生成」或参照规则填写",
            )
        parsed = code_util.parse_code(code)
        if parsed and parsed["asset_class"] != asset_class:
            raise HTTPException(
                status_code=400,
                detail=f"资产编号中的大类({parsed['asset_class']})与所选大类({asset_class})不一致",
            )
    data["asset_code"] = code
    data["public_token"] = _new_public_token()

    asset = models.Asset(**data)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset


def update_asset(
    db: Session, asset: models.Asset, payload: schemas.AssetUpdate
) -> models.Asset:
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(asset, key, value)
    db.commit()
    db.refresh(asset)
    return asset


def delete_asset(db: Session, asset: models.Asset) -> None:
    db.delete(asset)
    db.commit()


def list_asset_files(db: Session, asset_id: int) -> list[models.AssetFile]:
    stmt = (
        select(models.AssetFile)
        .where(models.AssetFile.asset_id == asset_id)
        .order_by(models.AssetFile.id.desc())
    )
    return list(db.execute(stmt).scalars().all())


def get_asset_file(db: Session, file_id: int) -> Optional[models.AssetFile]:
    return db.get(models.AssetFile, file_id)


def create_asset_file(
    db: Session,
    *,
    asset_id: int,
    filename: str,
    object_key: str,
    file_url: str,
    content_type: Optional[str],
    size: int,
    uploader: Optional[str],
) -> models.AssetFile:
    record = models.AssetFile(
        asset_id=asset_id,
        filename=filename,
        object_key=object_key,
        file_url=file_url,
        content_type=content_type,
        size=size,
        uploader=uploader,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def delete_asset_file(db: Session, record: models.AssetFile) -> None:
    db.delete(record)
    db.commit()
