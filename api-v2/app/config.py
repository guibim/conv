from dataclasses import dataclass
import os


def _parse_origins(value: str) -> list[str]:
    origins = [origin.strip() for origin in value.split(",") if origin.strip()]
    return origins


def _parse_bool(value: str, default: bool) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class Settings:
    service_name: str
    version: str
    max_upload_bytes: int
    allowed_origins: list[str]
    cors_allow_credentials: bool


def get_settings() -> Settings:
    origins = _parse_origins(
        os.getenv(
            "ALLOWED_ORIGINS",
            "https://guibim.github.io,http://localhost:3000,http://127.0.0.1:3000",
        )
    )

    return Settings(
        service_name="Conv API v2",
        version="2.0.0",
        max_upload_bytes=int(os.getenv("MAX_UPLOAD_BYTES", str(10 * 1024 * 1024))),
        allowed_origins=origins,
        cors_allow_credentials=_parse_bool(
            os.getenv("CORS_ALLOW_CREDENTIALS", "false"),
            default=False,
        ),
    )


settings = get_settings()
