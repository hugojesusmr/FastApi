import pdfplumber
import io
from fastapi import HTTPException, UploadFile
from app.schemas.pdf import PdfPageResponse, PdfExtractResponse, RegionRequest, RegionExtractResponse

class PdfService:
    async def extract_text(self, file: UploadFile) -> PdfExtractResponse:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
        try:
            content = await file.read()
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                pages = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    pages.append(PdfPageResponse(
                        page_number=i + 1,
                        text_content=text,
                        word_count=len(text.split())
                    ))
                return PdfExtractResponse(
                    filename=file.filename,
                    total_pages=len(pdf.pages),
                    pages=pages
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error procesando PDF: {str(e)}")

    async def extract_region(self, file: UploadFile, region: RegionRequest) -> RegionExtractResponse:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="El archivo debe ser un PDF")
        try:
            content = await file.read()
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                if region.page_number < 1 or region.page_number > len(pdf.pages):
                    raise HTTPException(status_code=400, detail="Número de página inválido")

                page = pdf.pages[region.page_number - 1]

                # Convertir coordenadas del canvas al espacio del PDF
                scale_x = page.width / region.pdf_width
                scale_y = page.height / region.pdf_height

                bbox = (
                    region.x0 * scale_x,
                    region.y0 * scale_y,
                    region.x1 * scale_x,
                    region.y1 * scale_y,
                )

                cropped = page.crop(bbox)

                # Intentar extraer tabla primero
                tables = cropped.extract_tables()
                if tables and len(tables) > 0:
                    table = tables[0]
                    # Limpiar celdas None
                    cleaned = [[cell or "" for cell in row] for row in table if any(cell for cell in row)]
                    if len(cleaned) > 1:
                        return RegionExtractResponse(
                            page_number=region.page_number,
                            type="table",
                            headers=cleaned[0],
                            rows=cleaned[1:]
                        )
                    elif len(cleaned) == 1:
                        return RegionExtractResponse(
                            page_number=region.page_number,
                            type="table",
                            headers=cleaned[0],
                            rows=[]
                        )

                # Si no hay tabla, extraer texto
                text = cropped.extract_text() or ""
                return RegionExtractResponse(
                    page_number=region.page_number,
                    type="text",
                    text=text
                )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error extrayendo región: {str(e)}")
