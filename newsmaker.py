from selenium import webdriver
from selenium.webdriver.common.by import By
import pause


def top_news():
    driver = webdriver.Chrome()
    driver.get("https://www.cnbctv18.com/tags/forex.htm")
    return (driver.find_element(By.XPATH, '//*[@id="all_Section"]/div/ul/li[1]/div/div[2]/a').text,
            driver.find_element(By.XPATH, '//*[@id="all_Section"]/div/ul/li[2]/div/div[2]/a/h2').text)

