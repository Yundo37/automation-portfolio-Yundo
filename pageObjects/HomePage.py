from selenium.webdriver.common.by import By
from pageObjects.CheckoutPage import CheckOutPage


class HomePage:
    def __init__(self, driver):
        self.driver = driver

    shop = (By.CSS_SELECTOR, "a[href*='shop']")
    name = (By.CSS_SELECTOR, "input[name='name']")
    email = (By.NAME, "email")
    password = (By.ID, "exampleInputPassword1")
    checkbox = (By.ID, "exampleCheck1")
    genderDropdown = (By.ID, "exampleFormControlSelect1")
    employmentStatus = (By.CSS_SELECTOR, "#inlineRadio1")
    submitButton = (By.XPATH, "//input[@type='submit']")
    successText = (By.CLASS_NAME, "alert-success")
    twoWayBindingField = (By.XPATH, "(//input[@type='text'])[3]")

    def shopItems(self):
        self.driver.find_element(*HomePage.shop).click()
        checkoutpage = CheckOutPage(self.driver)
        return checkoutpage

    def getName(self):
        return self.driver.find_element(*HomePage.name)

    def getEmail(self):
        return self.driver.find_element(*HomePage.email)

    def getPassword(self):
        return self.driver.find_element(*HomePage.password)

    def selectCheckbox(self):
        return self.driver.find_element(*HomePage.checkbox)

    def getGenderDropdown(self):
        return self.driver.find_element(*HomePage.genderDropdown)

    def selectEmploymentStatus(self):
        return self.driver.find_element(*HomePage.employmentStatus)

    def submitForm(self):
        return self.driver.find_element(*HomePage.submitButton)

    def getSuccessMessage(self):
        return self.driver.find_element(*HomePage.successText).text

    def getTwoWayBindingField(self):
        return self.driver.find_element(*HomePage.twoWayBindingField)
