# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:38:58 2025

@author: LK
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# C:\Users\MY PC\Downloads\chrome-win64https://www.sportybet.com/ng/sport/football/
# Set up Selenium WebDriver https://www.sportybet.com/ng/sport/football/today
driver = webdriver.Chrome()  # Ensure you have the Chrome WebDriver installed
driver.get("https://www.sportybet.com/ng/sport/football/today")  # SportyBet Nigeria URL https://www.sportybet.com/ng/sport/football/today
driver.maximize_window()

# Wait for the matches to load
# WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "m-table match-table")))
time.sleep(3)
# Extract all match elements
match_elements = driver.find_elements(By.CLASS_NAME, "m-table-row")

# if match_elements:
#     match = match_elements[0]  # Pick the first element
# List to store scraped data
data = []

for match in match_elements: # m-table-cell left-team-cell
    try:
        # Get match date (if available)
        # date_element = match.find_element(By.CLASS_NAME, "date").text if "date-row" in match.get_attribute("class") else None

        # Get match details
        time = match.find_element(By.CLASS_NAME, "clock-time").text.strip()
        game_id = match.find_element(By.CLASS_NAME, "game-id").text.replace("ID: ", "").strip()
        home_team = match.find_element(By.CLASS_NAME, "home-team").text.strip()
        away_team = match.find_element(By.CLASS_NAME, "away-team").text.strip()

        # Get odds
        odds_elements = match.find_elements(By.CLASS_NAME, "m-outcome-odds")
        odds_1 = odds_elements[0].text if len(odds_elements) > 0 else "N/A"
        odds_x = odds_elements[1].text if len(odds_elements) > 1 else "N/A"
        odds_2 = odds_elements[2].text if len(odds_elements) > 2 else "N/A"
        over_odds = odds_elements[3].text if len(odds_elements) > 3 else "N/A"
        under_odds = odds_elements[4].text if len(odds_elements) > 4 else "N/A"

        # Store extracted data
        data.append({
            # "Date": date_element,
            "Time": time,
            "Game ID": game_id,
            "Home Team": home_team,
            "Away Team": away_team,
            "1": odds_1,
            "X": odds_x,
            "2": odds_2,
            "Over": over_odds,
            "Under": under_odds
        })
        
    except Exception as e:
        print(f"Skipping a row due to error: {e}")

# # Close browser
# driver.quit()

# Convert Data to DataFrame
df = pd.DataFrame(data)
# df = pd.DataFrame(data, columns=["Date/Time", "Team 1", "Team 2", "Odd 1", "Odd X", "Odd 2"])

# Save Data to CSV
df.to_csv("sportybet_odds.csv", index=False)

# Print Data
# print(df)

# Close WebDriver
driver.quit()
