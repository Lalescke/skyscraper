from sqlalchemy import Column, String, Date, Integer, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.models.BaseModel import BaseModel

class RealEstateTransaction(BaseModel):
    __tablename__ = "real_estate_transaction"
    __table_args__ = {"schema": "immo"}

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    mutation_date = Column(Date)  # Date mutation
    mutation_nature = Column(String)  # Nature mutation
    value = Column(Float)  # Valeur fonciere
    postal_code = Column(Integer)  # Code postal
    local_type = Column(String)  # Type local
    real_surface = Column(Integer, nullable=True)  # Surface reelle bati
    main_rooms_number = Column(Integer)  # Nombre pieces principales
    land_surface = Column(Integer)  # Surface terrain
