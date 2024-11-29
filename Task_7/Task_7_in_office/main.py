from aiohttp.web_routedef import options
from holoviews.examples.gallery.apps.bokeh.gapminder import button
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time

options=Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get("https://wildberries.ru")
# input=driver.find_element(By.XPATH,"//input[@id='searchInput']")
time.sleep(2)
input=driver.find_element(By.ID,'searchInput')
input.send_keys("телевизор DEXP")
input.send_keys(Keys.ENTER)

time.sleep(2)

while True:
    # wait = WebDriverWait(driver, 30)
    # cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//article[@id]")))
    while True:
        wait = WebDriverWait(driver, 30)
        cards = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//article[@id]")))


    # cards=driver.find_elements(By.XPATH, "//article[@id]") #105
        count=len(cards)
        print(count)
        driver.execute_script("windows.scrollBy(0,2000)")
        time.sleep(2)
        cards=driver.find_elements(By.XPATH, "//article[@id]")
        if len(cards)==count:
            break

    for card in cards:
        price=card.find_element(By.CLASS_NAME, "price__lower-price").text
        name=card.find_element(By.CLASS_NAME, "./div/a").get_attribute("aria-label")
        url=card.find_element(By.XPATH, "./div/a").get_attribute("href")
        #goods.add({'price':price,'name':name,'url':url})
        print(price,name,url)
        # TODO-SAVE IN DB

    try:
        button=driver.find_element(By.CLASS_NAME, "pagination-next")
        actions=ActionChains(driver)
        actions.scroll_to_element(button).click()   #.key_down(Keys.CONTROL).key_down(Keys.C)
        actions.perform()
    except:
        break

# print(len(cards))


