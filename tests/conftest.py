import allure
import pytest
from selene import browser
import requests
from allure_commons.types import AttachmentType

EMAIL = 'Stanmr7n@gmail.com'
PASSWORD = 'k3K9uQV$z#jGj'
URL = 'https://demowebshop.tricentis.com'


def auth_with_api():
    response_auth = requests.post(
        url=URL + '/login',
        data={'Email': EMAIL, 'Password': PASSWORD},
        allow_redirects=False
    )
    cookie = response_auth.cookies.get("NOPCOMMERCE.AUTH")
    allure.attach(body=response_auth.text, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt')
    allure.attach(body=cookie, name='Cookie', attachment_type=AttachmentType.TEXT, extension='.txt')

    return cookie


@pytest.fixture(autouse=True)
def browser_management():
    browser.config.base_url = URL
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield

    browser.quit()
