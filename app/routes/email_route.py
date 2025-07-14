from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.models.scan_model import ScanResult
from app.scanner.email_scanner import scan_email
from app.pdf.generator import generate_pdf
from app.core.security import require_role

router = APIRouter()

@router.get("/{email}", response_model=ScanResult, dependencies=[Depends(require_role(["admin", "analyste"]))])
def scan_email_route(email: str):
    return scan_email(email)

@router.get("/pdf/{email}", dependencies=[Depends(require_role(["admin", "analyste"]))])
def scan_email_pdf(email: str):
    result = scan_email(email)
    filename = f"rapport_{email}.pdf"
    generate_pdf(result.dict(), output_path=filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)
