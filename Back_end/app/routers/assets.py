"""资产管理 API 路由。"""
import json
import logging
import re
import traceback
import uuid
from datetime import datetime
from typing import List, Optional

logger = logging.getLogger(__name__)

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    Request,
    UploadFile,
    status,
)
from fastapi.responses import Response
from sqlalchemy.orm import Session

from .. import activity
from .. import asset_code as code_util
from .. import cos_client, crud, excel_import, models, schemas
from ..config import get_settings
from ..database import get_db
from ..llm_client import LLMUnavailable, is_configured as llm_is_configured
from ..qrcode_util import make_qr_png
from ..security import get_current_user

router = APIRouter(
    prefix="/api/assets",
    tags=["资产管理"],
    dependencies=[Depends(get_current_user)],
)


_SAFE_NAME_RE = re.compile(r"[\\/:*?\"<>|\x00-\x1f]")


def _safe_filename(name: str) -> str:
    """清洗文件名：去掉路径分隔符与控制字符，保留中文/字母/数字/常见符号。"""
    name = (name or "file").strip().replace("\\", "/").split("/")[-1]
    name = _SAFE_NAME_RE.sub("_", name)
    return name[:200] or "file"


@router.get(
    "/dict/classes",
    response_model=List[schemas.AssetClassDictItem],
    summary="资产大类字典",
)
def list_asset_classes():
    return code_util.ASSET_CLASSES


@router.get(
    "/next-code",
    response_model=schemas.NextCodeOut,
    summary="预览下一个资产编号",
)
def next_asset_code(
    asset_class: str = Query(..., description="资产大类代码，如 IT"),
    year: Optional[int] = Query(
        None, ge=2000, le=9999, description="年份，默认当前年"
    ),
    db: Session = Depends(get_db),
):
    cls = asset_class.strip().upper()
    if not cls:
        raise HTTPException(status_code=400, detail="资产大类不能为空")
    settings = get_settings()
    y = year if year else datetime.now().year
    seq = code_util.next_sequence(db, settings.org_code, cls, y)
    code = code_util.build_code(settings.org_code, cls, y, seq)
    return {
        "code": code,
        "org": settings.org_code,
        "asset_class": cls,
        "year": y,
        "seq": seq,
    }


@router.get("", response_model=schemas.AssetListOut, summary="资产分页查询")
def list_assets(
    page: int = Query(1, ge=1, description="页码，从 1 开始"),
    page_size: int = Query(10, ge=1, le=200, description="每页数量"),
    keyword: Optional[str] = Query(None, description="按编号/品牌/型号/SN/使用人模糊搜索"),
    status: Optional[str] = Query(None, description="按状态过滤"),
    category: Optional[str] = Query(None, description="按分类过滤"),
    asset_class: Optional[str] = Query(None, description="按资产大类过滤，如 IT"),
    db: Session = Depends(get_db),
):
    total, items = crud.list_assets(
        db, page=page, page_size=page_size, keyword=keyword,
        status=status, category=category, asset_class=asset_class,
    )
    return {"total": total, "items": items}


@router.get("/{asset_id}", response_model=schemas.AssetOut, summary="资产详情")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    return asset


