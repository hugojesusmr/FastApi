import pdfplumber
import io
import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import HTTPException, UploadFile
from app.schemas.pdf import PdfPageResponse, PdfExtractResponse, RegionRequest, RegionExtractResponse

_executor = ThreadPoolExecutor()

MIN_AREA_FOR_TABLE = 5000  # px² mínimo para intentar detectar tabla


def _extract_page(page, index: int) -> PdfPageResponse:
    text = page.extract_text() or ""
    return PdfPageResponse(
        page_number=index + 1,
        text_content=text,
        word_count=len(text.split())
    )


def _extract_text_sync(content: bytes, filename: str) -> PdfExtractResponse:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        pages = [_extract_page(page, i) for i, page in enumerate(pdf.pages)]
        return PdfExtractResponse(filename=filename, total_pages=len(pdf.pages), pages=pages)


def _extract_region_sync(content: bytes, region: RegionRequest) -> RegionExtractResponse:
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        if region.page_number < 1 or region.page_number > len(pdf.pages):
            raise ValueError("Número de página inválido")

        page = pdf.pages[region.page_number - 1]
        scale_x = page.width / region.pdf_width
        scale_y = page.height / region.pdf_height

        bbox = (
            region.x0 * scale_x,
            region.y0 * scale_y,
            region.x1 * scale_x,
            region.y1 * scale_y,
        )
        cropped = page.crop(bbox)

        area = abs(region.x1 - region.x0) * abs(region.y1 - region.y0)
        if area >= MIN_AREA_FOR_TABLE:
            tables = cropped.extract_tables()
            if tables:
                cleaned = [[cell or "" for cell in row] for row in tables[0] if any(cell for cell in row)]
                if cleaned:
                    return RegionExtractResponse(
                        page_number=region.page_number,
                        type="table",
                        headers=cleaned[0],
                        rows=cleaned[1:] if len(cleaned) > 1 else []
                    )

        text = cropped.extract_text() or ""
        return RegionExtractResponse(page_number=region.page_number, type="text", text=text)


class PdfService:
    async def extract_text(self, file: UploadFile) -> PdfExtractResponse:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="El archivo supera los 10MB")
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(_executor, _extract_text_sync, content, file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando PDF: {str(e)}")

    async def extract_region(self, file: UploadFile, region: RegionRequest) -> RegionExtractResponse:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
        content = await file.read()
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="El archivo supera los 10MB")
        try:
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(_executor, _extract_region_sync, content, region)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extrayendo región: {str(e)}")
