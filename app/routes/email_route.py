from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from app.models.scan_model import ScanResult
from app.scanner.email_scanner import scan_email
from app.pdf.generator import generate_pdf
from app.core.security import require_role
import re

router = APIRouter()

def sanitize_filename(email: str) -> str:
    """Sanitize email to be used as a safe filename."""
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', email)

@router.get("/pdf/{email}", dependencies=[Depends(require_role(["admin", "analyste"]))])
def scan_email_pdf(email: str):
    try:
        result = scan_email(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    safe_filename = sanitize_filename(email)
    filename = f"rapport_{safe_filename}.pdf"
    generate_pdf(result.dict(), output_path=filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.get("/{email}", response_model=ScanResult, dependencies=[Depends(require_role(["admin", "analyste"]))])
def scan_email_route(email: str):
    try:
        return scan_email(email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
