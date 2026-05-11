"""资产编号生成与校验。

格式：  ORG-CLASS-YEAR-SEQ-CHECK
示例：  DG-IT-2026-000123-X

- ORG     组织码（来自配置 ORG_CODE，2~6 位字母/数字）
- CLASS   资产大类代码（IT/OF/VH/...，1~6 位字母/数字）
- YEAR    入账年份，4 位数字
- SEQ     当年（同组织+同大类）流水号，6 位数字
- CHECK   校验位，0~9 或 X（ISO 7064 MOD 11-2 改进版）

说明：校验位输入是 "ORG+CLASS+YEAR+SEQ" 拼接后的字符串（已去掉横线、转大写），
任何一段录错都会令校验位与之不符，从而被识别。
"""
from __future__ import annotations

import re
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models

# 内置资产大类字典（与业务定义一致；后续可改为数据库表维护）
ASSET_CLASSES: list[dict[str, str]] = [
    {"code": "IT", "name": "信息化设备"},
    {"code": "OF", "name": "办公家具"},
    {"code": "VH", "name": "车辆"},
    {"code": "ME", "name": "机械设备"},
    {"code": "IN", "name": "仪器仪表"},
    {"code": "OT", "name": "其他"},
]
ASSET_CLASS_CODES = {c["code"] for c in ASSET_CLASSES}

CODE_PATTERN = re.compile(
    r"^([A-Z0-9]{2,6})-([A-Z0-9]{1,6})-(\d{4})-(\d{6})-([0-9X])$"
)

_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def compute_check_char(base: str) -> str:
    """ISO 7064 MOD 11-2 校验位（支持数字 + 大写字母）。

    base：编号去掉校验位、去掉横线、统一大写后的字符串，
          例如 'DGIT2026000123'。
    """
    s = base.replace("-", "").upper()
    total = 0
    n = len(s)
    for i, ch in enumerate(s):
        v = _ALPHABET.index(ch) if ch in _ALPHABET else 0
        # 从右到左权重为 2^0, 2^1, ...，模 11
        weight = pow(2, n - i - 1, 11)
        total = (total + v * weight) % 11
    rem = (12 - total) % 11
    return "X" if rem == 10 else str(rem)


def build_code(org: str, asset_class: str, year: int, seq: int) -> str:
    """根据各段拼出完整编号（含校验位）。"""
    base = f"{org.upper()}-{asset_class.upper()}-{year:04d}-{seq:06d}"
    return f"{base}-{compute_check_char(base)}"


def parse_code(code: str) -> Optional[dict]:
    """解析编号；不合法返回 None。"""
    if not code:
        return None
    m = CODE_PATTERN.match(code.strip().upper())
    if not m:
        return None
    org, cls, year, seq, chk = m.groups()
    return {
        "org": org,
        "asset_class": cls,
        "year": int(year),
        "seq": int(seq),
        "check": chk,
    }


def is_valid_code(code: str) -> bool:
    """格式合法且校验位正确。"""
    parsed = parse_code(code)
    if not parsed:
        return False
    base = f"{parsed['org']}-{parsed['asset_class']}-{parsed['year']:04d}-{parsed['seq']:06d}"
    return compute_check_char(base) == parsed["check"]


def next_sequence(
    db: Session, org: str, asset_class: str, year: int
) -> int:
    """查询同组织+大类+年份的当前最大流水号 + 1。"""
    prefix = f"{org.upper()}-{asset_class.upper()}-{year:04d}-"
    rows = (
        db.execute(
            select(models.Asset.asset_code).where(
                models.Asset.asset_code.like(f"{prefix}%")
            )
        )
        .scalars()
        .all()
    )
    max_seq = 0
    for c in rows:
        parsed = parse_code(c)
        if parsed and parsed["seq"] > max_seq:
            max_seq = parsed["seq"]
    return max_seq + 1


def generate_next_code(
    db: Session,
    org: str,
    asset_class: str,
    year: Optional[int] = None,
) -> str:
    """生成下一个可用编号。"""
    if asset_class.upper() not in ASSET_CLASS_CODES:
        # 仍允许使用，但会按字典外大类继续编号
        pass
    y = year if year else datetime.now().year
    seq = next_sequence(db, org, asset_class, y)
    return build_code(org, asset_class, y, seq)
