from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://example.com")

result = driver.execute_script("return document.title")

print(result)
driver.quit()