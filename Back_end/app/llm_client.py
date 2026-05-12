"""阿里云百炼（DashScope）OpenAI 兼容协议客户端封装。

仅用于"看几行 Excel 样本，猜列名映射"这种轻量结构化任务，
不做按行抽取，避免成本随行数线性增长。

实现方式：直接用 httpx 调 DashScope 的 OpenAI 兼容 REST 接口，
不依赖 openai SDK，避免 openai 1.54.0 与新版 httpx 的 proxies 兼容性 bug。

调用失败、未配置 KEY、解析异常时均抛 LLMUnavailable，由上层走规则兜底。
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

from .config import get_settings

logger = logging.getLogger(__name__)


class LLMUnavailable(Exception):
    """LLM 不可用或调用失败的统一异常。"""


# 系统字段字典：key=英文字段，value=中文说明 + 示例
SYSTEM_FIELD_DICT: Dict[str, str] = {
    "asset_code": "资产编号（如 DG-IT-2026-000123-X，留空将自动生成）",
    "asset_class": "资产大类代码（IT=信息化设备/OF=办公家具/VH=车辆/ME=机械设备/IN=仪器仪表/OT=其他）",
    "category": "资产分类（如 笔记本电脑、显示器、办公桌、轿车）",
    "brand": "品牌（如 联想、Dell、华为）",
    "model": "型号（如 ThinkPad T14s、XPS 13）",
    "serial_number": "SN / 序列号",
    "specification": "规格配置（如 R7-7840U/16GB/512GB）",
    "purchase_date": "购置日期（任意日期格式都会被规范化）",
    "supplier": "供应商 / 采购渠道",
    "price": "采购金额（数字，可带 ¥ 元）",
    "warranty_until": "保修到期日期",
    "location": "存放位置（如 办公室A、机房）",
    "owner": "使用人 / 责任人",
    "department": "所属部门",
    "status": "状态：在用 / 闲置 / 维修 / 报废",
    "remark": "备注",
}

ALLOWED_FIELD_KEYS = set(SYSTEM_FIELD_DICT.keys())


def is_configured() -> bool:
    """是否配置了百炼 API Key。"""
    return bool(get_settings().dashscope_api_key.strip())


def _chat_completion(
    messages: List[Dict[str, str]],
    *,
    response_format: Optional[Dict[str, str]] = None,
    temperature: float = 0.0,
    timeout: float = 30.0,
) -> str:
    """直接走 OpenAI 兼容 REST 接口调 DashScope，避开 openai SDK 的兼容性问题。

    返回 assistant 消息的 content 字符串；任何异常（含网络、HTTP 非 2xx、
    返回结构不符合预期等）都包装成 LLMUnavailable 抛出。
    """
    settings = get_settings()
    if not settings.dashscope_api_key.strip():
        raise LLMUnavailable("DASHSCOPE_API_KEY 未配置")

    try:
        import httpx
    except ImportError as e:  # pragma: no cover - 依赖未装
        raise LLMUnavailable(f"httpx 未安装：{e}") from e

    url = settings.dashscope_base_url.rstrip("/") + "/chat/completions"
    payload: Dict[str, Any] = {
        "model": settings.dashscope_model,
        "messages": messages,
        "temperature": temperature,
    }
    if response_format is not None:
        payload["response_format"] = response_format

    headers = {
        "Authorization": f"Bearer {settings.dashscope_api_key}",
        "Content-Type": "application/json",
    }

    try:
        with httpx.Client(timeout=timeout, follow_redirects=True) as client:
            resp = client.post(url, json=payload, headers=headers)
    except Exception as e:  # noqa: BLE001
        raise LLMUnavailable(f"百炼请求网络异常：{e}") from e

    if resp.status_code >= 400:
        body = resp.text[:500]
        raise LLMUnavailable(
            f"百炼接口返回 {resp.status_code}：{body}"
        )

    try:
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError) as e:
        raise LLMUnavailable(f"百炼返回结构异常：{e}") from e

    if not isinstance(content, str):
        raise LLMUnavailable(f"百炼返回 content 非字符串：{type(content).__name__}")
    return content


def map_columns(
    headers: List[str], samples: List[Dict[str, Any]]
) -> Dict[str, Optional[str]]:
    """让大模型把 Excel 原列名映射到系统字段 key。

    参数：
        headers：Excel 表头原始列名列表
        samples：前若干行的样本（每行是 {原列名: 单元格值}），便于模型理解列含义

    返回：
        dict，键是原列名，值是系统字段 key 或 None；未识别的列值为 None。

    任何异常都会被统一包装成 LLMUnavailable。
    """
    if not headers:
        return {}

    field_dict_text = json.dumps(SYSTEM_FIELD_DICT, ensure_ascii=False, indent=2)
    sample_text = json.dumps(samples[:5], ensure_ascii=False, default=str)
    headers_text = json.dumps(headers, ensure_ascii=False)

    system_prompt = (
        "你是企业资产管理系统的字段映射助手。"
        "用户会给你一个 Excel 的表头和若干样本行，"
        "你需要把每个原始列名映射到系统的标准字段 key。"
        "只能输出严格 JSON，不允许任何解释或 Markdown。"
    )

    user_prompt = f"""系统字段字典（key 为字段英文名，value 为中文说明 + 示例）：
{field_dict_text}

