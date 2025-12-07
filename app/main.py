"""FastAPI application entry point and endpoint definitions"""
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.models import Document, uploadResponse, processRequest, processResponse
from app.storage import JobManager
from app.background import process_document, finalize_job

# Initialize FastAPI app
app = FastAPI(title="Async Document Processing API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize storage
job_manager = JobManager()


@app.post("/upload", response_model=uploadResponse)
async def upload_document(document: Document, background_tasks: BackgroundTasks):
    job_id = job_manager.create_job(document.type, str(document.content), document.metaData)
    
    # Add background tasks
    background_tasks.add_task(process_document, job_id, str(document.content), job_manager, document)
    background_tasks.add_task(finalize_job, job_id, job_manager)
    
    return uploadResponse(
        job_id=job_id,
        message="Document received. Processing started.",
        timestamp=datetime.now().isoformat()
    )


@app.post("/process", response_model=processResponse)
async def process_document_endpoint(request: processRequest):
    job = job_manager.get_job(request.job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return processResponse(
        job_id=job["job_id"],
        status=job["status"],
        result=job.get("result"),
        progress=job["progress"],
        created_at=job["created_at"],
        updated_at=job["updated_at"]
    )


@app.get("/status/{job_id}", response_model=processResponse)
async def get_status(job_id: str):
    job = job_manager.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return processResponse(
        job_id=job["job_id"],
        status=job["status"],
        result=job.get("result"),
        progress=job["progress"],
        created_at=job["created_at"],
        updated_at=job["updated_at"]
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}
