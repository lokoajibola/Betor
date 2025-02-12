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
url = "https://web.bet9ja.com/Sport/Default.aspx"
driver.get(url)

try:
    # Wait for the element to be clickable
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#panelOdds_NE > div.ng-scope.sp1 > div:nth-child(10) > div.pnlOddToday.ng-scope > span"))
    )

    # Click the element
    element.click()
    print("✅ Element clicked successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

# Allow time for content to load
time.sleep(5)  # Adjust if necessary

# Find all sports tables
events = driver.find_elements(By.XPATH, "//div[@ng-repeat='subEvent in sport.SottoEventiList']")

# List to store scraped data
bet_table = []


# Loop through each events
for event in events:
    tab_1 = []
# match = table_f_rows[-1]
    try:
        # Extract time
        time = event.find_element(By.XPATH, ".//div[@class='Time']").text.strip()

        teams = event.find_element(By.XPATH, ".//div[@class='Event ng-binding']").text.strip()

        tab_1 = [time, teams]
        odds_elements = event.find_elements(By.XPATH, ".//div[@class='odds']//div[contains(@class, 'odd')]")
        odds_list = []
        for odd in odds_elements:
            try:
                bet_type = odd.find_element(By.XPATH, ".//div[@class='oddsType']").get_attribute("title")
                bet_value = odd.find_elements(By.XPATH, ".//div")[1].text.strip()  # The second div contains the odd value
                # odds_list.append(f"{bet_type}: {bet_value}")
                odds_list.append(bet_value)
            except:
                # odds_list.append(f"{bet_type}: {bet_value}")
                # odds_list.append('N/A')
                continue  # Skip any missing elements
    # except:
        # odds_list = ["N/A"]
           
        tab_1.extend(odds_list)
        bet_table.append(tab_1)
    
    except Exception as e:
        print(f"Error extracting match data: {e}")

# Close the driver
driver.quit()

# Convert to DataFrame
columns = ["datetime", "teams", "1", "X", "2", "1X", "12", "2X", "O", "U"]
bet_table = pd.DataFrame(bet_table, columns=columns)

# Splitting the column into two based on '-'
bet_table[['home', 'away']] = bet_table['teams'].str.split('-', expand=True)
bet_table[['date', 'time']] = bet_table['datetime'].str.split(' ', expand=True)

# Dropping the original column (optional)
bet_table.drop(columns=['teams'], inplace=True)
bet_table.drop(columns=['datetime'], inplace=True)

bet_table = pd.DataFrame(bet_table) #, columns=columns)

# Save to CSV
csv_filename = "bet9ja_odds.csv"
bet_table.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")
