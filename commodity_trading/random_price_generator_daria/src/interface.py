from abc import ABC, abstractmethod

class PriceGeneratorBase(ABC):

    def generate_prices(self, num:int)->list[float]:
        if num < 0:
            raise RuntimeError("Number of items must be greater or equal to 0")

        return self._generate_prices_implementation(num)

    @abstractmethod
    def _generate_prices_implementation(self, num: int) -> list[float]:
        """Implementation of the actual random price generation."""
        pass
