# tests/test_HomePage.py  (드롭인 교체본: 의도적 실패 1건 포함)
import pytest
from pageObjects.HomePage import HomePage
from testData.HomePageData import HomePageData
from utilities.BaseClass import BaseClass


class TestHomePage(BaseClass):

    def test_formSubmission(self, getData):
        log = self.getLogger()
        homepage = HomePage(self.driver)

        print(f"[STEP] 폼 입력 시작: username={getData['username']!r}, email={getData['email']!r}, gender={getData['gender']!r}")
        log.info("user name is" + getData["username"])

        homepage.getName().send_keys(getData["username"])
        homepage.getEmail().send_keys(getData["email"])
        homepage.getPassword().send_keys("123456")
        homepage.selectCheckbox().click()
        homepage.selectEmploymentStatus().click()

        # 드롭다운 선택(텍스트/인덱스 둘 다 호출하여 동작 로그 확인)
        self.selectOptionByText(homepage.getGenderDropdown(), getData["gender"])
        self.selectOptionByIndex(homepage.getGenderDropdown(), 0)

        homepage.submitForm().click()
        message = homepage.getSuccessMessage()
        print(f"[STEP] 성공 메시지 원문: {message!r}")

        # --- 여기서 '일부러' 실패 유도 ---
        # 정상이라면 "Success" 가 들어있지만,
        # 데모를 위해 틀린 기대값으로 검증해 실패를 발생시킴.
        expected = "Success (DEMO FAIL)"   # <= 의도적 실패 포인트
        print(f"[CHECK] 기대값(실패 유도): {expected!r}")
        assert expected in message

        # 아래 줄은 실패 후 실행되지 않지만, 혹시 PASS 시 로그를 남김
        print("[STEP] 폼 제출 시나리오 PASS")

    @pytest.fixture(params=HomePageData.test_Homepage_data)
    def getData(self, request):
        return request.param
