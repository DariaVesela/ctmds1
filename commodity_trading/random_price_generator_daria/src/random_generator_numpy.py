from interface import PriceGeneratorBase
import numpy as np

class randomPricesNumpy(PriceGeneratorBase):
    def random_prices_numpy(self,num:int)->list[float]:
        return  np.random.rand(num)
