# pageObjects/ConfirmPage.py
from selenium.webdriver.common.by import By

class ConfirmPage:
    country_input = (By.ID, "country")
    suggestion = (By.LINK_TEXT, "India")
    checkbox = (By.CSS_SELECTOR, "div.checkbox input[type='checkbox']")
    submit = (By.CSS_SELECTOR, "input[type='submit']")
    alert = (By.CSS_SELECTOR, "div.alert-success")

    def __init__(self, driver):
        self.driver = driver

    def enterCountry(self, key):
        self.driver.find_element(*self.country_input).send_keys(key)

    def selectCountry(self):
        return self.driver.find_element(*self.suggestion)

    def checkTerms(self):
        return self.driver.find_element(*self.checkbox)

    def submitOrder(self):
        return self.driver.find_element(*self.submit)

    def getSuccessMessage(self):
        return self.driver.find_element(*self.alert).text
