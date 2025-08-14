# pageObjects/HomePage.py
from selenium.webdriver.common.by import By
from .CheckoutPage import CheckoutPage

class HomePage:
    shop_link = (By.LINK_TEXT, "Shop")
    name = (By.CSS_SELECTOR, "input[name='name']")
    email = (By.NAME, "email")
    password = (By.ID, "exampleInputPassword1")
    checkbox = (By.ID, "exampleCheck1")
    # Employment Status -> Student 라디오버튼 (튜토리얼 기준)
    employment = (By.CSS_SELECTOR, "#inlineRadio1")
    gender_dropdown = (By.ID, "exampleFormControlSelect1")
    submit_btn = (By.CSS_SELECTOR, "input[value='Submit']")
    success = (By.CLASS_NAME, "alert-success")

    def __init__(self, driver):
        self.driver = driver

    def shopItems(self):
        print("[PAGE] Home → Shop 클릭")
        self.driver.find_element(*self.shop_link).click()
        return CheckoutPage(self.driver)

    # 폼요소 getters
    def getName(self): return self.driver.find_element(*self.name)
    def getEmail(self): return self.driver.find_element(*self.email)
    def getPassword(self): return self.driver.find_element(*self.password)
    def selectCheckbox(self): return self.driver.find_element(*self.checkbox)
    def selectEmploymentStatus(self): return self.driver.find_element(*self.employment)
    def getGenderDropdown(self): return self.driver.find_element(*self.gender_dropdown)
    def submitForm(self): return self.driver.find_element(*self.submit_btn)
    def getSuccessMessage(self): return self.driver.find_element(*self.success).text
