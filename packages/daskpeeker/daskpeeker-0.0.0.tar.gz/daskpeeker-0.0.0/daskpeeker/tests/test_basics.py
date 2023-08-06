import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from daskpeeker.tests.peeker_for_testing import test_peeker_default_address

left_c1_input_1_xpath = '//*[@id="c1-left"]/label[1]/input'
left_apply_xpath = '//*[@id="apply-button-left"]'


def _init_browser(browser):
    browser.get(test_peeker_default_address)
    WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, left_c1_input_1_xpath))
    )


def test_peeker_setup(browser):
    requests.get(test_peeker_default_address)
    _init_browser(browser)

    elem = browser.find_element_by_xpath(left_c1_input_1_xpath)
    elem.click()

    filt_but = browser.find_element_by_xpath(left_apply_xpath)
    filt_but.click()
