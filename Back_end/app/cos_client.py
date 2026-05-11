"""腾讯云 COS 客户端封装。

依赖：cos-python-sdk-v5
SDK 文档：https://cloud.tencent.com/document/product/436/12269
"""
from __future__ import annotations

import logging
from functools import lru_cache
from typing import BinaryIO, Optional

from fastapi import HTTPException
from qcloud_cos import CosConfig, CosS3Client
from qcloud_cos.cos_exception import CosClientError, CosServiceError

from .config import get_settings

logger = logging.getLogger(__name__)


@lru_cache
def get_cos_client() -> CosS3Client:
    """单例式获取 COS 客户端。"""
    s = get_settings()
    if not (s.cos_secret_id and s.cos_secret_key and s.cos_bucket and s.cos_region):
        raise HTTPException(
            status_code=500,
            detail="COS 未配置，请在 Back_end/.env 中填写 COS_SECRET_ID / COS_SECRET_KEY / COS_BUCKET / COS_REGION",
        )
    config = CosConfig(
        Region=s.cos_region,
        SecretId=s.cos_secret_id,
        SecretKey=s.cos_secret_key,
        Token=None,
        Scheme="https",
    )
    return CosS3Client(config)


def build_public_url(object_key: str) -> str:
    """根据配置生成对象的公开访问 URL。"""
    s = get_settings()
    if s.cos_domain:
        domain = s.cos_domain.rstrip("/")
        if not domain.startswith("http"):
            domain = f"https://{domain}"
        return f"{domain}/{object_key}"
    return f"https://{s.cos_bucket}.cos.{s.cos_region}.myqcloud.com/{object_key}"


def upload_fileobj(
    file_obj: BinaryIO,
    object_key: str,
    content_type: Optional[str] = None,
) -> str:
    """上传文件流到 COS，返回对象的公开访问 URL。"""
    s = get_settings()
    client = get_cos_client()
    try:
        client.put_object(
            Bucket=s.cos_bucket,
            Body=file_obj,
            Key=object_key,
            ContentType=content_type or "application/octet-stream",
        )
    except (CosClientError, CosServiceError) as e:
        logger.exception("COS 上传失败: %s", e)
        raise HTTPException(status_code=500, detail=f"上传到 COS 失败: {e}") from e
    return build_public_url(object_key)


def delete_object(object_key: str) -> None:
    """从 COS 删除对象（不存在时忽略）。"""
    s = get_settings()
    client = get_cos_client()
    try:
        client.delete_object(Bucket=s.cos_bucket, Key=object_key)
    except CosServiceError as e:
        # 404 / NoSuchKey 直接忽略
        if str(e.get_status_code()).startswith("4"):
            logger.warning("COS 删除对象不存在或被忽略: %s", object_key)
            return
        logger.exception("COS 删除失败: %s", e)
        raise HTTPException(status_code=500, detail=f"删除 COS 对象失败: {e}") from e
    except CosClientError as e:
        logger.exception("COS 删除失败: %s", e)
        raise HTTPException(status_code=500, detail=f"删除 COS 对象失败: {e}") from e
