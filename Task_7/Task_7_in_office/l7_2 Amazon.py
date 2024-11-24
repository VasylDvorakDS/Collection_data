from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://amazon.com")

search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
search_box.send_keys["laptops"]
search_box.submit()

assert "laptops" in driver.title

div_element = driver.find_element(By.ID, 'my-div')
print(div_element.text)
print(div_element.get_attribute("class"))