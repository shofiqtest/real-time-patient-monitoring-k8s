"""
Placeholder metrics endpoints
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()


@router.get("/")
async def get_metrics(db: AsyncSession = Depends(get_db)):
    """Get patient metrics"""
    return {"message": "Metrics endpoint"}


@router.get("/{patient_id}")
async def get_patient_metrics(patient_id: str, db: AsyncSession = Depends(get_db)):
    """Get metrics for specific patient"""
    return {"patient_id": patient_id, "metrics": []}
