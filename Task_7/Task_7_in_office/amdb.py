from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get("https://www.imdb.com/chart/top")

movie_title_elements = driver.find_elements(By.CSS_SELECTOR, "td.titleColumn a")
rating_elements = driver.find_elements(By.CSS_SELECTOR, "td.ratingColumn strong")

titles = [element.text for element in movie_title_elements]
ratings = [element.text for element in rating_elements]

for i in range(10):
    print("Рейтинг {}: {} ({})".format(i + 1, titles[i], ratings[i]))

driver.quit()
