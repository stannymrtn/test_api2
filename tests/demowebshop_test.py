import logging
import allure
import requests
from allure_commons.types import AttachmentType
from selene import browser, be
from tests.conftest import auth_with_api, URL


def add_product_to_cart(product_url, cookie):
    response = requests.post(
        url=URL + product_url,
        cookies={"NOPCOMMERCE.AUTH": cookie}
    )
    allure.attach(body=response.text, name='Response', attachment_type=AttachmentType.TEXT, extension='.txt')
    logging.info(response.status_code)
    logging.info(response.text)

    return response.status_code


def clear_cart():
    browser.element('.qty-input').send_keys('0').press_enter()


def test_add_product():
    with allure.step('API-авторизация'):
        cookie = auth_with_api()

    with allure.step('Открываем страницу'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with allure.step('Добавляем товар в корзину через API'):
        response_code = add_product_to_cart(product_url='/addproducttocart/catalog/31/1/1', cookie=cookie)
        assert response_code == 200

    with allure.step('Проверяем отображение товара в корзине'):
        browser.element('.ico-cart .cart-label').click()
        browser.element('.product-picture').should(be.visible)

    with allure.step('Чистим корзину'):
        clear_cart()


def test_add_one_more_products():
    with allure.step('API-авторизация'):
        cookie = auth_with_api()

    with allure.step('Открываем страницу'):
        browser.open('/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('/')

    with allure.step('Добавляем несколько товаров в корзину'):
        response_code1 = add_product_to_cart(product_url='/addproducttocart/catalog/40/1/1', cookie=cookie)
        assert response_code1 == 200
        response_code2 = add_product_to_cart(product_url='/addproducttocart/catalog/75/1/1', cookie=cookie)
        assert response_code2 == 200

    with allure.step('Чистим корзину'):
        browser.open('/cart')
        clear_cart()
