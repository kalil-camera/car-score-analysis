"""Presentation layer - Safety Controller"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.container import get_container
from app.shared.exceptions import ApplicationException, EntityNotFoundError
from app.application import (
    AddSafetyRatingRequest, SafetyProfileResponse,
)
from app.presentation.dto_mappers import SafetyProfileDTOMapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["safety"])


@router.get("/vehicles/{vehicle_id}/safety", response_model=SafetyProfileResponse)
async def get_safety_profile(vehicle_id: int, db: Session = Depends(get_db)):
    """Obter safety profile"""
    try:
        container = get_container()
        use_case = container.get_get_safety_profile_use_case()
        
        safety_profile = await use_case.execute(vehicle_id)
        return SafetyProfileDTOMapper.to_response(safety_profile)
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting safety profile: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/vehicles/{vehicle_id}/safety", response_model=SafetyProfileResponse)
async def add_safety_rating(vehicle_id: int, request: AddSafetyRatingRequest, db: Session = Depends(get_db)):
    """Adicionar safety rating"""
    try:
        container = get_container()
        use_case = container.get_add_safety_rating_use_case()
        
        safety_profile = await use_case.execute(
            vehicle_id=vehicle_id,
            organization=request.organization,
            overall_score=request.overall_score,
            frontal_crash=request.frontal_crash,
            side_crash=request.side_crash,
            rollover=request.rollover,
            child_protection=request.child_protection,
            pedestrian_protection=request.pedestrian_protection,
        )
        
        return SafetyProfileDTOMapper.to_response(safety_profile)
    
    except ApplicationException as e:
        logger.error(f"Application error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding safety rating: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
