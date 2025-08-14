import pytest

from pageObjects.HomePage import HomePage
from testData.HomePageData import HomePageData
from utilities.BaseClass import BaseClass


class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):
        print(f"\n=== 폼 테스트 시작: {getData['username']} ===")
        log = self.getLogger()
        homepage = HomePage(self.driver)
        
        print("1. 사용자 정보 입력...")
        log.info("user name is " + getData["username"])
        homepage.getName().send_keys(getData["username"])
        print(f"   - 이름: {getData['username']}")
        
        homepage.getEmail().send_keys(getData["email"])
        print(f"   - 이메일: {getData['email']}")
        
        homepage.getPassword().send_keys("123456")
        print("   - 패스워드: ******")
        
        print("2. 옵션 선택...")
        homepage.selectCheckbox().click()
        print("   - 체크박스 선택")
        
        homepage.selectEmploymentStatus().click()
        print("   - 고용 상태 선택")

        print(f"3. 성별 선택: {getData['gender']}")
        if getData["gender"] == "InvalidGender":
            print("   ⚠ 의도적 실패 테스트 (스크린샷 캡처 확인용)")
        
        self.selectOptionByText(homepage.getGenderDropdown(), getData["gender"])
        self.selectOptionByIndex(homepage.getGenderDropdown(), 0)

        print("4. 폼 제출...")
        homepage.submitForm().click()
        
        message = homepage.getSuccessMessage()
        print(f"5. 결과: {message}")
        assert "Success" in message
        
        self.driver.refresh()
        print("=== 폼 테스트 완료 ===\n")

    @pytest.fixture(params=HomePageData.test_Homepage_data)
    def getData(self, request):
        return request.param
