import os
import sys
import time
import allure
from selenium import webdriver
from robotlibcore import PY2
from robot.libraries.BuiltIn import RobotNotRunningError
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      FrameKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords,
                                      WindowKeywords)
from airtest import aircv
from airtest_selenium.proxy import Element, WebChrome, WebFirefox, WebRemote
from airtest.core.helper import logwrap
from airtest.core.settings import Settings as ST

class AirSelenium(
    AlertKeywords,
    BrowserManagementKeywords,
    CookieKeywords,
    ElementKeywords,
    FormElementKeywords,
    FrameKeywords,
    JavaScriptKeywords,
    RunOnFailureKeywords,
    ScreenshotKeywords,
    SelectElementKeywords,
    TableElementKeywords,
    WaitingKeywords,
    WindowKeywords):
    
    def __init__(self, screenshot_root_directory='logs', remote_url=ST.REMOTE_URL, browser=ST.BROWSER, headless=False, alias=None, device=None, executable_path=None, options=None, service_args=None, desired_capabilities=None):
        """
        启动浏览器类型可选: Firefox, Chrome, Ie, Opera, Safari, PhantomJS, 可模拟移动设备
        """
        if browser not in ['Firefox', 'Chrome', 'Ie', 'Opera', 'Safari', 'PhantomJS']:
            raise Exception('浏览器类型不对, 仅可选: Firefox, Chrome, Ie, Opera, Safari, PhantomJS')
        ctx = SeleniumLibrary(screenshot_root_directory=screenshot_root_directory)
        if remote_url:
            if browser == 'Chrome':
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-setuid-sandbox')
                if headless:
                    chrome_options.add_argument('--headless')
                    chrome_options.add_argument('--disable-gpu')
                if device:
                    mobile_emulation = {'deviceName': device}
                    chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
                options = chrome_options
            elif browser == 'Firefox':
                firefox_options = webdriver.FirefoxOptions()
                if headless:
                    firefox_options.add_argument('--headless')
                    firefox_options.add_argument('--disable-gpu')
                options = firefox_options
            desired_capabilities = desired_capabilities or {}
            desired_capabilities['browserName'] = browser.lower()
            driver = WebRemote(command_executor=remote_url, desired_capabilities=desired_capabilities, options=options)
            # ctx.create_webdriver(driver_name='Remote', alias=alias, command_executor=remote_url, options=options, desired_capabilities=desired_capabilities)
        elif browser == 'Chrome': 
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-setuid-sandbox')
            if headless:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-gpu')
            if device:
                mobile_emulation = {'deviceName': device}
                chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
            if executable_path:
                driver = WebChrome(executable_path=executable_path, options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, executable_path=executable_path, options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
            else:
                driver = WebChrome(options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, options=options or chrome_options, service_args=service_args, desired_capabilities=desired_capabilities)
        elif browser == 'Firefox':
            firefox_options = webdriver.FirefoxOptions()
            if headless:
                firefox_options.add_argument('--headless')
                firefox_options.add_argument('--disable-gpu')
            if executable_path:
                driver = WebFirefox(executable_path=executable_path, options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, executable_path=executable_path, options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
            else:
                driver = WebFirefox(options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
                # ctx.create_webdriver(driver_name=browser, alias=alias, options=options or firefox_options, service_args=service_args, desired_capabilities=desired_capabilities)
        else:
            if executable_path:
                ctx.create_webdriver(driver_name=browser, alias=alias, executable_path=executable_path, service_args=service_args, desired_capabilities=desired_capabilities)
            else:
                ctx.create_webdriver(driver_name=browser, alias=alias, service_args=service_args, desired_capabilities=desired_capabilities)
            driver = ctx.driver
        ctx.register_driver(driver=driver, alias=alias)
        self.screenshot_directory = ctx.screenshot_root_directory
        super(AirSelenium, self).__init__(ctx)
    
    @logwrap
    def find_element(self, locator, tag=None, required=True, parent=None):
        web_element = super(AirSelenium, self).find_element(locator=locator, tag=tag, required=required, parent=parent)
        log_res=self._gen_screen_log(web_element)
        return Element(web_element, log_res)

    @logwrap
    @allure.step
    def click_element(self, locator, modifier=False, action_chain=False):
        super(AirSelenium, self).click_element(locator=locator, modifier=modifier, action_chain=action_chain)

    @logwrap
    @allure.step
    def click_link(self, locator, modifier=False):
        super(AirSelenium, self).click_link(locator=locator, modifier=modifier)

    @logwrap
    @allure.step
    def click_image(self, locator, modifier=False):
        super(AirSelenium, self).click_image(locator=locator, modifier=modifier)

    @logwrap
    @allure.step
    def click_button(self, locator, modifier=False):
        super(AirSelenium, self).click_button(locator=locator, modifier=modifier)

    @logwrap
    @allure.step
    def input_text(self, locator, text, clear=True):
        super(AirSelenium, self).input_text(locator=locator, text=text, clear=clear)

    @logwrap
    @allure.step
    def input_password(self, locator, password, clear=True):
        super(AirSelenium, self).input_password(locator=locator, password=password, clear=clear)

    @logwrap
    @allure.step
    def double_click_element(self, locator):
        super(AirSelenium, self).double_click_element(locator=locator)

    @logwrap
    def page_should_contain(self, text, loglevel='TRACE'):
        super(AirSelenium, self).page_should_contain(text=text, loglevel=loglevel)

    @logwrap
    def page_should_not_contain(self, text, loglevel='TRACE'):
        super(AirSelenium, self).page_should_not_contain(text=text, loglevel=loglevel)

    @logwrap
    @allure.step
    def open_context_menu(self, locator):
        super(AirSelenium, self).open_context_menu(locator=locator)

    @logwrap
    @allure.step
    def mouse_up(self, locator):
        super(AirSelenium, self).mouse_up(locator=locator)
    
    @logwrap
    @allure.step
    def mouse_down(self, locator):
        super(AirSelenium, self).mouse_down(locator=locator)

    @logwrap
    @allure.step
    def mouse_over(self, locator):
        super(AirSelenium, self).mouse_over(locator=locator)

    @logwrap
    @allure.step
    def mouse_out(self, locator):
        super(AirSelenium, self).mouse_out(locator=locator)

    @logwrap
    @allure.step
    def drag_and_drop(self, locator, target):
        super(AirSelenium, self).drag_and_drop(locator=locator, target=target)

    @logwrap
    @allure.step
    def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
        super(AirSelenium, self).drag_and_drop_by_offset(locator=locator, xoffset=xoffset, yoffset=yoffset)

    @logwrap
    @allure.step
    def go_to(self, url):
        super(AirSelenium, self).go_to(url=url)

    def screenshot(self, file_path=None):
        if file_path:
            file = self.capture_page_screenshot(file_path)
            with open(file, 'rb') as fp:
                allure.attach(fp.read(), '截图{}'.format(file_path), allure.attachment_type.PNG)
        else:
            if not self.screenshot_directory:
                file_path = "temp.png"
            else:
                file_path = os.path.join('', "temp.png")
            file = self.capture_page_screenshot(file_path)
            with open(file, 'rb') as fp:
                allure.attach(fp.read(), '截图{}'.format(file_path), allure.attachment_type.PNG)
            screen = aircv.imread(file_path)
            return screen

    def _gen_screen_log(self, element=None, filename=None,):
        if self.screenshot_directory is None:
            return None
        if filename:
            self.screenshot(filename)
        jpg_file_name=str(int(time.time())) + '.png'
        jpg_path=os.path.join('', jpg_file_name)
        # print("this is jpg path:", jpg_path)
        self.screenshot(jpg_path)
        saved={"screen": jpg_file_name}
        if element:
            size=element.size
            location=element.location
            x=size['width'] / 2 + location['x']
            y=size['height'] / 2 + location['y']
            if "darwin" in sys.platform:
                x, y=x * 2, y * 2
            saved.update({"pos": [[x, y]]})
        return saved

    @property
    def log_dir(self):
        try:
            if os.path.isdir(self.screenshot_directory):
                return os.path.abspath(self.screenshot_directory)
            else:
                os.makedirs(self.screenshot_directory)
                return os.path.abspath(self.screenshot_directory)
        except RobotNotRunningError:
            return os.getcwd() if PY2 else os.getcwd()
