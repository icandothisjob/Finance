"""Pydantic Schemas：请求与响应数据结构。"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class LoginIn(BaseModel):
    username: str = Field(..., max_length=64)
    password: str = Field(..., max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    nickname: Optional[str] = None
    is_active: bool


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="过期秒数")
    user: UserOut


class AssetBase(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    asset_code: str = Field(..., max_length=64, description="资产编号")
    asset_class: str = Field(..., max_length=8, description="资产大类代码，例如 IT")
    category: str = Field(..., max_length=64, description="资产分类，例如 笔记本电脑")
    brand: Optional[str] = Field(default=None, max_length=64, description="品牌")
    model: Optional[str] = Field(default=None, max_length=128, description="型号")
    serial_number: Optional[str] = Field(
        default=None, max_length=64, description="SN / 序列号"
    )
    specification: Optional[str] = Field(
        default=None, max_length=255, description="规格配置"
    )
    purchase_date: Optional[datetime] = Field(default=None, description="购置日期")
    supplier: Optional[str] = Field(
        default=None, max_length=128, description="供应商/采购渠道"
    )
    price: Optional[float] = Field(default=None, ge=0, description="采购金额")
    warranty_until: Optional[datetime] = Field(
        default=None, description="保修到期日期"
    )
    location: Optional[str] = Field(default=None, max_length=128)
    owner: Optional[str] = Field(default=None, max_length=64)
    department: Optional[str] = Field(default=None, max_length=64)
    status: str = Field(default="在用", max_length=32)
    remark: Optional[str] = Field(default=None, max_length=255)


class AssetCreate(AssetBase):
    asset_code: Optional[str] = Field(
        default=None,
        max_length=64,
        description="资产编号；留空则后端按规则自动生成",
    )


class AssetUpdate(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    asset_class: Optional[str] = Field(default=None, max_length=8)
    category: Optional[str] = Field(default=None, max_length=64)
    brand: Optional[str] = Field(default=None, max_length=64)
    model: Optional[str] = Field(default=None, max_length=128)
    serial_number: Optional[str] = Field(default=None, max_length=64)
    specification: Optional[str] = Field(default=None, max_length=255)
    purchase_date: Optional[datetime] = None
    supplier: Optional[str] = Field(default=None, max_length=128)
    price: Optional[float] = Field(default=None, ge=0)
    warranty_until: Optional[datetime] = None
    location: Optional[str] = Field(default=None, max_length=128)
    owner: Optional[str] = Field(default=None, max_length=64)
    department: Optional[str] = Field(default=None, max_length=64)
    status: Optional[str] = Field(default=None, max_length=32)
    remark: Optional[str] = Field(default=None, max_length=255)


class AssetOut(AssetBase):
    model_config = ConfigDict(from_attributes=True, protected_namespaces=())

    id: int
    created_at: datetime
    updated_at: datetime


class AssetListOut(BaseModel):
    total: int
    items: List[AssetOut]


class AssetClassDictItem(BaseModel):
    code: str
    name: str


class NextCodeOut(BaseModel):
    code: str
    org: str
    asset_class: str
    year: int
    seq: int


class QrInfoOut(BaseModel):
    """二维码相关信息。"""
    public_token: str
    qr_url: str = Field(..., description="二维码包含的目标 URL（前端展示页）")
    image_url: str = Field(..., description="二维码 PNG 接口路径（带 token）")


class AssetFileOut(BaseModel):
    """资产附件信息。"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    filename: str
    object_key: str
    file_url: str
    content_type: Optional[str] = None
    size: int
    uploader: Optional[str] = None
    created_at: datetime


class PublicAssetOut(BaseModel):
    """对外公开（无需登录）展示的字段。"""
    model_config = ConfigDict(protected_namespaces=())

    asset_code: str
    asset_class: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    specification: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    purchase_date: Optional[datetime] = None
    price: Optional[float] = None
    owner: Optional[str] = None
    department: Optional[str] = None


class FieldChange(BaseModel):
    """单个字段的变更详情。"""
    field: str = Field(..., description="字段英文名")
    label: str = Field(..., description="字段中文名")
    before: Optional[str] = None
    after: Optional[str] = None


