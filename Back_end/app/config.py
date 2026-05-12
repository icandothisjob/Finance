"""应用配置：读取 .env 中的环境变量。"""
from functools import lru_cache
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    mysql_host: str = Field(default="127.0.0.1")
    mysql_port: int = Field(default=3306)
    mysql_user: str = Field(default="root")
    mysql_password: str = Field(default="123456")
    mysql_database: str = Field(default="asset_management")

    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    cors_origins: str = Field(
        default="http://localhost:5173,http://127.0.0.1:5173"
    )

    jwt_secret: str = Field(default="please-change-me-to-a-long-random-string")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expire_minutes: int = Field(default=24 * 60)

    default_admin_username: str = Field(default="DAIL")
    default_admin_password: str = Field(default="DAIL2026")

    org_code: str = Field(default="DG", description="组织码，用于资产编号前缀")

    public_base_url: str = Field(
        default="http://localhost:5173",
        description="二维码扫码后跳转的前端基础 URL",
    )

    cos_secret_id: str = Field(default="", description="腾讯云 COS SecretId")
    cos_secret_key: str = Field(default="", description="腾讯云 COS SecretKey")
    cos_region: str = Field(default="ap-chengdu", description="COS 所在地域")
    cos_bucket: str = Field(default="", description="COS 桶名（含 APPID 后缀）")
    cos_domain: str = Field(
        default="",
        description="可选：自定义/CDN 域名；留空则用默认 cos.<region>.myqcloud.com",
    )
    cos_prefix: str = Field(
        default="assets",
        description="对象前缀（目录），最终 key=<prefix>/<asset_code>/<uuid>_<filename>",
    )
    upload_max_size_mb: int = Field(
        default=50, description="单个文件最大大小（MB）"
    )

    dashscope_api_key: str = Field(default="", description="百炼 API Key")
    dashscope_base_url: str = Field(
        default="https://dashscope.aliyuncs.com/compatible-mode/v1",
        description="百炼 OpenAI 兼容接口 Base URL",
    )
    dashscope_model: str = Field(
        default="qwen-plus", description="使用的百炼模型名称"
    )
    import_max_rows: int = Field(
        default=500, description="单次 Excel 导入最大行数"
    )

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
            f"?charset=utf8mb4"
        )

    @property
    def cors_origin_list(self) -> List[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
