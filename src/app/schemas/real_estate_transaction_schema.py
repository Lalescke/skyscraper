from datetime import date
from pydantic import BaseModel
from typing import Optional

class RealEstateTransactionSchema(BaseModel):
    mutation_date: Optional[date] = None
    mutation_nature: Optional[str] = None
    value: Optional[float] = None
    postal_code: Optional[int] = None
    local_type: Optional[str] = None
    real_surface: Optional[int] = None
    main_rooms_number: Optional[int] = None
    land_surface: Optional[int] = None
