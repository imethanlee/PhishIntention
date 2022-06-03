import os
from urllib import parse

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager


class Crawler:
    def __init__(self, demo_folder_path = "./demo/demo_cache"):
        self.demo_folder_path = demo_folder_path
        if not os.path.exists(self.demo_folder_path):
            os.makedirs(self.demo_folder_path)

        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(),
            desired_capabilities=self._get_chrome_capabilities(),
            options=self._get_chrome_options(lang_txt=os.path.join(os.getcwd(), 'phishintention/src/util/lang.txt'))
            )
        self.driver.set_page_load_timeout(10)  # set timeout to avoid wasting time
        self.driver.set_script_timeout(10)  # set timeout to avoid wasting time
        print("\n")

    def _get_chrome_options(self, lang_txt):
        # enable translation
        white_lists = {}

        with open(lang_txt) as langf:
            for i in langf.readlines():
                i = i.strip()
                text = i.split(' ')
                white_lists[text[1]] = 'en'
        prefs = {
            "translate": {"enabled": "true"},
            "translate_whitelists": white_lists
        }

        options = webdriver.ChromeOptions()
        
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--ignore-certificate-errors') # ignore errors
        options.add_argument('--ignore-ssl-errors')
        # options.add_argument("--headless") # FIXME: do not disable browser (have some issues: https://github.com/mherrmann/selenium-python-helium/issues/47)
        options.add_argument('--no-proxy-server')
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")

        options.add_argument("--start-maximized")
        options.add_argument('--window-size=1920,1080') # fix screenshot size
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        options.set_capability('unhandledPromptBehavior', 'dismiss') # dismiss

        # Add those options for Linux users
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')

        options.add_argument('--hide-scrollbars')

        return options

    def _get_chrome_capabilities(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # chromedriver 75+
        capabilities["unexpectedAlertBehaviour"] = "dismiss"  # handle alert
        capabilities["pageLoadStrategy"] = "eager"  # eager mode #FIXME: set eager mode, may load partial webpage

    def crawl(self, url):
        # Step 0: Check accessibility of the url
        try:
            self.driver.get(url)
        except Exception as e:
            print("Open webpage failed ({})".format(url))
            print("ERROR: {}".format(e))
            return

        # Step 1: New folder
        parse_url = parse.urlparse(url)
        netloc = parse_url.netloc
        url_folder_path = os.path.join(self.demo_folder_path, netloc)
        if not os.path.exists(url_folder_path):
            os.mkdir(url_folder_path)
        url_path = os.path.join(url_folder_path, "info.txt")
        screenshot_path =  os.path.join(url_folder_path, "shot.png")
        html_code_path = os.path.join(url_folder_path, "html.txt")

        # Step 2: Save URL to .txt
        self._get_url_txt(url_path)

        # Step 3: Screenshot
        self._get_screenshot(screenshot_path)

        # Step 4: HTML code
        self._get_html_code(html_code_path)

        # Step 5: Return paths
        return {
            "url_folder_path": url_folder_path, 
            "url_path": url_path,
            "screenshot_path":screenshot_path, 
            "html_code_path": html_code_path
            }

    def _get_url_txt(self, path):
        file = open(path, 'w')
        file.write(self.driver.current_url)
        file.close()

    def _get_screenshot(self, path):
        self.driver.get_screenshot_as_file(path)

    def _get_html_code(self, path):        
        file = open(path, 'w')
        file.write(self.driver.page_source)
        file.close()


if __name__ == "__main__":
    crawler = Crawler()
    url = "https://bhooi.github.io/"
    # url = "https://www.google.com/"
    # url = "https://www.baidu.com/"
    url = "https://claimskintransformers.gamename.net/"
    # url = "http://casaelizabeth.com/neon/Webmail/index.html"
    crawler.crawl(url)
    # url = "https://www.google.com/"
    # crawler.crawl(url)
