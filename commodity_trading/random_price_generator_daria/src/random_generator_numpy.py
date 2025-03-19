from interface import PriceGeneratorBase
import numpy as np

class randomPricesNumpy(PriceGeneratorBase):
    def _generate_prices_implementation(self,num:int)->list[float]:
        if not isinstance(num, int) or num < 0:
            raise ValueError("num must be a positive integer")
        else:
            return  np.round(np.random.rand(num), 2)
    
    def random_prices_numpy(self, num:int)->list[float]:
        return self._generate_prices_implementation(num)
    


