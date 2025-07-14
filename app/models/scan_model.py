from pydantic import BaseModel
from typing import List

class SourceData(BaseModel):
    source: str
    data: List[str]

class ScanResult(BaseModel):
    email: str
    valid: bool
    summary: str
    sources: List[SourceData]
    sensitive: bool
