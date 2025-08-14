import time
from selenium.webdriver.common.by import By
from pageObjects.HomePage import HomePage
from utilities.BaseClass import BaseClass


class TestOne(BaseClass):

    def test_e2e(self):
        print("\n=== E2E 테스트 시작: 전체 주문 프로세스 ===")
        log = self.getLogger()
        
        print("1. 홈페이지에서 Shop 메뉴로 이동...")
        homePage = HomePage(self.driver)
        checkoutpage = homePage.shopItems()
        
        print("2. 상품 목록 조회 중...")
        log.info("getting all the product title")
        products = checkoutpage.getProductTitles()
        print(f"   총 {len(products)}개 상품 발견")

        print("3. Blackberry 상품 검색 및 장바구니 추가...")
        for product in products:
            productName = product.find_element(By.XPATH, "div/h4/a").text
            print(f"   - 상품: {productName}")
            log.info(productName)
            if productName == "Blackberry":
                print("   ✓ Blackberry 발견! 장바구니에 추가")
                checkoutpage.getProductFooter(product).click()
                break

        print("4. 장바구니로 이동...")
        self.driver.find_element(By.CSS_SELECTOR, "a[class*=btn-primary]").click()

        print("5. 체크아웃 진행...")
        confirmPage = checkoutpage.CheckOutItems()
        
        print("6. 배송 정보 입력...")
        log.info("Entering country name is ind")
        confirmPage.enterCountry("ind")
        print("   - 국가 코드 'ind' 입력")
        
        self.verifyLinkPresence("India")
        print("   - India 옵션 선택")
        confirmPage.selectCountry().click()
        
        print("   - 약관 동의")
        confirmPage.checkTerms().click()
        
        print("7. 주문 제출...")
        confirmPage.submitOrder().click()

        successText = confirmPage.getSuccessMessage()
        print(f"8. 주문 완료: {successText}")
        log.info("Text received from application is" + successText)
        assert "Success! Thank you!" in successText
        print("=== E2E 테스트 성공 완료 ===\n")
        time.sleep(3)
