# tests/test_e2e.py  (드롭인 교체본: 성공 유지)
import time
from selenium.webdriver.common.by import By
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestOne(BaseClass):

    def test_e2e(self):
        log = self.getLogger()
        homePage = HomePage(self.driver)
        print("[STEP] 홈 페이지 로드 완료")
        checkoutpage = homePage.shopItems()
        print("[STEP] Shop 화면으로 이동")

        log.info("getting all the product title")
        products = checkoutpage.getProductTitles()
        print(f"[STEP] 상품 개수: {len(products)}")

        target = "Blackberry"
        for product in products:
            productName = product.find_element(By.XPATH, "div/h4/a").text
            print(f"[STEP] 상품명: {productName}")
            log.info(productName)
            if productName == target:
                checkoutpage.getProductFooter(product).click()
                print(f"[STEP] '{target}' 장바구니 담기 클릭")
                break

        self.driver.find_element(By.CSS_SELECTOR, "a[class*=btn-primary]").click()
        print("[STEP] 장바구니 페이지로 이동 버튼 클릭")

        confirmPage = checkoutpage.CheckOutItems()
        log.info("Entering country name is ind")
        print("[STEP] 국가 'ind' 입력")
        confirmPage.enterCountry("ind")
        self.verifyLinkPresence("India")
        print("[STEP] 자동완성에서 'India' 링크 노출 확인")

        confirmPage.selectCountry().click()
        confirmPage.checkTerms().click()
        print("[STEP] 국가 선택 및 약관 체크")

        confirmPage.submitOrder().click()
        print("[STEP] 주문 제출")

        successText = confirmPage.getSuccessMessage()
        print(f"[STEP] 성공 메시지: {successText!r}")
        log.info("Text received from application is" + successText)
        assert "Success! Thank you!" in successText

        time.sleep(1)
        print("[STEP] e2e 시나리오 PASS")
