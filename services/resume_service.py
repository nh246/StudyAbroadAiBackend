from fastapi import UploadFile, HTTPException
import fitz  # PyMuPDF
import io

async def parse_resume(file: UploadFile) -> str:
    """
    Parse text from a PDF resume using PyMuPDF (edge-compatible).
    
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
        
        # Open PDF with PyMuPDF (fitz)
        pdf_document = fitz.open(stream=content, filetype="pdf")
        
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            extracted = page.get_text()
            if extracted:
                text += extracted + "\n"
        
        pdf_document.close()
                    
        if not text.strip():
             raise HTTPException(status_code=400, detail="Could not extract text from the PDF. It might be an image-based PDF.")
             
        return text.strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")
