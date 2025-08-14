from selenium.webdriver.common.by import By


class ConfirmPage:

    def __init__(self, driver):
        self.driver = driver

    countryInput = (By.ID, "country")
    countrySelect = (By.LINK_TEXT, "India")
    checkbox = (By.XPATH, "//div[@class='checkbox checkbox-primary']")
    submitButton = (By.CSS_SELECTOR, "[type='submit']")
    successMsg = (By.CLASS_NAME, "alert-success")

    def enterCountry(self, name):
        return self.driver.find_element(*ConfirmPage.countryInput).send_keys(name)

    def selectCountry(self):
        return self.driver.find_element(*ConfirmPage.countrySelect)

    def checkTerms(self):
        return self.driver.find_element(*ConfirmPage.checkbox)

    def submitOrder(self):
        return self.driver.find_element(*ConfirmPage.submitButton)

    def getSuccessMessage(self):
        return self.driver.find_element(*ConfirmPage.successMsg).text