class ActivityLogOut(BaseModel):
    """消息列表项。"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    actor: Optional[str] = None
    actor_nickname: Optional[str] = None
    action: str
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    target_label: Optional[str] = None
    summary: str
    changes: List[FieldChange] = Field(default_factory=list)
    ip: Optional[str] = None
    is_read: bool = False
    created_at: datetime


class ActivityLogListOut(BaseModel):
    total: int
    unread: int = Field(0, description="当前用户未读数（仅 scope=all 时有意义）")
    items: List[ActivityLogOut]


class UnreadCountOut(BaseModel):
    unread: int


class MarkReadIn(BaseModel):
    ids: Optional[List[int]] = Field(
        default=None,
        description="要标记为已读的日志 ID 列表；为空则标记当前可见范围内全部已读",
    )


# ============ Excel 批量导入 ============


class ImportIssue(BaseModel):
    """单行解析过程中产生的问题（错误或警告）。"""

    level: str = Field(..., description="error / warning")
    field: Optional[str] = Field(default=None, description="所属字段 key")
    message: str = Field(..., description="问题描述")


class ImportRowOut(BaseModel):
    """解析后的一行候选数据。"""

    row_index: int = Field(..., description="Excel 中的行号（1 = 表头下方第一行）")
    data: Dict[str, Any] = Field(
        ..., description="已规范化的字段字典，键为系统字段 key"
    )
    issues: List[ImportIssue] = Field(default_factory=list)


class FieldDictItem(BaseModel):
    """系统字段说明（提供给前端做列映射下拉用）。"""

    key: str
    label: str


class ImportParseOut(BaseModel):
    """/import/parse 响应。"""

    headers: List[str] = Field(..., description="Excel 原始列名")
    mapping: Dict[str, Optional[str]] = Field(
        ..., description="原列名 -> 系统字段 key"
    )
    rows: List[ImportRowOut]
    total: int = Field(..., description="解析出的总行数")
    error_count: int = Field(..., description="存在 error 的行数")
    warning_count: int = Field(..., description="存在 warning 的行数")
    llm_used: bool = Field(..., description="本次列映射是否由大模型完成")
    header_row: int = Field(
        ..., description="本次使用的表头所在行号（1-based）"
    )
    header_auto_detected: bool = Field(
        ..., description="表头行是否由后端自动检测（false 表示用户强制指定）"
    )
    top_rows_preview: List[List[Optional[str]]] = Field(
        default_factory=list,
        description="顶部最多 10 行的原始内容预览，便于前端让用户切换表头行",
    )
    field_dict: List[FieldDictItem] = Field(
        default_factory=list, description="系统字段字典，供前端下拉显示"
    )


class ImportCommitIn(BaseModel):
    """/import/commit 请求体。"""

    rows: List[AssetCreate] = Field(
        ..., description="用户预览/编辑后的待入库列表"
    )


class ImportFailure(BaseModel):
    index: int = Field(..., description="rows 列表中的下标（0-based）")
    asset_code: Optional[str] = None
    error: str


class ImportCommitOut(BaseModel):
    success: int
    failed: int
    failures: List[ImportFailure] = Field(default_factory=list)


# ============ AI 一键补全 ============


class ImportAiFillRow(BaseModel):
    """ai-fill 接口的输入行。"""

    row_index: int = Field(..., description="Excel 行号（与解析阶段一致）")
    data: Dict[str, Any] = Field(
        default_factory=dict, description="当前已知字段（含用户已手工修正的值）"
    )


class ImportAiFillIn(BaseModel):
    """/import/ai-fill 请求体。"""

    rows: List[ImportAiFillRow] = Field(
        ..., description="需要补全的待入库行（一般是含 error / warning 的那些）"
    )
    only_missing: bool = Field(
        default=True,
        description="为 true 时只补全空字段；为 false 允许模型对已存在的字段也给出更规范的建议",
    )


class ImportAiFillOut(BaseModel):
    """/import/ai-fill 响应。"""

    rows: List[ImportRowOut] = Field(
        ..., description="补全后的行（已重新跑过规范化与校验）"
    )
    error_count: int = 0
    warning_count: int = 0
    used_samples: int = Field(0, description="参考的前置资产样本条数")
    llm_used: bool = Field(True, description="是否真的调用了大模型")
