from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://example.com/movies")

next_button_locator = (By.XPATH, "//a[@class='next']")

current_page = 1

while True:
    print(f"Page {current_page}")

    try:
        next_button = driver.find_element(*next_button_locator)
        next_button.click()
        current_page += 1
    except NoSuchElementException:
        break

driver.quit()
