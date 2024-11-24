from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://www.example.com/modal-window")

# Нахождение триггера модального окна и клик на нем, чтобы открыть модальное окно
modal_trigger = driver.find_element(By.ID, "modal-trigger")
modal_trigger.click()

# Ожидание отображения модального окна
modal = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modal")))

# Взаимодействовать с модальным окном (например, заполнение формы)
modal_input = modal.find_element(By.ID, "modal-input")
modal_input.send_keys("Hello, World!")

# Закрытие модального окна
modal_close = modal.find_element(By.ID, "modal-close")
modal_close.click()

# Закрытие браузера
driver.quit()
