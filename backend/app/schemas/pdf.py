from pydantic import BaseModel
from typing import List, Optional

class PdfPageResponse(BaseModel):
    page_number: int
    text_content: str
    word_count: int

class PdfExtractResponse(BaseModel):
    filename: str
    total_pages: int
    pages: List[PdfPageResponse]

class RegionRequest(BaseModel):
    page_number: int
    x0: float
    y0: float
    x1: float
    y1: float
    pdf_width: float
    pdf_height: float

class CellData(BaseModel):
    row: int
    col: int
    value: str

class RegionExtractResponse(BaseModel):
    page_number: int
    type: str  # "table" o "text"
    text: Optional[str] = None
    headers: Optional[List[str]] = None
    rows: Optional[List[List[str]]] = None
