"""Presentation layer - Vehicle Controller"""
import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.container import get_container
from app.shared.exceptions import ApplicationException, EntityNotFoundError
from app.application import (
    CreateVehicleRequest, VehicleResponse, VehicleDetailResponse,
    UpdateVehicleRequest, SearchVehicleQuery,
)
from app.presentation.dto_mappers import VehicleDTOMapper, PriceHistoryDTOMapper, SafetyProfileDTOMapper, ReliabilityProfileDTOMapper

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["vehicles"])


@router.post("/vehicles", response_model=VehicleResponse, status_code=201)
async def create_vehicle(request: CreateVehicleRequest, db: Session = Depends(get_db)):
    """Criar novo vehicle"""
    try:
        container = get_container()
        use_case = container.get_create_vehicle_use_case()
        
        vehicle = await use_case.execute(
            brand=request.brand,
            model=request.model,
            year=request.year,
            fuel_type=request.fuel_type,
            body_type=request.body_type,
            description=request.description,
        )
        
        return VehicleDTOMapper.to_response(vehicle)
    
    except ApplicationException as e:
        logger.error(f"Application error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/vehicles", response_model=list[VehicleResponse])
async def list_vehicles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """Listar todos vehicles"""
    try:
        container = get_container()
        use_case = container.get_list_vehicles_use_case()
        
        vehicles = await use_case.execute(skip, limit)
        return [VehicleDTOMapper.to_response(v) for v in vehicles]
    
    except Exception as e:
        logger.error(f"Error listing vehicles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Obter vehicle por ID"""
    try:
        container = get_container()
        use_case = container.get_get_vehicle_use_case()
        
        vehicle = await use_case.execute(vehicle_id)
        return VehicleDTOMapper.to_response(vehicle)
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting vehicle: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(vehicle_id: int, request: UpdateVehicleRequest, db: Session = Depends(get_db)):
    """Atualizar vehicle"""
    try:
        container = get_container()
        use_case = container.get_update_vehicle_use_case()
        
        vehicle = await use_case.execute(vehicle_id, request.description)
        return VehicleDTOMapper.to_response(vehicle)
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating vehicle: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/vehicles/{vehicle_id}", status_code=204)
async def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Deletar vehicle"""
    try:
        container = get_container()
        use_case = container.get_delete_vehicle_use_case()
        
        await use_case.execute(vehicle_id)
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting vehicle: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/vehicles/search", response_model=list[VehicleResponse])
async def search_vehicles(
    brand: str = Query(None),
    model: str = Query(None),
    year_from: int = Query(None),
    year_to: int = Query(None),
    fuel_type: str = Query(None),
    body_type: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Buscar vehicles com filtros avançados"""
    try:
        container = get_container()
        
        # Por enquanto, apenas filtro por brand
        if brand:
            use_case = container.get_search_vehicles_by_brand_use_case()
            vehicles = await use_case.execute(brand)
        else:
            use_case = container.get_list_vehicles_use_case()
            vehicles = await use_case.execute(skip, limit)
        
        return [VehicleDTOMapper.to_response(v) for v in vehicles]
    
    except Exception as e:
        logger.error(f"Error searching vehicles: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/vehicles/{vehicle_id}/detail", response_model=VehicleDetailResponse)
async def get_vehicle_detail(vehicle_id: int, db: Session = Depends(get_db)):
    """Obter detalhes completos do vehicle"""
    try:
        container = get_container()
        
        vehicle_use_case = container.get_get_vehicle_use_case()
        vehicle = await vehicle_use_case.execute(vehicle_id)
        
        price_use_case = container.get_get_price_history_use_case()
        price_history = await price_use_case.execute(vehicle_id)
        
        safety_use_case = container.get_get_safety_profile_use_case()
        safety_profile = await safety_use_case.execute(vehicle_id)
        
        reliability_use_case = container.get_get_reliability_use_case()
        reliability_profile = await reliability_use_case.execute(vehicle_id)
        
        return VehicleDetailResponse(
            vehicle=VehicleDTOMapper.to_response(vehicle),
            prices=PriceHistoryDTOMapper.to_response(price_history).records if price_history else None,
            safety_ratings=SafetyProfileDTOMapper.to_response(safety_profile).ratings if safety_profile else None,
            reliability=ReliabilityProfileDTOMapper.to_response(reliability_profile) if reliability_profile else None,
        )
    
    except EntityNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting vehicle detail: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
