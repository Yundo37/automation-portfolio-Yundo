import pytest
from pageObjects.HomePage import HomePage
from testData.HomePageData import HomePageData
from utilities.BaseClass import BaseClass

class TestHomePage(BaseClass):
    def test_formSubmission(self, getData):
        log = self.getLogger()
        homepage = HomePage(self.driver)

        print(f"[FORM] 입력 시작: {getData}")
        log.info("user name is" + getData["username"])

        homepage.getName().send_keys(getData["username"])
        homepage.getEmail().send_keys(getData["email"])
        homepage.getPassword().send_keys("123456")
        homepage.selectCheckbox().click()
        homepage.selectEmploymentStatus().click()
        self.selectOptionByText(homepage.getGenderDropdown(), getData["gender"])
        self.selectOptionByIndex(homepage.getGenderDropdown(), 0)

        homepage.submitForm().click()
        message = homepage.getSuccessMessage()
        print(f"[FORM] 성공 메시지: {message}")

        if getData["username"] == "OB":           # 데모용 실패
            print("[FORM] 데모용 실패 트리거")
            assert "ThisShouldFail" in message
        else:
            assert "Success" in message

        self.driver.refresh()

    @pytest.fixture(params=HomePageData.test_Homepage_data)
    def getData(self, request):
        return request.param
