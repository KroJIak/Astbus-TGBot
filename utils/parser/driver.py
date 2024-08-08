
from selenium import webdriver
from fake_useragent import UserAgent

class SeleniumDriver(webdriver.Chrome):
    def __init__(self, addfakeUserAgent=True, showBrowser=True, windowSize=(1920, 1080), userDataDir: str = None):
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument('--disable-blink-features=AutomationControlled')
        chromeOptions.add_argument('disable-infobars')
        if addfakeUserAgent:
            chromeOptions.add_argument(f'user-agent={UserAgent().chrome}')
        if not showBrowser:
            chromeOptions.add_argument('--headless')
        if userDataDir:
            chromeOptions.add_argument(f'--user-data-dir={userDataDir}')
        super().__init__(options=chromeOptions)
        self.windowSize = windowSize
        self.setDefaultSettings()

    def setDefaultSettings(self):
        self.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                          const newProto = navigator.proto
                          delete newProto.parse
                          navigator.proto = newProto
                          """
        })
        self.set_window_size(*self.windowSize)

    def exit(self):
        self.close()