"""
This is a web scraper for Sweetgreen Restaurants 
"""

# Importing required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
from datetime import datetime
current_date = datetime.now().date()

# Setting options for Chrome Webdriver
chrome_options = Options()
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("−−lang=en-US")
driver = webdriver.Chrome(chrome_options)
driver.maximize_window()

wait = WebDriverWait(driver, 120) # Sets a wait time for driver before throwing an exception

while True:
    try:
        driver.get("https://order.sweetgreen.com/locations")
        wait.until(EC.presence_of_element_located((By.XPATH, '//input[@data-testid="location-search-input"]'))) # Waits till the element with specified class name appears on the page
        break
    except Exception as e:
        continue

# Search for the given address
address_search = driver.find_element(By.XPATH, '//input[@data-testid="location-search-input"]') # Finding an element with provided class name
address_search.click()
address_search.send_keys('Austin')

submit_button = driver.find_element(By.XPATH, '//button[@data-testid="locationsearch.submit-button"]')
submit_button.click()
while True:
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//main/div/div[2]/div[2]/div[2]/div/ul[1]/li[1]/button')))
        pick_button = driver.find_element(By.XPATH, '//main/div/div[2]/div[2]/div[2]/div/ul[1]/li[1]/button')
        pick_button.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-testid="menu.categories.wrapper"]/div[1]/div[1]/div')))
        break
    except Exception as e:
        continue

menu_categories = driver.find_elements(By.XPATH, '//div[@data-testid="menu.categories.wrapper"]/div[1]/div[1]/div')

output_array = [['item_id','company_name','item_name','protein_option','price','description','added_date', 'last_modified_date', 'discontinued_date']]

for menu_category in menu_categories:
    div_menu = menu_category.find_element(By.XPATH, './/div[contains(@data-testid, "menupage") and contains(@data-testid, "-container")]')
    if div_menu.get_attribute('data-testid') == 'menupage.custom-container':
        continue
    menu_category_name = div_menu.find_element(By.XPATH, './/div[contains(@data-testid, "menupage") and contains(@data-testid, "category-header")]').text
    sub_menu_category_list = div_menu.find_elements(By.XPATH, './/div[2]/div/ul[1]/li')
    for sub_menu_category in sub_menu_category_list:
        sub_menu_category_name = sub_menu_category.find_element(By.XPATH, './/div/div/div/button/div[2]').text
        sub_menu_category_desc = sub_menu_category.find_element(By.XPATH, './/div/div/div/button/div[3]/div').text
        sub_menu_category_price = sub_menu_category.find_element(By.XPATH, './/div/div/div/button/div[4]/div/div/div').text
        itme_id = len(output_array)
        output_array.append([itme_id, 'Sweetgreen', menu_category_name, sub_menu_category_name, sub_menu_category_price, sub_menu_category_desc,  current_date, current_date, 'none']) 

with open('sweetgreen.csv', 'w', newline='', encoding='utf-8') as file:
    # Create a writing object
    writer = csv.writer(file)

    # Write output data to the CSV file
    writer.writerows(output_array)

exit()