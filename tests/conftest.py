import os
import base64
import shutil
import tempfile
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


driver = None


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome")


@pytest.fixture(scope="class")
def setup(request):
    global driver

    browser_name = request.config.getoption("browser_name")

    if browser_name != "chrome":
        raise RuntimeError("Only chrome supported in Colab")

    cft_chrome = "/content/chrome-for-testing/chrome-linux64/chrome"
    cft_driver = "/content/chromedriver-for-testing/chromedriver-linux64/chromedriver"

    if os.path.exists(cft_chrome) and os.path.exists(cft_driver):
        chrome_binary = cft_chrome
        service_obj = ChromeService(cft_driver)
    else:
        chrome_binary = (
            shutil.which("google-chrome")
            or shutil.which("google-chrome-stable")
            or shutil.which("chromium")
            or shutil.which("chromium-browser")
        )

        if chrome_binary is None:
            raise RuntimeError("Chrome binary not found in Colab environment")

        service_obj = None

    options = ChromeOptions()
    options.binary_location = chrome_binary

    user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-background-networking")
    options.add_argument("--disable-sync")
    options.add_argument("--disable-default-apps")
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-pipe")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    if service_obj is not None:
        driver = webdriver.Chrome(service=service_obj, options=options)
    else:
        driver = webdriver.Chrome(options=options)

    driver.get("https://rahulshettyacademy.com/angularpractice/")
    driver.implicitly_wait(5)
    driver.maximize_window()

    request.cls.driver = driver

    yield

    driver.quit()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when in ("call", "setup"):
        xfail = hasattr(report, "wasxfail")
        if ((report.skipped and xfail) or (report.failed and not xfail)) and driver is not None:
            file_name = report.nodeid.replace("::", "_").replace("/", "_") + ".png"
            file_path = os.path.join("reports", file_name)

            _capture_screenshot(file_path)

            if os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    b64 = base64.b64encode(f.read()).decode()

                html = (
                    f'<div><img src="data:image/png;base64,{b64}" '
                    f'alt="screenshot" style="width:304px;height:228px;" '
                    f'onclick="window.open(this.src)" align="right"/></div>'
                )
                extra.append(pytest_html.extras.html(html))

    report.extra = extra


def _capture_screenshot(path):
    if driver is None:
        return

    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.get_screenshot_as_file(path)
