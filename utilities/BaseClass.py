# utilities/BaseClass.py
import logging
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class BaseClass:
    def __init__(self, driver):
        # pytest에서는 request.cls.driver로 주입되므로 빈 생성자를 허용
        pass

    def getLogger(self):
        logger = logging.getLogger("portfolio")
        if not logger.handlers:
            handler = logging.StreamHandler()
            fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            handler.setFormatter(fmt)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def verifyLinkPresence(self, text, timeout=10):
        print(f"[WAIT] 링크 노출 대기: {text!r}")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(("link text", text))
        )

    def selectOptionByText(self, element, text):
        print(f"[SELECT] by text: {text!r}")
        Select(element).select_by_visible_text(text)

    def selectOptionByIndex(self, element, index):
        print(f"[SELECT] by index: {index}")
        Select(element).select_by_index(index)
