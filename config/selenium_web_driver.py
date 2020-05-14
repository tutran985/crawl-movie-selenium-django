import json
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options as OptionsFirefox
from selenium.webdriver.remote.webdriver import WebDriver
import config.config_system as config_system


class SeleniumDriver:
    def __init__(self):
        self.chrome_driver_path = "bin/chromedriver-2.42"
        self.use_remote_webdriver = True

    def get_chrome_option(self):
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--single-process')
        # chrome_options.add_argument('--disable-dev-shm-usage')
        # chrome_options.binary_location = "../python/bin/headless-chromium-v69"
        user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
        chrome_options.add_argument(f'user-agent={user_agent}')
        return chrome_options

    def get_chrome_driver(self):
        chrome_options = self.get_chrome_option()
        driver = webdriver.Chrome(
            executable_path=self.chrome_driver_path, chrome_options=chrome_options)
        SeleniumDriver.global_driver = driver
        if self.use_remote_webdriver:
            def send(driver, cmd, params={}):
                resource = "/session/%s/chromium/send_command_and_get_result" % driver.session_id
                url = driver.command_executor._url + resource
                body = json.dumps({'cmd': cmd, 'params': params})

                response = driver.command_executor._request('POST', url, body)
                response['status'] = 0
                response['session_id'] = driver.session_id

                # if response['status']:
                #     raise Exception(response.get('value'))

                return response.get('value')

            def add_script(driver, script):
                send(driver, "Page.addScriptToEvaluateOnNewDocument",
                     {"source": script})

            WebDriver.add_script = add_script

            driver.add_script(
                """
                Object.defineProperty(navigator, 'webdriver', { value: false, configurable: true});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                """
            )
        return driver

    def get_driver(self):
        # if config_system.is_used_chrome:
        return self.get_chrome_driver()
