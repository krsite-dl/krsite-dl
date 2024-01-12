from pydantic import BaseModel, constr
from typing import Optional
import datetime

class Site(BaseModel):
    hostname: str | list[str]
    name: str
    location: constr(pattern=r"^(KR|JP|SG)$", max_length=2, min_length=2, strip_whitespace=True)


class DownloadPayload(BaseModel):
    media: list[str] | list[tuple[str, str]]
    directory: str
    option: Optional[str]


class DataPayload(BaseModel):
    directory_format: list[str]
    media: list[str] | list[tuple[str, str]]
    option: Optional[str]