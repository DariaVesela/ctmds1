from interface import PriceGeneratorBase
import random

class standardPrices(PriceGeneratorBase):
    def _generate_prices_implementation(self, num: int) -> list[float]:
        if not isinstance(num, int) or num < 0:
            raise ValueError("num must be a positive integer")
        else:
            return [round(random.uniform(0, 100), 2) for _ in range(num)]
    
    def standard_price_generation(self, num:int)-> list[float]:
        return self._generate_prices_implementation(num)