@router.post(
    "",
    response_model=schemas.AssetOut,
    status_code=status.HTTP_201_CREATED,
    summary="新增资产",
)
def create_asset(
    payload: schemas.AssetCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if payload.asset_code and crud.get_asset_by_code(db, payload.asset_code):
        raise HTTPException(status_code=400, detail="资产编号已存在")
    asset = crud.create_asset(db, payload)
    # 记录"新增资产"日志：把所有非空字段都列为 changes（before=None）
    after = activity.asset_to_dict(asset)
    changes = activity.diff_asset({}, after)
    activity.log(
        db,
        action="asset.create",
        actor=current_user,
        target_type="asset",
        target_id=asset.id,
        target_label=asset.asset_code,
        summary=f"新增资产 {asset.asset_code}",
        changes=changes,
        request=request,
    )
    return asset


@router.put("/{asset_id}", response_model=schemas.AssetOut, summary="更新资产")
def update_asset(
    asset_id: int,
    payload: schemas.AssetUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    before = activity.asset_to_dict(asset)
    asset = crud.update_asset(db, asset, payload)
    after = activity.asset_to_dict(asset)
    changes = activity.diff_asset(before, after)
    if changes:
        if len(changes) == 1:
            summary = f"修改资产 {asset.asset_code} 的「{changes[0]['label']}」"
        else:
            summary = (
                f"修改资产 {asset.asset_code}（共 {len(changes)} 项变更）"
            )
        activity.log(
            db,
            action="asset.update",
            actor=current_user,
            target_type="asset",
            target_id=asset.id,
            target_label=asset.asset_code,
            summary=summary,
            changes=changes,
            request=request,
        )
    return asset


@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除资产",
)
def delete_asset(
    asset_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    asset_code = asset.asset_code
    asset_pk = asset.id
    crud.delete_asset(db, asset)
    activity.log(
        db,
        action="asset.delete",
        actor=current_user,
        target_type="asset",
        target_id=asset_pk,
        target_label=asset_code,
        summary=f"删除资产 {asset_code}",
        request=request,
    )
    return None


def _build_qr_url(token: str) -> str:
    settings = get_settings()
    base = settings.public_base_url.rstrip("/")
    return f"{base}/p/asset/{token}"


@router.get(
    "/{asset_id}/qrcode-info",
    response_model=schemas.QrInfoOut,
    summary="获取该资产的二维码信息（URL + 图片接口）",
)
def asset_qr_info(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    asset = crud.ensure_public_token(db, asset)
    return {
        "public_token": asset.public_token,
        "qr_url": _build_qr_url(asset.public_token),
        "image_url": f"/api/assets/{asset.id}/qrcode.png",
    }


@router.post(
    "/{asset_id}/regenerate-token",
    response_model=schemas.QrInfoOut,
    summary="刷新二维码 token（旧二维码立即失效）",
)
def regenerate_qr_token(
    asset_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    asset = crud.regenerate_public_token(db, asset)
    activity.log(
        db,
        action="asset.qr.regen",
        actor=current_user,
        target_type="asset",
        target_id=asset.id,
        target_label=asset.asset_code,
        summary=f"刷新二维码 {asset.asset_code}（旧二维码已失效）",
        request=request,
    )
    return {
        "public_token": asset.public_token,
        "qr_url": _build_qr_url(asset.public_token),
        "image_url": f"/api/assets/{asset.id}/qrcode.png",
    }


@router.get(
    "/{asset_id}/qrcode.png",
    summary="下载该资产的二维码 PNG 图片",
    responses={200: {"content": {"image/png": {}}}},
)
def asset_qrcode_png(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    asset = crud.ensure_public_token(db, asset)
    png = make_qr_png(_build_qr_url(asset.public_token), box_size=10, border=2)
    headers = {
        "Content-Disposition": f'inline; filename="qr-{asset.asset_code}.png"',
        "Cache-Control": "no-store",
    }
    return Response(content=png, media_type="image/png", headers=headers)


# ============ 资产附件（腾讯云 COS） ============

@router.get(
    "/{asset_id}/files",
    response_model=List[schemas.AssetFileOut],
    summary="获取资产附件列表",
)
def list_files(asset_id: int, db: Session = Depends(get_db)):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")
    return crud.list_asset_files(db, asset_id)


@router.post(
    "/{asset_id}/files",
    response_model=schemas.AssetFileOut,
    status_code=status.HTTP_201_CREATED,
    summary="上传资产附件到腾讯云 COS",
)
async def upload_file(
    asset_id: int,
    request: Request,
    file: UploadFile = File(..., description="待上传的文件"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    asset = crud.get_asset(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="资产不存在")

    settings = get_settings()
    max_bytes = settings.upload_max_size_mb * 1024 * 1024

    content = await file.read()
    size = len(content)
    if size == 0:
        raise HTTPException(status_code=400, detail="文件为空")
    if size > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，单文件最大 {settings.upload_max_size_mb} MB",
        )

    safe_name = _safe_filename(file.filename or "file")
    object_key = (
        f"{settings.cos_prefix.strip('/')}"
        f"/{asset.asset_code}"
        f"/{uuid.uuid4().hex}_{safe_name}"
    )

    import io
    file_url = cos_client.upload_fileobj(
        io.BytesIO(content),
        object_key=object_key,
        content_type=file.content_type,
    )

    record = crud.create_asset_file(
        db,
        asset_id=asset.id,
        filename=safe_name,
        object_key=object_key,
        file_url=file_url,
        content_type=file.content_type,
        size=size,
        uploader=current_user.username,
    )
    activity.log(
        db,
        action="file.upload",
        actor=current_user,
        target_type="file",
        target_id=record.id,
        target_label=safe_name,
        summary=f"为 {asset.asset_code} 上传附件 {safe_name}",
        extra={
            "asset_code": asset.asset_code,
            "asset_id": asset.id,
            "size": size,
        },
        request=request,
    )
    return record


# ============ Excel 批量导入（AI 智能映射） ============

@router.post(
    "/import/parse",
    response_model=schemas.ImportParseOut,
    summary="解析 Excel / CSV，返回 AI 推断的列映射与规范化后的数据预览",
)
async def import_parse(
    file: UploadFile = File(..., description="待导入的 .xlsx / .xls / .csv 文件"),
    mapping: Optional[str] = Form(
        default=None,
        description="可选：用户在前一步手动调整后的 mapping JSON 字符串，"
                    "传入后跳过 AI 调用，直接按此映射规范化",
    ),
    header_row: Optional[int] = Form(
        default=None,
        description="可选：1-based 表头所在行号；不传则由后端自动检测",
    ),
    db: Session = Depends(get_db),
):
    try:
        return await _import_parse_impl(file, mapping, header_row, db)
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        tb = traceback.format_exc()
        print("[import_parse] 未捕获异常:\n" + tb, flush=True)
        logger.error("import_parse failed: %s\n%s", e, tb)
        raise HTTPException(
            status_code=500,
            detail=f"导入解析失败（{type(e).__name__}）：{e}",
        ) from e


async def _import_parse_impl(
    file: UploadFile,
    mapping: Optional[str],
    header_row: Optional[int],
    db: Session,
):
    settings = get_settings()
    max_bytes = settings.upload_max_size_mb * 1024 * 1024
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="文件为空")
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"文件过大，单文件最大 {settings.upload_max_size_mb} MB",
        )

    name = (file.filename or "").lower()
    if name.endswith(".xls") and not name.endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="不支持旧版 .xls 格式，请先用 Excel 另存为 .xlsx 后再上传",
        )
    if not (name.endswith(".xlsx") or name.endswith(".csv")):
        raise HTTPException(
            status_code=400, detail="仅支持 .xlsx / .csv 文件"
        )

    try:
        headers, raw_rows, header_row_used = excel_import.parse_workbook(
            content, file.filename or "", header_row=header_row
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=400, detail=f"文件解析失败：{e}"
        ) from e

    # 顶部预览失败不影响主流程
    try:
        top_preview = excel_import.preview_top_rows(content, file.filename or "")
    except Exception:  # noqa: BLE001
        top_preview = []

    if not headers:
        raise HTTPException(
            status_code=400,
            detail="未识别到表头，请确认文件首部是否包含列名行；"
                   "如顶部有标题/说明行，可在前端切换表头行后重试",
        )

    user_mapping: Optional[dict] = None
    if mapping:
        try:
            user_mapping = json.loads(mapping)
            if not isinstance(user_mapping, dict):
                raise ValueError("mapping 不是 JSON 对象")
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=400, detail=f"mapping 参数无法解析为 JSON：{e}"
            ) from e

    if user_mapping is not None:
        cleaned: dict = {}
        for h in headers:
            v = user_mapping.get(h)
            cleaned[h] = v if (isinstance(v, str) and v) else None
        mapping_out = cleaned
        llm_used = False
    else:
        samples = raw_rows[:5]
        mapping_out, llm_used = excel_import.resolve_mapping(headers, samples)

    rows_out: List[dict] = []
    error_count = 0
    warning_count = 0
    for idx, raw in enumerate(raw_rows, start=1):
        data, issues = excel_import.normalize_row(raw, mapping_out)
        has_error = any(i["level"] == "error" for i in issues)
        has_warn = any(i["level"] == "warning" for i in issues)
        if has_error:
            error_count += 1
        if has_warn:
            warning_count += 1
        rows_out.append(
            {
                "row_index": idx,
                "data": data,
                "issues": issues,
            }
        )

    field_dict = excel_import.get_field_dict()
    return {
        "headers": headers,
        "mapping": mapping_out,
        "rows": rows_out,
        "total": len(rows_out),
        "error_count": error_count,
        "warning_count": warning_count,
        "llm_used": llm_used,
        "header_row": header_row_used,
        "header_auto_detected": header_row is None,
        "top_rows_preview": top_preview,
        "field_dict": [{"key": k, "label": v} for k, v in field_dict.items()],
    }


@router.post(
    "/import/ai-fill",
    response_model=schemas.ImportAiFillOut,
    summary="AI 一键补全：参考系统已有资产风格，补全选中行的缺失字段",
)
def import_ai_fill(
    payload: schemas.ImportAiFillIn,
    db: Session = Depends(get_db),
):
    if not payload.rows:
        raise HTTPException(status_code=400, detail="没有需要补全的行")
    if not llm_is_configured():
        raise HTTPException(
            status_code=400,
            detail="后端未配置百炼 API Key，无法使用 AI 补全。"
                   "请先在 Back_end/.env 中设置 DASHSCOPE_API_KEY 后重启服务。",
        )

    # 取最近的若干条资产作为「前置资产样本」，供 LLM 参考风格
    _, recent_assets = crud.list_assets(db, page=1, page_size=30)
    reference_assets = [
        excel_import.asset_to_reference(a) for a in recent_assets
    ]
    reference_assets = [r for r in reference_assets if r]

    input_rows = [
        {"row_index": r.row_index, "data": dict(r.data or {})}
        for r in payload.rows
    ]

    try:
        new_rows, err_count, warn_count = excel_import.apply_ai_fill(
            input_rows,
            reference_assets,
            only_missing=payload.only_missing,
        )
    except LLMUnavailable as e:
        raise HTTPException(
            status_code=502,
            detail=f"AI 补全失败：{e}",
        ) from e
    except Exception as e:  # noqa: BLE001
        tb = traceback.format_exc()
        print("[import_ai_fill] 未捕获异常:\n" + tb, flush=True)
        logger.error("import_ai_fill failed: %s\n%s", e, tb)
        raise HTTPException(
            status_code=500,
            detail=f"AI 补全异常（{type(e).__name__}）：{e}",
        ) from e

    return {
        "rows": new_rows,
        "error_count": err_count,
        "warning_count": warn_count,
        "used_samples": len(reference_assets),
        "llm_used": True,
    }


@router.post(
    "/import/commit",
    response_model=schemas.ImportCommitOut,
    summary="批量入库（接收预览阶段确认后的资产数据）",
)
def import_commit(
    payload: schemas.ImportCommitIn,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    try:
        return _import_commit_impl(payload, request, db, current_user)
    except HTTPException:
        raise
    except Exception as e:  # noqa: BLE001
        tb = traceback.format_exc()
        print("[import_commit] 未捕获异常:\n" + tb, flush=True)
        logger.error("import_commit failed: %s\n%s", e, tb)
        raise HTTPException(
            status_code=500,
            detail=f"批量导入失败（{type(e).__name__}）：{e}",
        ) from e


def _import_commit_impl(
    payload: schemas.ImportCommitIn,
    request: Request,
    db: Session,
    current_user: models.User,
):
    settings = get_settings()
    rows = payload.rows
    if not rows:
        raise HTTPException(status_code=400, detail="没有可导入的数据")
    if len(rows) > settings.import_max_rows:
        raise HTTPException(
            status_code=400,
            detail=f"单次导入不能超过 {settings.import_max_rows} 行",
        )

    success_codes: List[str] = []
    failures: List[dict] = []
    for idx, item in enumerate(rows):
        # 批量导入时强制忽略 Excel 中的资产编号，统一由平台按
        # 「机构-大类-年份-流水」规则自动生成，避免外部编号与系统冲突 / 重复。
        item.asset_code = None
        try:
            asset = crud.create_asset(db, item)
            success_codes.append(asset.asset_code)
        except HTTPException as e:
            failures.append(
                {
                    "index": idx,
                    "asset_code": None,
                    "error": str(e.detail),
                }
            )
        except Exception as e:  # noqa: BLE001
            failures.append(
                {
                    "index": idx,
                    "asset_code": None,
                    "error": str(e),
                }
            )

    total = len(rows)
    success = len(success_codes)
    failed = len(failures)
    activity.log(
        db,
        action="asset.import",
        actor=current_user,
        target_type="asset",
        target_label=f"共 {total} 条",
        summary=f"批量导入资产：成功 {success} 条 / 失败 {failed} 条",
        extra={
            "total": total,
            "success": success,
            "failed": failed,
            "success_codes": success_codes[:50],
            "failures": failures[:50],
        },
        request=request,
    )
    return {
        "success": success,
        "failed": failed,
        "failures": failures,
    }


@router.delete(
    "/{asset_id}/files/{file_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="删除资产附件（同时删除 COS 对象）",
)
def delete_file(
    asset_id: int,
    file_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    record = crud.get_asset_file(db, file_id)
    if not record or record.asset_id != asset_id:
        raise HTTPException(status_code=404, detail="附件不存在")
    asset = crud.get_asset(db, asset_id)
    asset_code = asset.asset_code if asset else ""
    filename = record.filename
    cos_client.delete_object(record.object_key)
    crud.delete_asset_file(db, record)
    activity.log(
        db,
        action="file.delete",
        actor=current_user,
        target_type="file",
        target_id=file_id,
        target_label=filename,
        summary=f"删除 {asset_code} 的附件 {filename}",
        extra={"asset_code": asset_code, "asset_id": asset_id},
        request=request,
    )
    return None
