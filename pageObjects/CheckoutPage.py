from selenium.webdriver.common.by import By

from pageObjects.ConfirmPage import ConfirmPage

class CheckOutPage:
    def __init__(self, driver):
        self.driver = driver

    productTitle = (By.XPATH, "//div[@class='card h-100']")
    productFooter = (By.XPATH, "div/button")
    checkOut = (By.CSS_SELECTOR, "a[class*='btn-primary']")

    def getProductTitles(self):
        return self.driver.find_elements(*CheckOutPage.productTitle)

    def getProductFooter(self, product):
        return product.find_element(*CheckOutPage.productFooter)

    def CheckOutItems(self):
        self.driver.find_element(*CheckOutPage.checkOut).click()
        confirmPage = ConfirmPage(self.driver)
        return confirmPage
