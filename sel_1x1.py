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
from time import sleep


# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run without opening browser (optional)
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# Initialize Chrome WebDriver
# service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome() # service=service, options=options)

# Open Bet9ja Sports page
url = "https://1xbet.ng/en/live/football"
driver.get(url)

try:
    # Wait for the element to be clickable
    # element = WebDriverWait(driver, 15).until(
    #     # EC.element_to_be_clickable((By.CSS_SELECTOR, "#panelOdds_NE > div.ng-scope.sp1 > div:nth-child(10) > div.pnlOddToday.ng-scope > span"))
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="__BETTING_APP__"]/div[2]/div/div/div[2]/main/div[2]/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/div[2]/div/div/div/ul/li[2]/button/span/span')))
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Upcoming events"]')))
    
    

    # Click the element
    element.click()
    print("✅ Element clicked successfully!")

except Exception as e:
    print(f"❌ Error: {e}")

# Allow time for content to load
time.sleep(5)  # Adjust if necessary

# events = driver.find_elements(By.CSS_SELECTOR, ".ui-dashboard-champ.ui-dashboard-champ--theme-gray.dashboard-champ.dashboard__champ")
# events = driver.find_elements(By.XPATH, "//div[@ng-repeat='subEvent in sport.SottoEventiList']")
events = driver.find_elements(By.CSS_SELECTOR, "li[class*='dashboard__champ']")
# List to store scraped data
bet_table = []
timess = driver.find_elements(By.XPATH, './/span[contains(@class, "dashboard-game-block__info")]')
teamss = driver.find_elements(By.XPATH, './/span[contains(@class, "dashboard-game-block__teams")]')
oddss = driver.find_elements(By.XPATH, './/span[contains(@class, "dashboard-markets__group")]')
# Loop through each events

for i in range(len(timess)):
# for event in events:
    event_row = []
    
# match = table_f_rows[-1]
    try:
        # Extract time
        e_time = timess[i]
        time = e_time.find_element(By.XPATH, './/span[contains(@class, "dashboard-game-info__time")]').text
        # (By.CSS_SELECTOR, ".span[class*='ui-team-scores-teams']")
        # teams = event.find_elements(By.CSS_SELECTOR, ".span[class*='ui-team-scores-teams']")
        
        e_team = teamss[i]
        teams = e_team.find_elements(By.XPATH, ".//div[contains(@class, 'dashboard-game-block__team')]")
        # dashboard-game-block__teams  dashboard-game-block__team
        teams_list = []
        for team in teams:
            team = team.find_element(By.XPATH, ".//span[contains(@class,'dashboard-game-team-info__name')]").text.strip()
            teams_list.append(team)
        
        e_odd = oddss[i]
        odds_elements = e_odd.find_elements(By.XPATH, ".//button[contains(@class,'dashboard-markets__item')]")
        odds_list = []
        for odd in odds_elements:
            try:
                bet_value = odd.find_element(By.XPATH, ".//span[contains(@class,'ui-market__value')]").text
                # bet_value = odd.find_elements(By.XPATH, ".//div")[1].text.strip()  # The second div contains the odd value
                odds_list.append(bet_value)
            except:
                # odds_list.append(f"{bet_type}: {bet_value}")
                # odds_list.append('N/A')
                continue  # Skip any missing elements
    # except:
        # odds_list = ["N/A"]
        event_row.extend([time])
        event_row.extend(teams_list)
        event_row.extend(odds_list)
        bet_table.append(event_row)
    
    except Exception as e:
        print('next')
        # print(f"Error extracting match data: {e}")


# time.sleep(30)
# time.sleep(30)  # Adjust if necessary

# Convert to DataFrame
columns = ["time", "home","away", "1", "X", "2"]
bet_table = pd.DataFrame(bet_table, columns=columns)


bet_table = pd.DataFrame(bet_table) #, columns=columns)

# Save to CSV
csv_filename = "1xbet_odds.csv"
bet_table.to_csv(csv_filename, index=False)

print(f"Data saved to {csv_filename}")


# Close the driver
driver.quit()