"""Presentation layer - Pricing Controller"""
import logging
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.container import get_container
from app.shared.exceptions import ApplicationException, EntityNotFoundError
from app.application import (
    AddPriceRequest, PriceHistoryResponse, PriceStatisticsResponse,
)
from app.presentation.dto_mappers import PriceHistoryDTOMapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["prices"])


@router.get("/vehicles/{vehicle_id}/prices", response_model=PriceHistoryResponse)
async def get_price_history(vehicle_id: int, db: Session = Depends(get_db)):
    """Obter histórico de preços"""
    try:
        container = get_container()
        use_case = container.get_get_price_history_use_case()
        
        price_history = await use_case.execute(vehicle_id)
        return PriceHistoryDTOMapper.to_response(price_history)
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting price history: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/vehicles/{vehicle_id}/prices", response_model=PriceHistoryResponse)
async def add_price(vehicle_id: int, request: AddPriceRequest, db: Session = Depends(get_db)):
    """Adicionar novo preço"""
    try:
        container = get_container()
        use_case = container.get_add_price_use_case()
        
        price_history = await use_case.execute(
            vehicle_id=vehicle_id,
            price_amount=request.price,
            source=request.source,
            market_type=request.market_type,
            currency=request.currency,
        )
        
        return PriceHistoryDTOMapper.to_response(price_history)
    
    except ApplicationException as e:
        logger.error(f"Application error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error adding price: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/vehicles/{vehicle_id}/prices/stats", response_model=PriceStatisticsResponse)
async def get_price_statistics(vehicle_id: int, db: Session = Depends(get_db)):
    """Obter estatísticas de preço"""
    try:
        container = get_container()
        use_case = container.get_get_price_statistics_use_case()
        
        stats = await use_case.execute(vehicle_id)
        return PriceStatisticsResponse(
            count=stats["count"],
            average=stats["average"],
            min=stats["min"],
            max=stats["max"],
        )
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting price statistics: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
