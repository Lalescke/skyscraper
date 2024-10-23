from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models.RealEstateTransaction import RealEstateTransaction

class StatisticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_average_value_by_postal_code(self):
        """
        Fetches average transaction values grouped by postal code.
        Returns a list of dictionaries, each containing the postal code and its average transaction value.
        """
        query = text("""
            SELECT
                postal_code,
                local_type,
                AVG(value) AS average_value
            FROM immo.real_estate_transaction
            WHERE value IS NOT NULL AND postal_code IS NOT NULL AND local_type = 'Appartement'
            GROUP BY postal_code, local_type
            ORDER BY average_value DESC
        """)

        result = self.db.execute(query)
        averages = [
            {
                "postal_code": row.postal_code,
                "average_value": float(row.average_value),
            } for row in result.fetchall()
        ]
        return averages

    def get_average_price_per_square_meter_by_postal_code(self):
        """
        Fetches average price per square meter for transactions of type 'Appartement',
        grouped by postal code. Returns a list of dictionaries, each containing the
        postal code and its average price per square meter.
        """
        query = text("""
            SELECT
                postal_code,
                AVG(value / real_surface) AS average_price_per_sqm
            FROM immo.real_estate_transaction
            WHERE value IS NOT NULL AND real_surface IS NOT NULL AND real_surface > 0 
                  AND postal_code IS NOT NULL AND local_type = 'Appartement'
            GROUP BY postal_code
            ORDER BY average_price_per_sqm DESC
        """)

        result = self.db.execute(query)
        averages_per_sqm = [
            {
                "postal_code": row['postal_code'],
                "average_price_per_sqm": float(row['average_price_per_sqm']),
            } for row in result.fetchall()
        ]
        return averages_per_sqm