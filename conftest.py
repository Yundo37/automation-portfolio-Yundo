import pytest

from selenium import webdriver
driver = None
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.webdriver import WebDriver as EdgeDriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome"
    )


@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    
    print(f"\n브라우저 설정: {browser_name}")
    
    if browser_name == "chrome":
        chrome_options = Options()
        
        # Colab 환경 감지
        try:
            import google.colab
            print("Google Colab 환경 감지 - 헤드리스 모드로 실행")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        except ImportError:
            print("로컬 환경에서 실행")
        
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        try:
            from webdriver_manager.chrome import ChromeDriverManager
            service_obj = ChromeService(ChromeDriverManager().install())
            print("ChromeDriver 자동 다운로드 완료")
        except:
            service_obj = ChromeService("C:/Users/YB/Documents/chromedriver/chromedriver.exe")
            print("로컬 ChromeDriver 사용")
        
        driver = webdriver.Chrome(service=service_obj, options=chrome_options)
    elif browser_name == "edge":
        service_obj = EdgeService("C:/Users/YB/Documents/edgedriver/msedgedriver.exe")
        driver = EdgeDriver(service=service_obj)

    print("테스트 사이트 접속: https://rahulshettyacademy.com/angularpractice/")
    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.implicitly_wait(5)
    driver.maximize_window()

    request.cls.driver = driver
    yield
    print("브라우저 종료")
    driver.close()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            print(f"테스트 실패 - 스크린샷 캡처: {file_name}")
            _capture_screenshot(file_name)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


def _capture_screenshot(name):
    driver.get_screenshot_as_file(name)
