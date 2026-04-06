from dataclasses import dataclass, field
from typing import Callable


@dataclass(frozen=True)
class ConversionContext:
    source_format: str
    target_format: str
    filename: str | None = None
    options: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class ConversionResult:
    output_bytes: bytes
    media_type: str
    extension: str
    warnings: list[str] = field(default_factory=list)


ConversionHandler = Callable[[bytes, ConversionContext], ConversionResult]


@dataclass(frozen=True)
class ConversionSpec:
    source_format: str
    target_format: str
    handler: ConversionHandler
    media_type: str
    extension: str
    stability: str
    notes: str = ""
