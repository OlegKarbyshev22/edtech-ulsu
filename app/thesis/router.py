from fastapi import APIRouter
from app.thesis.services.pipeline import ThesisPipelineService
from pydantic import BaseModel

router = APIRouter()

class ScanFoldersRequest(BaseModel):
    folders: list[str]

@router.post("/sending_paths")
def path(request: ScanFoldersRequest):
    pipeline = ThesisPipelineService()
    return pipeline.run(request.folders)