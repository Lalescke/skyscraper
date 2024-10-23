from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.statistics_service import StatisticsService

router = APIRouter()


@router.get("/real_estate/stats", response_model=None, tags=["data"], response_description="Sends back data from different sources")
def insert_csv(
    db: Session = Depends(get_db),
    departement: Optional[str] = Query(None, description="Departure date and time"),
    type_bien: Optional[str] = Query(None, description="Return date and time"),
    pieces: Optional[str] = Query(None, description="Departure location"),
    prix_min: Optional[str] = Query(None, description="Destination location"),
    prix_max: Optional[str] = Query(None, description="Destination location"),
    surface_min: Optional[str] = Query(None, description="Destination location"),
    surface_max: Optional[str] = Query(None, description="Maximum price")):

    statistics_service = StatisticsService(db)

    try:
        return statistics_service.get_transaction_statistics(
            {"departement": departement,
             "type_bien": type_bien,
             "pieces": pieces,
             "prix_min": prix_min,
             "prix_max": prix_max,
             "surface_min": surface_min,
             "surface_max": surface_max
             }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))