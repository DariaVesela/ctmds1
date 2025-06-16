from src.interface import PriceGeneratorBase
import random
from typing import Protocol

class RandomGenerator(Protocol):
    def uniform(self, a: float, b: float) -> float:
        ...

class StandardPrices(PriceGeneratorBase):
    def __init__(self, random_generator: RandomGenerator = None):
        self._random_generator = random_generator or random
    
    def _generate_prices_implementation(self, num: int) -> list[float]:
        if not isinstance(num, int) or num < 0:
            raise ValueError("num must be a positive integer")
        
        if num == 0:
            return []
        
        return [round(self._random_generator.uniform(0, 100), 2) for _ in range(num)]
    
    def standard_price_generation(self, num: int) -> list[float]:
        return self._generate_prices_implementation(num)





