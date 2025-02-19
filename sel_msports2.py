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
# url = "https://www.msport.com/ng/web/sports/list/Soccer?d=Today"
url = "https://www.msport.com/ng/web/"

driver.get(url)

time.sleep(3)
sport_btn = driver.find_element(By.XPATH, '//span[contains(@class, "nav-item-inner") and contains(text(), "Sports")]')
sport_btn.click()

time.sleep(5)
today_button = driver.find_element(By.XPATH, '//span[@class="item-name" and contains(text(), "Today")]')
today_button.click()

time.sleep(5)
try:

    bet_table = []
    events = driver.find_elements(By.XPATH, '//div[(@class="m-event")]')
    timess = driver.find_elements(By.XPATH, '//span[contains(@class, "m-time")]')
    home_teamss = driver.find_elements(By.XPATH, '//div[contains(@class, "m-home-team")]')
    away_teamss = driver.find_elements(By.XPATH, '//div[contains(@class, "m-away-team")]')
    oddss = driver.find_elements(By.XPATH, '//div[contains(@class, "m-market")]')
    # Loop through each events
    
    # for i in range(len(timess)):
    for event in events:
        event_row = []
        
    # match = table_f_rows[-1]
        try:
            # Extract time
            # e_time = timess[i]
            time = event.find_element(By.XPATH, './/span[contains(@class, "m-time")]').text
            # (By.CSS_SELECTOR, ".span[class*='ui-team-scores-teams']")
            # teams = event.find_elements(By.CSS_SELECTOR, ".span[class*='ui-team-scores-teams']")
            
            # h_team = home_teamss[i]
            home = event.find_element(By.XPATH, './/div[contains(@class, "m-home-team")]').text
            # a_team = away_teamss[i]
            away = event.find_element(By.XPATH, './/div[contains(@class, "m-away-team")]').text
            # dashboard-game-block__teams  dashboard-game-block__team
  
            
            # e_odd = oddss[i] m-market m-market
            odds_elements = event.find_elements(By.XPATH, ".//div[contains(@class,'m-market m-market')]")
            odds_list = []
            odds_element = odds_elements[0]
            odds_element2 = odds_element.find_elements(By.XPATH, ".//div[contains(@class,'m-outcome')]")
            for odds in odds_element2:
                try:
                    bet_value = odds.find_element(By.XPATH, ".//div[contains(@class,'odds')]").text
                    # bet_value = odd.find_elements(By.XPATH, ".//div")[1].text.strip()  # The second div contains the odd value
                    odds_list.append(bet_value)
                except:
                    # odds_list.append(f"{bet_type}: {bet_value}")
                    # odds_list.append('N/A')
                    continue  # Skip any missing elements
        # except:
            # odds_list = ["N/A"]
            event_row.extend([time])
            event_row.extend([home])
            event_row.extend([away])
            event_row.extend(odds_list)
            bet_table.append(event_row)
        
        except Exception as e:
            print('next')
            # print(f"Error extracting match data: {e}")
    
    
    # time.sleep(30)
    # time.sleep(30)  # Adjust if necessary
    
    # Convert to DataFrame
    columns = ["time", "home","away", "1", "X", "2"] # , "G", "O", "U"]
    bet_table = pd.DataFrame(bet_table, columns=columns)
    
    
    # bet_table = pd.DataFrame(bet_table) #, columns=columns)
    
    # Save to CSV
    csv_filename = "msports_odds.csv"
    bet_table.to_csv(csv_filename, index=False)
    
    print(f"Data saved to {csv_filename}")
    
    # Close the driver
    driver.quit()

except Exception as e:
    print(f"❌ Error: {e}")

    # Close the driver
    driver.quit()