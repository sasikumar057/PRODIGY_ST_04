from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

LAMBDA_USERNAME = "xyz@gmail"
LAMBDA_ACCESS_KEY = "ljoiclkjlweroijlckjalkmdflksdfjosidjlckj"

LAMBDA_GRID_URL = f"https://{LAMBDA_USERNAME}:{LAMBDA_ACCESS_KEY}@hub.lambdatest.com/wd/hub"

browsers = [
    {"browserName": "Chrome", "platform": "Windows 10", "version": "latest"},
    {"browserName": "Firefox", "platform": "Windows 10", "version": "latest"},
    {"browserName": "Edge", "platform": "Windows 10", "version": "latest"},
    {"browserName": "Safari", "platform": "macOS Ventura", "version": "latest"},
]

def test_login(browser_config):
    if browser_config["browserName"].lower() == "chrome":
        options = Options()
    elif browser_config["browserName"].lower() == "firefox":
        options = FirefoxOptions()
    elif browser_config["browserName"].lower() == "edge":
        options = EdgeOptions()
    elif browser_config["browserName"].lower() == "safari":
        options = SafariOptions()
    else:
        options = None  

    options.set_capability("platform", browser_config["platform"])
    options.set_capability("browserName", browser_config["browserName"])
    options.set_capability("browserVersion", browser_config["version"])
    options.set_capability("resolution", "1920x1080")
    options.set_capability("name", f"Test on {browser_config['browserName']} {browser_config['version']}")
    options.set_capability("build", "Cross-Browser Testing")
    options.set_capability("project", "My Project")
    options.set_capability("network", True)
    options.set_capability("visual", True)
    options.set_capability("video", True)

    driver = None 
    try:
        driver = webdriver.Remote(
            command_executor=LAMBDA_GRID_URL,
            options=options, 
        )

        driver.get("https://www.saucedemo.com/") 

        username = driver.find_element(By.ID, "user-name") 
        password = driver.find_element(By.ID, "password") 
        login_button = driver.find_element(By.ID, "login-button")  

        username.send_keys("standard_user")
        password.send_keys("secret_sauce")
        login_button.click()
        
        driver.get_screenshot_as_file("screenshot_after_login.png")

        assert "Swag Labs" in driver.title, "Login test failed!" 
        print(f"Test Passed on {browser_config['browserName']} {browser_config['version']}")

    except Exception as e:
        print(f"Test Failed on {browser_config['browserName']} {browser_config['version']} - {e}")

    finally:
        if driver:
            driver.quit()

for browser in browsers:
    test_login(browser)
