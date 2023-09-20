"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture(scope='function')
def list_of_products():
    book = Product("book", 100, "This is a book", 1000)
    new_book = Product('new_book', 17, 'This is new book', 30)
    other_book = Product('other_book', 3.5, 'This is other book', 50)
    return {'book': book, 'new_book': new_book, 'other_book': other_book}

@pytest.fixture()
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """
    # TODO напишите проверки на метод check_quantity
    def test_product_check_quantity(self, list_of_products):
        equal_quantity = list_of_products['book'].quantity
        assert list_of_products['book'].check_quantity(equal_quantity)

        less_quantity = list_of_products['book'].quantity - 1
        assert list_of_products['book'].check_quantity(less_quantity)

        more_quantity = list_of_products['book'].quantity + 1
        assert not list_of_products['book'].check_quantity(more_quantity)

        much_more_quantity = list_of_products['book'].quantity + 1000
        assert not list_of_products['book'].check_quantity(much_more_quantity)

    def test_product_buy(self, list_of_products):

        list_of_products['book'].buy(1)
        assert list_of_products['book'].quantity == 999

        list_of_products['new_book'].buy(15)
        assert list_of_products['new_book'].quantity == 15

        list_of_products['other_book'].buy(50)
        assert list_of_products['other_book'].quantity == 0

    def test_product_buy_more_than_available(self, list_of_products):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        more_quantity = list_of_products['book'].quantity + 1
        with pytest.raises(ValueError):
            assert list_of_products['book'].buy(more_quantity) == ValueError


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_one_product(self, list_of_products, cart):
        cart.add_product(list_of_products['new_book'])
        assert cart.products[list_of_products['new_book']] == 1
    def test_add_product(self,list_of_products,cart):
        cart.add_product(list_of_products['new_book'], 5)
        cart.add_product(list_of_products['new_book'], 7)

        assert len(cart.products) == 1
        assert cart.products[list_of_products['new_book']] == 12

    def test_one_more_product(self,list_of_products,cart):
        cart.add_product(list_of_products['new_book'], 7)
        cart.add_product(list_of_products['other_book'], 17)

        assert len(cart.products) == 2
        assert cart.products[list_of_products['other_book']] == 17


    def test_reduce_quantity(self, list_of_products, cart):
        cart.add_product(list_of_products['new_book'], 5)
        cart.remove_product(list_of_products['new_book'],3)

        assert cart.products[list_of_products['new_book']] == 2
        assert len(cart.products) == 1

    def test_delete_without_quantity(self,list_of_products,cart):
        cart.add_product(list_of_products['new_book'], 5)
        cart.remove_product(list_of_products['new_book'])

        assert len(cart.products) == 0

    def test_remove_large_quantities(self,list_of_products,cart):
        cart.add_product(list_of_products['new_book'], 50)
        cart.remove_product(list_of_products['new_book'],500)

        assert len(cart.products) == 0

    def test_clear_cart(self, list_of_products, cart):
        cart.add_product(list_of_products['book'], 1000)
        cart.clear()

        assert len(cart.products) == 0

    def test_get_total_price_product(self, list_of_products, cart):

        cart.add_product(list_of_products['new_book'], 3)
        assert cart.get_total_price() == 51

    def test_get_total_price(self, list_of_products, cart):
        cart.add_product(list_of_products['other_book'])

        assert len(cart.products) == 1
        assert cart.get_total_price() == 3.5

    def test_get_total_price_other(self,list_of_products,cart):
        cart.add_product(list_of_products['other_book'], 10)

        assert cart.get_total_price() == 35
