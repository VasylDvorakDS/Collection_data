import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://quotes.toscrape.com/page/1")

quotes = []

while True:
    quote_elements = driver.find_elements(By.XPATH, "//div[@class='quote']")

    for quote_element in quote_elements:
        quote = quote_element.find_element(By.XPATH, "//span[@class = 'text']").text
        author = quote_element.find_element(By.XPATH, "//span/small[@class = 'author']").text
        quotes.append({"quote":quote, "author": author})

    next_button = driver.find_elements(By.XPATH, "//li[@class='next']/a")
    if not next_button:
        break

    next_button[0].click()
    time.sleep(1)

for quote in quotes:
    print(quote["quote"], 'by' , quote["author"])

with open("quotes.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["quote", "author"])
    writer.writeheader()
    writer.writerows(quotes)

driver.close()