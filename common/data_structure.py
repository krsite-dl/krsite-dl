from pydantic import BaseModel, constr
from typing import Optional
import datetime

class Site(BaseModel):
    hostname: str | list[str]
    name: str
    location: constr(pattern=r"^(KR|JP|SG)$", max_length=2, min_length=2, strip_whitespace=True)


class ScrapperPayload(BaseModel):
    title: str
    shortDate: str
    mediaDate: datetime.datetime
    site: str
    series: Optional[str]
    writer: Optional[str]
    location: str
    media: list[str] | list[tuple[str, str]]


class DownloadPayload(BaseModel):
    media: list[str] | list[tuple[str, str]]
    directory: str
    date: datetime.datetime
    shortDate: Optional[str]
    location: str