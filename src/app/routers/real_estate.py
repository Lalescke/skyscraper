from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.real_estate_service import RealEstateTransactionService

router = APIRouter()

@router.get("/real_estate/compare", response_model=None, tags=["collect"], response_description="Fetch and data from different sources")
def collect_data(
    departure_at: Optional[datetime] = Query(None, description="Departure date and time"),
    back_at: Optional[datetime] = Query(None, description="Return date and time"),
    from_location: Optional[str] = Query(None, description="Departure location"),
    to_location: Optional[str] = Query(None, description="Destination location"),
    price_max: Optional[float] = Query(None, description="Maximum price")
):
    # query_params = FetchAndCompareRequest(
    #     departure_at=departure_at,
    #     back_at=back_at,
    #     from_location=from_location,
    #     to_location=to_location,
    #     price_max=price_max
    # )
    # scrapper_service = ScrapperService()
    try:
        return None
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/real_estate/scrap_seloger", response_model=None, tags=["data"], response_description="Sends back data from different sources")
def insert_csv(
    db: Session = Depends(get_db),
    departement: Optional[str] = Query(None, description="Departure date and time"),
    type_bien: Optional[str] = Query(None, description="Return date and time"),
    pieces: Optional[str] = Query(None, description="Departure location"),
    prix_min: Optional[str] = Query(None, description="Destination location"),
    prix_max: Optional[str] = Query(None, description="Destination location"),
    surface_min: Optional[str] = Query(None, description="Destination location"),
    surface_max: Optional[str] = Query(None, description="Maximum price")):

    real_estate_service = RealEstateTransactionService(db)

    try:
        return real_estate_service.scrap_seloger(
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
    
@router.post("/real_estate/insert_from_gouv_data", response_model=None, tags=["data"], response_description="Insertion complete")
def insert_from_gouv_data(db: Session = Depends(get_db)):
    real_estate_service = RealEstateTransactionService(db)
    try:
        return real_estate_service.insert_from_gouv_data()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))