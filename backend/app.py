from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import json
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid

# Import the service layer
from services.classifier_service import GitHubStarClassifierService, ClassificationConfig, ClassificationResult

app = FastAPI(title="GitHub Star Classifier API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for jobs and results
jobs = {}
results = {}

# Setup templates
templates = Jinja2Templates(directory="templates")

class ClassificationRequest(BaseModel):
    token: str
    min_stars: int = 0
    exclude_forks: bool = True
    include_archived: bool = False

class ClassificationJob(BaseModel):
    job_id: str
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    total_repos: Optional[int] = None
    error: Optional[str] = None

class ClassificationResult(BaseModel):
    job_id: str
    repos: List[Dict[str, Any]]
    stats: Dict[str, Any]
    completed_at: datetime

@app.get("/")
async def root():
    return {"message": "GitHub Star Classifier API", "version": "1.0.0"}

@app.post("/classify", response_model=ClassificationJob)
async def start_classification(request: ClassificationRequest, background_tasks: BackgroundTasks):
    """Start a new classification job."""
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "processing",
        "created_at": datetime.now(),
        "completed_at": None,
        "error": None
    }
    
    background_tasks.add_task(process_classification, job_id, request)
    
    return ClassificationJob(**jobs[job_id])

@app.get("/jobs/{job_id}", response_model=ClassificationJob)
async def get_job_status(job_id: str):
    """Get the status of a classification job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return ClassificationJob(**jobs[job_id])

@app.get("/results/{job_id}", response_model=ClassificationResult)
async def get_results(job_id: str):
    """Get the results of a completed classification job."""
    if job_id not in results:
        if job_id not in jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        elif jobs[job_id]["status"] == "processing":
            raise HTTPException(status_code=202, detail="Job still processing")
        else:
            raise HTTPException(status_code=404, detail="No results available")
    
    return ClassificationResult(**results[job_id])

@app.get("/jobs")
async def list_jobs():
    """List all jobs."""
    return {"jobs": list(jobs.values())}

@app.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a job and its results."""
    if job_id in jobs:
        del jobs[job_id]
    if job_id in results:
        del results[job_id]
    return {"message": "Job deleted"}

async def process_classification(job_id: str, request: ClassificationRequest):
    """Process the classification job in the background."""
    try:
        # Create classifier service with config
        config = ClassificationConfig(
            token=request.token,
            min_stars=request.min_stars,
            exclude_forks=request.exclude_forks,
            include_archived=request.include_archived
        )

        print(f"Process task : {config}")
        classifier = GitHubStarClassifierService(config)
        result = classifier.classify_and_analyze()
        
        # Update job status
        jobs[job_id].update({
            "status": "completed",
            "completed_at": datetime.now(),
            "total_repos": result.total_repos
        })
        
        # Store results
        results[job_id] = {
            "job_id": job_id,
            "repos": result.repos,
            "stats": result.stats,
            "completed_at": result.completed_at
        }
        
    except Exception as e:
        jobs[job_id].update({
            "status": "failed",
            "error": str(e),
            "completed_at": datetime.now()
        })

@app.get("/view/{job_id}")
async def view_results(job_id: str):
    """View classification results as HTML page."""
    if job_id not in results:
        if job_id not in jobs:
            raise HTTPException(status_code=404, detail="Job not found")
        elif jobs[job_id]["status"] == "processing":
            return HTMLResponse(
                """
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Processing...</title>
                    <meta http-equiv="refresh" content="5">
                    <style>
                        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                        .container { text-align: center; }
                        .spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px; }
                        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="spinner"></div>
                        <h2>Processing your stars...</h2>
                        <p>This page will refresh automatically.</p>
                        <p>Status: Processing</p>
                    </div>
                </body>
                </html>
                """
            )
        else:
            raise HTTPException(status_code=404, detail="No results available")
    
    result = results[job_id]
    
    # Prepare data for template
    context = {
        "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_repos": result["stats"]["total_repos"],
        "total_stars": result["stats"]["total_stars"],
        "categories_count": len(result["stats"]["categories"]),
        "avg_stars": round(result["stats"]["avg_stars"], 1),
        "stats_json": json.dumps(result["stats"]),
        "repos_json": json.dumps(result["repos"]),
        "categories_json": json.dumps(result["stats"]["categories"]),
        "languages_json": json.dumps(result["stats"]["languages"])
    }
    
    return templates.TemplateResponse("results.html", {"request": None, **context})

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)