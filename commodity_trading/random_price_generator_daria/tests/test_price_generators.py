import pytest
from src.random_generator_numpy import randomPricesNumpy
from src.random_generator_standard import standardPrices
from src.interface import PriceGeneratorBase

class TestStandardPrices:
    def setup_method(self):
        self.generator = standardPrices()

    def test_output_is_list(self):
        prices = self.generator.generate_prices(10)
        assert isinstance(prices, list)

    def test_length_of_list(self):
        num = 15
        #make sure to call the function in the interface!!!
        prices = self.generator.generate_prices(num)
        assert len(prices) == num

    def test_items_are_floats(self):
        prices = self.generator.generate_prices(5)
        for price in prices:
            assert isinstance(price, float)

    def test_price_range(self):
        prices = self.generator.generate_prices(20)
        for price in prices:
            assert 0 <= price <= 100


class TestNumpyPrices:
    def setup_method(self):
        self.generator = randomPricesNumpy()

    def test_output_is_list(self):
        prices = self.generator.generate_prices(10)
        assert isinstance(prices, list)

    def test_length_of_list(self):
        num = 15
        prices = self.generator.generate_prices(num)
        assert len(prices) == num

    def test_items_are_floats(self):
        prices = self.generator.generate_prices(5)
        for price in prices:
            assert isinstance(price, float)

    def test_price_range(self):
        prices = self.generator.generate_prices(20)
        for price in prices:
            assert 0 <= price <= 100
