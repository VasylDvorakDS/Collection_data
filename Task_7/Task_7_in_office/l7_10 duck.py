from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

driver = webdriver.Chrome()
driver.get("https://duckduckgo.com")

# Ввод текста
search_bar = driver.find_element(By.NAME, "q")
search_bar.send_keys("Selenium books")

# Кнопка поиск
search_button = driver.find_element(By.XPATH, "//input[@type='submit']")
search_button.click()

# Выпадающее меню время
time_dropdown = driver.find_element(By.XPATH, "//*[@id='link_wrapper']/div/div[3]/a")
time_dropdown.click()

# За последний месяц
time_last_month = driver.find_element(By.XPATH, "*//a[@data-value='m']")
time_last_month.click()

# Показать больше
more_btn = driver.find_element(By.XPATH, "//a[@class='result--more__btn btn btn--full']")
more_btn.click()

# Результаты
results = driver.find_elements(By.XPATH, "//div[@class='nrn-react-div']")
result_data = []

# Извлечение заголовка и URL каждого результата
for result in results:
    result_title = result.find_element(By.XPATH, ".//a[@class='eVNpHGjtxRBq_gLOfGDr LQNqh2UlkzYxREs65IJu']").text
    result_url = result.find_element(By.XPATH, ".//a[@class='eVNpHGjtxRBq_gLOfGDr LQNqh2UlkzYxREs65IJu']").get_attribute("href")
    result_data.append([result_title, result_url])

driver.quit()

# Запись данных в файл CSV
with open("duckduckgo_results.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Result Title", "URL"])
    writer.writerows(result_data)
