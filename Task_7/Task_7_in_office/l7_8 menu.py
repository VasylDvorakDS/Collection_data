from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://www.example.com/dropdown-menu")

dropdown = driver.find_element(By.ID, "dropdown-menu")
select = Select(dropdown)
select.select_by_visible_text("Option 2")

driver.quit()