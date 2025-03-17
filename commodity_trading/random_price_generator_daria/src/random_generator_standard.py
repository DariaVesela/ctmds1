from interface import PriceGeneratorBase
import random

class standardPrices(PriceGeneratorBase):
    def standard_price_generation(self, num:int)-> list[float]:
        return num * random.randrange(0,100)