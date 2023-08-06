from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel
from typing_extensions import Literal


class CrunchyFile(BaseModel):
    path: str
    file: Literal["first_read", "second_read", "spring"]
    checksum: str
    algorithm: Literal["sha1", "md5", "sha256"]
    updated: Optional[date]


class CrunchyMetadata(BaseModel):
    files: List[CrunchyFile]
