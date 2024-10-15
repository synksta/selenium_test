from selenium import webdriver
import time

url = "https://аквасуши.рф/"
driver = webdriver.Firefox()

try:
    for i in range(50):
        driver.get(url=url)
        time.sleep(0.1 * i)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()
