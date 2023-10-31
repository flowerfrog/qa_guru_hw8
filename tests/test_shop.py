import random

import allure
import pytest

from tests.models import Product, Cart


@allure.tag("web")
@allure.label("owner", "flowerfrog")
@allure.feature("Тестирование классов интернет магазина")
@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


@allure.story("Тестирование класса Product")
class TestProducts:

    def test_product_check_quantity(self, product):
        books = product.quantity
        assert product.check_quantity(books) is True
        assert product.check_quantity(books - 1) is True
        assert product.check_quantity(books + 1) is False

    def test_product_buy(self, product):
        books = product.quantity
        quantity = random.randint(1, books)
        product.buy(quantity)
        assert product.quantity >= 0

    def test_product_buy_more_than_available(self, product):
        books = product.quantity
        quantity = random.randint(books + 1, books + 10)
        with pytest.raises(ValueError):
            product.buy(quantity)


@allure.story("Тестирование класса Cart")
class TestCart:

    def test_add_product(self, product, cart):
        cart.add_product(product)
        assert product in cart.products
        assert cart.products[product] == 1

    def test_remove_product(self, product, cart):
        cart.add_product(product)
        cart.remove_product(product)
        assert product not in cart.products

    def test_clear(self, product, cart):
        books = product.quantity
        quantity = random.randint(1, books)
        cart.add_product(product, quantity)
        cart.clear()
        assert product not in cart.products

    def test_total_price(self, product, cart):
        cart.clear()
        assert cart.get_total_price() == 0
        books = product.quantity
        quantity = random.randint(1, books)
        cart.add_product(product, quantity)
        assert cart.get_total_price() == quantity * product.price

    def test_buy(self, product, cart):
        books = product.quantity
        books_in_order = random.randint(1, books)
        cart.add_product(product, books_in_order)
        cart.buy()
        assert product not in cart.products
        assert product.quantity == books - books_in_order

    def test_buy_more_than_quantity(self, product, cart):
        product.quantity = 0
        cart.add_product(product)
        with pytest.raises(ValueError):
            cart.buy()
