"""
Background task functions for document processing
"""
from datetime import datetime
from app.storage import JobManager
from app.models import Document
import random


def process_document(job_id: str, content: str, job_manager: JobManager, document: Document):
    job_manager.update_job_status(job_id, "processing")
    
    if document.type == "invoice":
        import time
        time.sleep(2)  # Simulate 2 second processing
        progress = random.randint(50, 99)
        job = job_manager.get_job(job_id)
        if job:
            job["progress"] = progress
            job["updated_at"] = datetime.now().isoformat()
            job["result"] = {
                "invoice_number": f"INV-{random.randint(1000, 9999)}",
                "amount": round(random.uniform(100, 10000), 2),
                "status": "processed"
            }
    
    elif document.type == "contract":
        import time
        time.sleep(3)  
        progress = random.randint(50, 99)
        job = job_manager.get_job(job_id)
        if job:
            job["progress"] = progress
            job["updated_at"] = datetime.now().isoformat()
            job["result"] = {
                "contract_number": f"CON-{random.randint(1000, 9999)}",
                "parties": ["Party A", "Party B"],
                "effective_date": str(datetime.now().date()),
                "status": "signed",
                "signed_by": ["Party A", "Party B"]
            }
    else:
        job_manager.update_job_status(job_id, "failed", {"error": f"Invalid document type: {document.type}"})
        return job_id
    
    return job_id


def finalize_job(job_id: str, job_manager: JobManager):
    import time
    time.sleep(0.5)
    job = job_manager.get_job(job_id)
    if job:
        job["progress"] = 100
        job["updated_at"] = datetime.now().isoformat()
        job["status"] = "completed"
    return job_id

 
    



    