Excel 表头：
{headers_text}

前若干行样本（list of object，键为原列名）：
{sample_text}

请输出一个 JSON 对象，键必须是 Excel 原列名（与表头数组一一对应），
值必须是上面字典里的某个 key，或者 null（表示无法匹配）。
不要输出任何解释，只输出 JSON 对象本身。
"""

    content = _chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.0,
        timeout=30.0,
    )

    try:
        raw = json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning("百炼返回解析失败：%s; content=%r", e, content[:300])
        raise LLMUnavailable(f"返回内容不是合法 JSON：{e}") from e

    if not isinstance(raw, dict):
        raise LLMUnavailable("返回 JSON 顶层不是对象")

    result: Dict[str, Optional[str]] = {}
    for h in headers:
        v = raw.get(h)
        if isinstance(v, str) and v in ALLOWED_FIELD_KEYS:
            result[h] = v
        else:
            result[h] = None
    return result


# 可被 LLM 补全的字段（asset_code 由系统生成，不允许覆盖）
_FILLABLE_FIELDS = [k for k in SYSTEM_FIELD_DICT.keys() if k != "asset_code"]


def fill_missing_fields(
    rows: List[Dict[str, Any]],
    reference_assets: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """根据前置资产样本，让大模型补全每一行缺失的字段。

    参数：
        rows：待补全行，每个元素形如 {"row_index": int, "data": {...}, "missing": [...]}
              其中 missing 是建议优先补的字段 key 列表（可为空，模型会自行判断）。
        reference_assets：系统现有的若干资产，作为风格 / 取值参考的 few-shot 样本。

    返回：
        list[dict]，长度与 rows 一致；每个元素是 {"row_index": int, "data": {...}}，
        data 只包含模型给出的「建议覆盖 / 新增」字段（已有非空字段会被忠实保留并回传）。

    任何异常都会被统一包装成 LLMUnavailable。
    """
    if not rows:
        return []

    field_dict_text = json.dumps(
        {k: SYSTEM_FIELD_DICT[k] for k in _FILLABLE_FIELDS},
        ensure_ascii=False,
        indent=2,
    )
    ref_text = json.dumps(reference_assets[:20], ensure_ascii=False, default=str)
    rows_text = json.dumps(rows, ensure_ascii=False, default=str)

    system_prompt = (
        "你是企业资产管理系统的数据补全助手。"
        "用户会给你若干「前置资产样本」和若干「待补全行」，"
        "你需要参考前置样本的取值风格（例如分类命名习惯、部门简称、状态用语等），"
        "对每个待补全行尽量推断出缺失的字段值。"
        "严格遵守以下规则：\n"
        "1. 只能输出严格 JSON，不允许任何解释 / Markdown / 代码块标记；\n"
        "2. 已有非空字段必须忠实保留原值，不得修改；\n"
        "3. 对真的无法合理推断的字段返回 null，不要瞎编序列号 / SN / 具体日期；\n"
        "4. 资产大类只能取 IT/OF/VH/ME/IN/OT 之一；\n"
        "5. 状态只能取 在用/闲置/维修/报废 之一；\n"
        "6. 不要返回 asset_code（系统会自动生成）。"
    )

    user_prompt = f"""可补全的系统字段字典（key 为字段英文名，value 为中文说明）：
{field_dict_text}

前置资产样本（最多 20 条，作为风格 / 取值参考）：
{ref_text}

待补全行（每行含已有字段 data 与建议优先补的字段 missing）：
{rows_text}

请输出 JSON 数组，长度与待补全行一致，每个元素形如：
  {{"row_index": <对应输入行的 row_index>, "data": {{字段key: 值或null, ...}}}}
data 中应包含「保留下来的原值」+「推断出来的新值」，缺失且无法推断的字段填 null。
不要输出任何解释，只输出 JSON 数组本身。
"""

    content = _chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.2,
        timeout=45.0,
    )

    try:
        raw = json.loads(content)
    except json.JSONDecodeError as e:
        logger.warning("百炼补全返回解析失败：%s; content=%r", e, content[:300])
        raise LLMUnavailable(f"补全返回内容不是合法 JSON：{e}") from e

    # 兼容大模型在外层套对象的情况，如 {"rows": [...]} 或 {"result": [...]}
    if isinstance(raw, dict):
        for k in ("rows", "result", "data", "items"):
            if isinstance(raw.get(k), list):
                raw = raw[k]
                break

    if not isinstance(raw, list):
        raise LLMUnavailable("补全返回 JSON 顶层不是数组")

    cleaned: List[Dict[str, Any]] = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        row_index = item.get("row_index")
        data = item.get("data") if isinstance(item.get("data"), dict) else {}
        # 过滤非法字段 / 丢掉 asset_code（始终由系统生成）
        safe_data: Dict[str, Any] = {}
        for k, v in data.items():
            if k in _FILLABLE_FIELDS:
                safe_data[k] = v
        cleaned.append({"row_index": row_index, "data": safe_data})
    return cleaned
