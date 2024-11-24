from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://quotes.toscapr.com/page/1")

wait = WebDriverWait(driver,10)
element = wait.until(EC.presence_of_element_located(By.CSS_SELECTION,".quote"))

quote = element.text

driver.quit()