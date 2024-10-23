import csv
from datetime import datetime
from typing import Any

from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.models.RealEstateTransaction import RealEstateTransaction
from app.schemas.real_estate_transaction_schema import RealEstateTransactionSchema

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
import re

load_dotenv()


class RealEstateTransactionService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def extract_data(bien):
        gonext = False
        info1 = bien.find_element(By.XPATH, './/span[@class="ad-overview-details__ad-title ad-overview-details__ad-title--small"]')
        text = info1.text.strip()
        type_bien, nb_pieces, surface, code_postal = None,None,None, None

        if "Studio" in text:
            type_bien = "Appartement"
            nb_pieces = "1"
            match_surface = re.search(r"\b(\d+\s?m²)\b", text)
            if match_surface:
                surface = match_surface.group(1)
            else:
                gonext = True
        else:
            match = re.match(r"(appartement|maison)\s(\d+\s\w+)\s(\d+\s\w+)", text, re.IGNORECASE)
            if match:
                type_bien = match.group(1)
                nb_pieces = match.group(2)
                surface = match.group(3)
            else:
                gonext = True
                
        info2 = bien.find_element(By.XPATH, './/span[@class="ad-overview-details__address-title ad-overview-details__address-title--small"]')
        match = re.search(r"\b\d{5}\b", info2.text.strip())

        if match:
            code_postal = match.group()
        else:
            gonext = True

        prix = bien.find_element(By.XPATH, './/span[@class="ad-price__the-price"]').text.strip()
        if gonext == False and type_bien and nb_pieces and surface and code_postal and prix:
            return {
                'Type de bien': type_bien,
                'Nombre de pièces': re.sub(r'[^\d.]', '', nb_pieces),
                'Surface': re.sub(r'[^\d.]', '', surface),
                'Code postal': code_postal,
                'Prix': re.sub(r'[^\d.]', '', prix)
            }

    @staticmethod
    def click_next_page(driver, current_page):
        if current_page >= 10:
            return False
        
        try: 
            next_button = driver.find_element(By.XPATH, '//a[@class="btn goForward btn-primary pagination__go-forward-button"]')
        except NoSuchElementException:
            return False
        else:
            next_button.click()
            return True
        
    def scrap_seloger(self, request) -> list[dict[str, str | None | Any]]:

        url = f"""https://www.bienici.com/recherche/achat/{request["departement"]}/{request["type_bien"]}/{request["pieces"]}-pieces?prix-min={request["prix_min"]}&prix-max={request["prix_max"]}&surface-min={request["surface_min"]}&surface-max={request["surface_max"]}"""

        
        options = Options()
        options.headless = True
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)

        driver.get(url)
        time.sleep(2)

        driver.find_element(By.XPATH, '//span[@class="didomi-continue-without-agreeing"]').click()
        time.sleep(2)
        
        page_count = 0
        data = []
        next_page = True
        while next_page:
            page_count += 1
            time.sleep(2)
            biens = driver.find_elements(By.XPATH, '//article[@class="sideListItem"]')
            for bien in biens:
                row = RealEstateTransactionService.extract_data(bien)
                if row is not None:
                    # Calculate price per square meter if both price and surface are available
                    if row['Prix'] and row['Surface'] and float(row['Surface']) > 0:
                        price_per_sqm = float(row['Prix']) / float(row['Surface'])
                        row['Prix par mètre carré'] = price_per_sqm
                    else:
                        row['Prix par mètre carré'] = None
                    data.append(row)
            if RealEstateTransactionService.click_next_page(driver, page_count) == False:
                next_page = False

        driver.quit()
        return data

    def insert_from_gouv_data(self) -> None:
        """
        Fetch data from the data folder at the root of the project.
        Files must be dowloaded form the url given in ulrdata.txt in the data folder.
        Names of the files in data folder must match the ones of the 'files' list below.
        """
        files = [
                './data/valeursfoncieres-2023.txt',
                './data/valeursfoncieres-2022.txt',
                './data/valeursfoncieres-2021.txt',
                './data/valeursfoncieres-2020.txt',
                './data/valeursfoncieres-2019.txt',
                './data/valeursfoncieres-2018-s2.txt'
                 ]
        for file_path in files:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file, delimiter='|')
                next(reader)  # Skip header
                for row in reader:
                    try:
                        # Convert postal_code to integer, handle empty or invalid values
                        try:
                            postal_code_processed = int(row[16]) if row[16] else None
                        except ValueError:
                            print(f"Error processing postal code {row}: {e}")
                            postal_code_processed = None

                        selected_fields = RealEstateTransactionSchema(
                            mutation_date=datetime.strptime(row[8], "%d/%m/%Y").date() if row[8] else None,
                            mutation_nature=row[9],
                            value=float(row[10].replace(',', '.')) if row[10] else None,
                            postal_code=postal_code_processed,
                            local_type=row[36],
                            real_surface=int(row[38]) if row[38].isdigit() else None,
                            main_rooms_number=int(row[39]) if row[39].isdigit() else None,
                            land_surface=int(row[42]) if row[42].isdigit() else None
                        )
                        db_transaction = RealEstateTransaction(**selected_fields.dict(exclude_unset=True))
                        self.db.add(db_transaction)
                    except Exception as e:
                        # Handle or log the error appropriately
                        print(f"Error processing row {row}: {e}")
            self.db.commit()