# pageObjects/CheckoutPage.py
from selenium.webdriver.common.by import By
from .ConfirmPage import ConfirmPage

class CheckoutPage:
    # 카드 전체 블록
    product_cards = (By.XPATH, "//div[@class='card h-100']")
    add_button = (By.XPATH, "div/button")  # 각 카드 내부 버튼
    # 우상단 체크아웃(장바구니 보기)
    checkout_top = (By.CSS_SELECTOR, "a[class*='btn-primary']")
    # 장바구니 페이지에서 체크아웃 버튼
    checkout_bottom = (By.XPATH, "//button[contains(@class,'btn-success')]")

    def __init__(self, driver):
        self.driver = driver

    def getProductTitles(self):
        return self.driver.find_elements(*self.product_cards)

    def getProductFooter(self, card_element):
        return card_element.find_element(*self.add_button)

    def CheckOutItems(self):
        # 상단 장바구니 버튼 클릭 → 장바구니 화면에서 'Checkout' 클릭
        print("[CHECKOUT] 장바구니 페이지로 이동")
        self.driver.find_element(*self.checkout_top).click()
        print("[CHECKOUT] Checkout 진행")
        self.driver.find_element(*self.checkout_bottom).click()
        return ConfirmPage(self.driver)
