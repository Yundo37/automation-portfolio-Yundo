# conftest.py
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

driver = None  # 실패 시 스크린샷용

def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")

@pytest.fixture(scope="class")
def setup(request):
    """
    원본 흐름 유지: request.cls.driver 주입.
    Colab/헤드리스에서 안정 동작하도록 옵션만 반영.
    """
    global driver
    browser_name = request.config.getoption("browser_name")

    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    # 브라우저 콘솔 로그도 캡처 원하면 주석 해제
    # opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    opts.binary_location = os.environ.get("CHROME_BIN", "/usr/bin/chromium-browser")

    if browser_name.lower() != "chrome":
        print("[WARN] Colab에서는 chrome만 지원합니다. chrome으로 실행합니다.")

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(30)
    driver.implicitly_wait(5)
    try:
        driver.set_window_size(1920, 1080)
    except Exception:
        pass

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    print(f"[SETUP] Started at: {driver.current_url}")

    request.cls.driver = driver
    yield
    driver.close()

# ----------------------------
# pytest-html 스크린샷 첨부
# ----------------------------
@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    실패/xfail 시 스크린샷을 HTML 보고서에 포함.
    --self-contained-html 과 함께 쓰면 Base64로 임베드되어 휴대성이 좋음.
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when in ("setup", "call"):
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            _capture_screenshot(file_name)
            if pytest_html:
                try:
                    with open(file_name, "rb") as f:
                        image_data = f.read()
                    extra.append(pytest_html.extras.image(image_data, mime_type='image/png'))
                except Exception:
                    extra.append(pytest_html.extras.html(
                        f'<div><img src="{file_name}" style="width:304px;height:228px;" '
                        'onclick="window.open(this.src)" align="right"/></div>'
                    ))
        report.extra = extra

def _capture_screenshot(name: str):
    if driver:
        driver.get_screenshot_as_file(name)
