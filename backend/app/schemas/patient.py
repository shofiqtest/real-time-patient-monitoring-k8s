"""
Pydantic schemas for patient endpoints
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid


class PatientCreate(BaseModel):
    """Patient creation schema"""
    
    name: str = Field(..., min_length=1, max_length=255)
    age: Optional[int] = Field(None, ge=0, le=150)
    medical_id: str = Field(..., min_length=1, max_length=100)
    gender: Optional[str] = None
    notes: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "John Doe",
                "age": 45,
                "medical_id": "MED-12345",
                "gender": "M",
                "notes": "Patient admitted for routine checkup"
            }
        }


class PatientResponse(PatientCreate):
    """Patient response schema"""
    
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
