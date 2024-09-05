import os
import allure
import pytest
from selene import browser
import requests
from allure_commons.types import AttachmentType
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
URL = "https://demowebshop.tricentis.com"


def auth_with_api():
    response_auth = requests.post(
        url=URL + '/login',
        data={'Email': EMAIL, 'Password': PASSWORD},
        allow_redirects=False
    )

    allure.attach(body=response_auth.text, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt')
    allure.attach(body=str(response_auth.headers), name='Response Headers', attachment_type=AttachmentType.TEXT,
                  extension='.txt')


@pytest.fixture(autouse=True)
def browser_management():
    browser.config.base_url = URL
    browser.config.window_height = 1080
    browser.config.window_width = 1920

    yield

    browser.quit()
