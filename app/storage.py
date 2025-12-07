"""
In-Memory Storage Implementation to track jobs
"""
from typing import Dict, Optional
from datetime import datetime
import C


class JobManager:
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}

    def create_job(self, doc_type: str, content: str, metaData: Optional[dict] = None) -> str:
        job_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        self.jobs[job_id] = {
            "job_id": job_id,
            "status": "pending",
            "progress": 0,
            "created_at": now,
            "updated_at": now,
            "type": doc_type,
            "metaData": metaData,
            "content": content,
            "result": None
        }
        return job_id
    
    def get_job(self, job_id: str) -> Optional[Dict]:
        return self.jobs.get(job_id)
    
    def update_job_status(self, job_id: str, status: str, result: Optional[Dict] = None):  
        job = self.jobs.get(job_id)
        if job:
            job["status"] = status
            job["updated_at"] = datetime.now().isoformat()
            if result is not None:
                job["result"] = result
    
    def delete_job(self, job_id: str):
        if job_id in self.jobs:
            del self.jobs[job_id]
