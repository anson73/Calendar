import os
import sys
import time
import pandas as pd
import logging

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import date, timedelta

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from numerology.numerology import numerology

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class bbg_bids:
    def __init__(self):
        self.working_directory = os.path.dirname(os.path.abspath(__file__))
        self.today = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        self.new_folder = os.path.join(self.working_directory, "bbg_bidx", self.today)
        os.makedirs(self.new_folder, exist_ok=True)

    def run(self):
        self.extract()
        self.analyse()

    def extract(self):
        '''
        Get bloomberg top 500 richest people
        '''
        logger.info(f"Starting: Extracting Data")

        try:
            # Get data and save in files. 
            options = Options()
            options.add_argument("--start-maximized")

            driver = webdriver.Firefox(options)
            driver.get("https://www.bloomberg.com/billionaires/")
            wait = WebDriverWait(driver, 10)

            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.table-chart")))

            with open(os.path.join(self.new_folder, f'bbg_{self.today}.txt'), 'w', encoding='utf-8') as file:
                file.write(element.text)
            
            with open(os.path.join(self.new_folder, f'bbg_html_{self.today}.txt'), 'w', encoding='utf-8') as file:
                file.write(element.get_attribute("outerHTML"))

        finally:
            driver.quit()

        logger.info(f"Starting: Cleaning Data")
        # Clean data 
        with open(os.path.join(self.new_folder, f'bbg_html_{self.today}.txt'), "r") as file:
            content = file.read()

        soup = BeautifulSoup(content, "html.parser")
        
        rows = []
        for row in soup.select(".table-row"):
            cells = row.select(".table-cell")

            data = {
                "Rank": cells[0].get_text(strip=True),
                "Name": cells[1].get_text(strip=True),
                "Net Worth": cells[2].get_text(strip=True),
                "1-Day Change": cells[3].get_text(strip=True),
                "1-Year Change": cells[4].get_text(strip=True),
                "Country": cells[5].get_text(strip=True),
                "Industry": cells[6].get_text(strip=True)
            }
            
            rows.append(data)

        df = pd.DataFrame(rows)

        df["Birthday"] = df["Name"].apply(self.get_birthdate)

        data_file = os.path.join(self.new_folder, 'bbg.csv')
        df.to_csv(data_file, index=False)

        logger.info(f"Saved file {data_file}")
    
    def get_birthdate(self, name):
        """
        Query Wikidata for a person's date of birth using SPARQL.
        Returns ISO-formatted date string or None.
        """
        logger.info(f"Getting birthday for: {name}")

        endpoint = "https://query.wikidata.org/sparql"
        
        query = f"""
        SELECT ?dob WHERE {{
        ?person wdt:P31 wd:Q5;
                rdfs:label "{name}"@en;
                wdt:P569 ?dob.
        }}
        LIMIT 1
        """
        
        headers = {"Accept": "application/sparql-results+json"}
        r = requests.get(endpoint, params={"query": query}, headers=headers)
        
        if r.status_code != 200:
            return None
        
        data = r.json()["results"]["bindings"]
        if not data:
            return None
        
        birthday = data[0]["dob"]["value"].split("T")[0] # ISO Date

        logger.info(f"{name}, Birthday: {birthday}")
        r.close()
        time.sleep(0.5)

        return birthday

    def analyse(self):
        '''
        Analyse data
        '''
        logger.info("Analysing data")
        df = pd.read_csv(os.path.join(self.new_folder, 'bbg.csv'))
        df = df[~df["Birthday"].isna()]
        
        # Analyse day born
        logger.info("Analysing day born")
        df["Day"] = pd.to_datetime(df["Birthday"], format="%Y-%m-%d", errors="coerce").dt.day
        day_result = df["Day"].value_counts().sort_index()
        # day_counts = day_counts.sort_values()
        day_result.to_csv(os.path.join(self.new_folder, f"day_{self.today}.csv"))
        
        # Analyse lifepath
        logger.info("Analysing lifepath")
        utils = numerology()
        # df["test"] = pd.to_datetime(df["Birthday"], format="%Y-%m-%d", errors="coerce")
        df["lifepath"] = df["Birthday"].apply(utils.reduce_wrapper)
        lp_result = df["lifepath"].value_counts().sort_index()
        lp_result.to_csv(os.path.join(self.new_folder, f"lp_{self.today}.csv"))

if __name__ == '__main__':
    bbg_bids().run()
