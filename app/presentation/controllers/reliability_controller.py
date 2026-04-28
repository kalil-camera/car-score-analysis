"""Presentation layer - Reliability Controller"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.container import get_container
from app.shared.exceptions import ApplicationException, EntityNotFoundError
from app.application import (
    UpdateReliabilityRequest, ReliabilityResponse,
)
from app.presentation.dto_mappers import ReliabilityProfileDTOMapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["reliability"])


@router.get("/vehicles/{vehicle_id}/reliability", response_model=ReliabilityResponse)
async def get_reliability(vehicle_id: int, db: Session = Depends(get_db)):
    """Obter reliability profile"""
    try:
        container = get_container()
        use_case = container.get_get_reliability_use_case()
        
        reliability_profile = await use_case.execute(vehicle_id)
        return ReliabilityProfileDTOMapper.to_response(reliability_profile)
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting reliability: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/vehicles/{vehicle_id}/reliability", response_model=ReliabilityResponse)
async def update_reliability(vehicle_id: int, request: UpdateReliabilityRequest, db: Session = Depends(get_db)):
    """Atualizar reliability profile"""
    try:
        container = get_container()
        use_case = container.get_update_reliability_use_case()
        
        reliability_profile = await use_case.execute(
            vehicle_id=vehicle_id,
            overall_score=request.overall_score,
            breakdown_frequency=request.breakdown_frequency,
            customer_satisfaction=request.customer_satisfaction,
            warranty_claims_rate=request.warranty_claims_rate,
            warranty_avg_cost=request.warranty_avg_cost,
        )
        
        return ReliabilityProfileDTOMapper.to_response(reliability_profile)
    
    except ApplicationException as e:
        logger.error(f"Application error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating reliability: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
