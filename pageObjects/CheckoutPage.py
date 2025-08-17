from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pageObjects.ConfirmPage import ConfirmPage

class CheckOutPage:
    def __init__(self, driver):
        self.driver = driver

    productTitle = (By.XPATH, "//div[@class='card h-100']")
    productFooter = (By.XPATH, "div/button")
    checkOut = (By.XPATH, "//a[contains(@class, 'btn-primary')]")

    def getProductTitles(self):
        return self.driver.find_elements(*CheckOutPage.productTitle)

    def getProductFooter(self, product):
        return product.find_element(*CheckOutPage.productFooter)

    def CheckOutItems(self):
        wait = WebDriverWait(self.driver, 10)
        checkout_btn = wait.until(EC.element_to_be_clickable(CheckOutPage.checkOut))
        self.driver.execute_script("arguments[0].scrollIntoView();", checkout_btn)
        checkout_btn.click()
        return ConfirmPage(self.driver)
