

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from pathlib import Path
import uvicorn

# Import our 4-part architecture
from reader import PDFReader
from brain import KNOWLEDGE_BASE, process_all_interventions
from price_finder import get_price_for_material
from report_generator import create_pdf_report


# Initialize FastAPI app
app = FastAPI(
    title="Road Safety Estimator Tool",
    description="AI-powered cost estimation for road safety interventions",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create necessary directories
UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("outputs")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize the Reader
pdf_reader = PDFReader()


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the HTML frontend"""
    try:
        # Look for index.html in the current directory
        html_path = Path("index.html")
        if not html_path.exists():
            # If not found, return helpful error
            return HTMLResponse(
                content="""
                <html>
                <head><title>File Not Found</title></head>
                <body style="font-family: Arial; padding: 50px; text-align: center;">
                    <h1> Frontend File Not Found</h1>
                    <p>Could not find <code>index.html</code> in the project directory.</p>
                    <p>Please ensure <code>index.html</code> is in the same folder as <code>main.py</code></p>
                </body>
                </html>
                """,
                status_code=404
            )
        
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except Exception as e:
        return HTMLResponse(
            content=f"""
            <html>
            <head><title>Error</title></head>
            <body style="font-family: Arial; padding: 50px; text-align: center;">
                <h1> Error Loading Frontend</h1>
                <p>{str(e)}</p>
            </body>
            </html>
            """,
            status_code=500
        )


@app.post("/upload-report/")
async def upload_report(file: UploadFile = File(...)):
 
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    # Save uploaded file
    upload_path = UPLOAD_DIR / file.filename
    try:
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
    try:
        # PART 1: THE READER
        # Extract text and find intervention sentences
        print("Step 1: Reading PDF and extracting interventions...")
        found_interventions = pdf_reader.process_pdf(str(upload_path), KNOWLEDGE_BASE)
        
        if not found_interventions:
            raise HTTPException(
                status_code=422,
                detail="No road safety interventions found in the uploaded PDF"
            )
        
        print(f"Found {len(found_interventions)} potential interventions")
        
        # PART 2: THE BRAIN
        # Process interventions and calculate quantities
        print("Step 2: Processing interventions through Brain...")
        processed_interventions = process_all_interventions(found_interventions)
        
        if not processed_interventions:
            raise HTTPException(
                status_code=422,
                detail="Could not process any interventions from the PDF"
            )
        
        print(f"Processed {len(processed_interventions)} interventions")
        
        # PART 3: THE PRICE FINDER
        # Add cost information to each intervention
        print("Step 3: Fetching prices...")
        costed_items = []
        for item in processed_interventions:
            rate = get_price_for_material(item['material_name'])
            cost = item['quantity'] * rate
            
            costed_items.append({
                'material_name': item['material_name'],
                'quantity': item['quantity'],
                'unit': item['unit'],
                'rate': rate,
                'cost': cost,
                'intervention_type': item['intervention_type']
            })
        
        # Calculate summary
        total_cost = sum(item['cost'] for item in costed_items)
        print(f"Total estimated cost: INR {total_cost:,.2f}")
                # PART 4: THE REPORT GENERATOR
        # Generate final PDF report
        print("Step 4: Generating PDF report...")
        
        # Create safe filename without special characters
        base_name = Path(file.filename).stem
        safe_base = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in base_name)
        output_filename = f"cost_estimate_{safe_base}.pdf"
        output_path = OUTPUT_DIR / output_filename
        
        create_pdf_report(costed_items, str(output_path))
        
        print(f"Report generated successfully: {output_filename}")
        
        # Return the generated PDF with proper encoding
        from urllib.parse import quote
        
        return FileResponse(
            path=str(output_path),
            media_type="application/pdf",
            filename=output_filename,
            headers={
                "Content-Disposition": f'attachment; filename="{output_filename}"; filename*=UTF-8\'\'{quote(output_filename)}'
            }
        )

        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
    
    finally:
        # Cleanup uploaded file
        if upload_path.exists():
            upload_path.unlink()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Road Safety Estimator Tool",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Road Safety Estimator Tool - National Hackathon 2025")
    print("=" * 60)
    print("\nStarting FastAPI server...")
    print("Frontend: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
