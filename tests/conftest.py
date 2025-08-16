import os, base64, pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

driver = None

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")

@pytest.fixture(scope="class")
def setup(request):
    global driver
    browser_name = request.config.getoption("browser_name")
    if browser_name == "chrome":
        service_obj = ChromeService(ChromeDriverManager().install())
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=service_obj, options=options)
    else:
        raise RuntimeError("Only chrome supported in Colab")

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.implicitly_wait(5)
    driver.maximize_window()

    request.cls.driver = driver
    yield
    driver.close()

# (기존 내용 유지) 상단 import / 전역 driver 그대로 사용

# ... 중략 ...

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when in ('call','setup'):
        xfail = hasattr(report, 'wasxfail')
        # ↓ driver가 없으면 스크린샷 로직 건너뜀
        if ((report.skipped and xfail) or (report.failed and not xfail)) and (driver is not None):
            file_name = report.nodeid.replace("::", "_") + ".png"
            file_path = os.path.join("reports", file_name)
            _capture_screenshot(file_path)
            with open(file_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            html = (
                f'<div><img src="data:image/png;base64,{b64}" alt="screenshot" '
                f'style="width:304px;height:228px;" '
                f'onclick="window.open(this.src)" align="right"/></div>'
            )
            extra.append(pytest_html.extras.html(html))
    report.extra = extra

def _capture_screenshot(path):
    # ↓ driver가 없으면 바로 리턴
    if driver is None:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.get_screenshot_as_file(path)


