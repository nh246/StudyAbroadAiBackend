from fastapi import UploadFile, HTTPException
import pdfplumber
import io

async def parse_resume(file: UploadFile) -> str:
    """
    Parse text from a PDF resume.
    
    Args:
        file: The uploaded PDF file.
        
    Returns:
        Extracted text from the PDF.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF.")
    
    try:
        content = await file.read()
        text = ""
        
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
                    
        if not text.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be an image-based PDF.")
             
        return text.strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
