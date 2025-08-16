import time
from selenium.webdriver.common.by import By
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass

class TestOne(BaseClass):
    def test_e2e(self):
        log = self.getLogger()
        print("[E2E] 홈 진입 및 상점 이동")
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()

        log.info("getting all the product title")
        print("[E2E] 상품 목록 수집")
        products = checkoutpage.getProductTitles()

        for product in products:
            productName = product.find_element(By.XPATH, "div/h4/a").text
            log.info(productName)
            print(f"[E2E] 발견한 상품: {productName}")
            if productName == "Blackberry":
                checkoutpage.getProductFooter(product).click()
                print("[E2E] Blackberry 담기 완료")
                break

        print("[E2E] 카트 페이지로 이동")
        self.driver.find_element(By.CSS_SELECTOR, "a[class*=btn-primary]").click()

        print("[E2E] 체크아웃 페이지 진입")
        confirmPage = checkoutpage.CheckOutItems()

        log.info("Entering country name is ind")
        print("[E2E] 국가 입력: ind")
        confirmPage.enterCountry("ind")
        self.verifyLinkPresence("India")

        print("[E2E] 국가 'India' 선택 및 약관 동의")
        confirmPage.selectCountry().click()
        confirmPage.checkTerms().click()
        confirmPage.submitOrder().click()

        successText = confirmPage.getSuccessMessage()
        log.info("Text received from application is" + successText)
        print(f"[E2E] 완료 메시지: {successText}")
        assert "Success! Thank you!" in successText
        time.sleep(1)
