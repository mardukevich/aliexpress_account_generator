from time import sleep
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from tools.utils import get_logger, get_proxy, generate_email, generate_password


class Autoreger:

    def __init__(self, account_file, logger, proxy=None):
        self.__logger = logger
        self.__proxy = proxy
        self.__accounts_file_path = account_file
        self.__browser = None

    def __run_browser(self, proxy):
        if proxy:
            webdriver.DesiredCapabilities.CHROME['proxy']={
                    "httpProxy": proxy,
                    'ftpProxy': proxy,
                    "sslProxy": proxy,
                    "proxyType":"MANUAL",
                }
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.__browser = webdriver.Chrome(options=chrome_options)
        self.__logger.info('Login page is loaded')

    def __load_page(self, url):
        self.__browser.get(url)

    def register_account(self, proxy=None):
        try:
            self.__run_browser(proxy)
            self.__load_page("https://login.aliexpress.com/")
            self.__click_on_register_tab()

            email = generate_email('gmail.com')
            self.__enter_email(email)

            password = generate_password()
            self.__enter_password(password)

            self.__move_scrollbar()
            self.__click_on_register_button()
            if self.__is_register():
                self.__save_account(email, password)
        except (NoSuchElementException, RuntimeError) as err:
            self.__logger.exception(err)
        finally:
            self.__close_browser()

    def __save_account(self, email, password):
        with open(self.__accounts_file_path, 'a') as file:
            file.write(f'{email} {password} \n')
            self.__logger.info(f'Account saved: {email}, {password}')

    def __click_on_register_tab(self):
        register_tab = self.__browser.\
            find_element_by_css_selector('#root > div > ul > li:nth-child(1)')
        register_tab.click()
        sleep(3)
        self.__logger.info('Register tab clicked')

    def __enter_email(self, email):
        try:
            email_field = self.__browser.\
                find_element_by_xpath("//input[@placeholder='Email address']")
        except NoSuchElementException:
            self.__logger.info("Email widget doesn't appear!")
        else:
            email = generate_email(domain='gmail.com')
            email_field.send_keys(email)
            sleep(3)
            self.__logger.info('Mail entered')

    def __enter_password(self, password):
        password_field = self.__browser.find_element_by_xpath("//input[@type='password']")
        password_field.send_keys(password)
        sleep(3)
        self.__logger.info('Password entered')

    def __move_scrollbar(self):
        try:
            scrollbar = self.__browser.find_element_by_id("nc_1__scale_text")
        except NoSuchElementException:
            self.__logger.info('Scrollbar did not appear')
        else:
            x_offset = scrollbar.location.get("x")
            y_offset = scrollbar.location.get("y")
            webdriver.ActionChains(self.__browser).click_and_hold(scrollbar).\
                move_by_offset(x_offset, y_offset).release().perform()
            self.__logger.info('Scrollbar moved')

    def __click_on_register_button(self):
        register_button = self.__browser.find_element_by_tag_name("body").\
                                 find_element_by_class_name('fm-button')
        register_button.click()
        self.__logger.info('Register button clicked')

    def __is_register(self):
        old_title = self.__browser.title
        register_tab = self.__browser.find_element_by_class_name("login-container") \
                                     .find_element_by_tag_name("ul") \
                                     .find_element_by_class_name("fm-tabs-tab")
        register_tab.click()
        return old_title != self.__browser.title

    def __close_browser(self):
        self.__browser.close()

def generate_accounts(number, logger):
    autoreger = Autoreger('files/accounts.txt', logger)
    for _ in range(number):
        autoreger.register_account(proxy=get_proxy())

if __name__ == "__main__":
    logger = get_logger('file.log', name='ali')
    try:
        generate_accounts(500, logger)
    except Exception as err:
        logger.exception(err)
