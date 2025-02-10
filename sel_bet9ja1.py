# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 05:11:50 2025

@author: LK
"""

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening browser (optional)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize Chrome WebDriver
# service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome() # service=service, options=options)

# Open Bet9ja Sports page
url = "https://sports.bet9ja.com/"
driver.get(url)

# Allow time for content to load
time.sleep(60)  # Adjust if necessary

# Find all sports tables
sports_tables = driver.find_elements(By.CLASS_NAME, "sports-table")

# List to store scraped data
match_data = []

# Loop through each sports table
# for table in sports_tables:
table_f_rows = driver.find_elements(By.CLASS_NAME, "table-f")  # Get all 
# Loop through each match entry
for match in table_f_rows:
# match = table_f_rows[-1]
    try:
        # Extract time
        time_element = WebDriverWait(match, 10).until(
                EC.presence_of_element_located((By.XPATH, ".//div[contains(@class, 'sports-table__time')]//span")))
        # time_element = match.find_element(By.CLASS_NAME, "sports-table__time")
        match_time = time_element.text.strip()
    
        # Extract teams
        home_team = match.find_element(By.CLASS_NAME, "sports-table__home").text.strip()
        away_team = match.find_element(By.CLASS_NAME, "sports-table__away").text.strip()
    
        # Extract odds
        odds_elements = match.find_elements(By.CLASS_NAME, "sports-table__odds-item")
        odds = [odds.text.strip() for odds in odds_elements[:15]]  # Collect odds list
    
        # Append match details to list
        m_data = [match_time, home_team, away_team]
        m_data.extend(odds)
        match_data.append(m_data)
    
    except Exception as e:
        print(f"Error extracting match data: {e}")

# Close the driver
driver.quit()

# Convert to DataFrame
columns = ["Time", "Home Team", "Away Team", "Odd 1", "Odd X", "Odd 2"]
df = pd.DataFrame(match_data) #, columns=columns)

# Save to CSV
csv_filename = "bet9ja_odds.csv"
df.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
