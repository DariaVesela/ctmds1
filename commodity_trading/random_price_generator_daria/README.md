# Commodity Price Generator

A flexible Python library for generating random commodity prices with configurable parameters including forward/backward time periods and granularity settings.

## Features

- **Multiple Generation Strategies**: Standard random prices with extensible architecture
- **Time-based Generation**: Support for forward and backward time periods
- **Configurable Granularity**: Generate prices at different time intervals (daily, hourly, etc.)
- **SOLID Principles**: Clean, testable, and maintainable code architecture
- **Type Safety**: Full type hints and protocol-based interfaces

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd random_price_generator_daria

# Install dependencies (if any)
pip install -r requirements.txt
```

## Quick Start

```python
from src.random_generator_standard import StandardPrices

# Basic usage - generate 10 random prices
generator = StandardPrices()
prices = generator.standard_price_generation(10)
print(prices)  # [45.67, 78.23, 12.89, ...]
```

## Advanced Usage

### Forward/Backward Days

Generate prices for specific time periods relative to a reference date:

```python
from datetime import datetime, timedelta
from src.random_generator_standard import StandardPrices

generator = StandardPrices()

# Generate prices for the next 30 days (forward)
forward_prices = generator.generate_forward_prices(
    reference_date=datetime.now(),
    days=30,
    granularity='daily'
)

# Generate prices for the previous 7 days (backward)
backward_prices = generator.generate_backward_prices(
    reference_date=datetime.now(),
    days=7,
    granularity='daily'
)
```

### Granularity Options

Control the time intervals for price generation:

```python
# Daily prices (default)
daily_prices = generator.generate_prices_with_granularity(
    days=5,
    granularity='daily'
)  # Returns 5 prices (one per day)

# Hourly prices
hourly_prices = generator.generate_prices_with_granularity(
    days=1,
    granularity='hourly'
)  # Returns 24 prices (one per hour)

# Custom interval (every 4 hours)
custom_prices = generator.generate_prices_with_granularity(
    days=2,
    granularity='4h'
)  # Returns 12 prices (every 4 hours for 2 days)
```

### Supported Granularity Values

| Granularity | Description                | Points per Day |
| ----------- | -------------------------- | -------------- |
| `'daily'`   | One price per day          | 1              |
| `'hourly'`  | One price per hour         | 24             |
| `'4h'`      | One price every 4 hours    | 6              |
| `'6h'`      | One price every 6 hours    | 4              |
| `'12h'`     | One price every 12 hours   | 2              |
| `'15min'`   | One price every 15 minutes | 96             |
| `'30min'`   | One price every 30 minutes | 48             |

## API Reference

### StandardPrices Class

#### Methods

- **`standard_price_generation(num: int) -> list[float]`**

  - Generate a specified number of random prices
  - **Parameters**: `num` - Number of prices to generate
  - **Returns**: List of float values between 0-100

- **`generate_forward_prices(reference_date: datetime, days: int, granularity: str = 'daily') -> dict`**

  - Generate prices for future dates
  - **Parameters**:
    - `reference_date` - Starting date for generation
    - `days` - Number of days forward
    - `granularity` - Time interval between prices
  - **Returns**: Dictionary with timestamps as keys and prices as values

- **`generate_backward_prices(reference_date: datetime, days: int, granularity: str = 'daily') -> dict`**
  - Generate prices for past dates
  - **Parameters**:
    - `reference_date` - Starting date for generation
    - `days` - Number of days backward
    - `granularity` - Time interval between prices
  - **Returns**: Dictionary with timestamps as keys and prices as values

## Configuration

### Custom Random Generator

For testing or specific distributions, inject a custom random generator:

```python
class CustomRandom:
    def uniform(self, a: float, b: float) -> float:
        # Your custom logic here
        return your_custom_value

generator = StandardPrices(random_generator=CustomRandom())
```

### Price Range Configuration

Modify the price range by extending the class:

```python
class CustomRangeGenerator(StandardPrices):
    def _generate_prices_implementation(self, num: int) -> list[float]:
        # Generate prices between 50-150 instead of 0-100
        return [round(self._random_generator.uniform(50, 150), 2) for _ in range(num)]
```

## Examples

### Complete Time Series Generation

```python
from datetime import datetime
from src.random_generator_standard import StandardPrices

generator = StandardPrices()

# Generate a complete price history for analysis
start_date = datetime(2024, 1, 1)
historical_data = generator.generate_backward_prices(
    reference_date=datetime.now(),
    days=365,
    granularity='daily'
)

# Generate future projections
future_data = generator.generate_forward_prices(
    reference_date=datetime.now(),
    days=30,
    granularity='hourly'
)

print(f"Historical data points: {len(historical_data)}")
print(f"Future data points: {len(future_data)}")
```

## Testing

Run the test suite to verify functionality:

```bash
python -m pytest tests/
```

For testing with predictable values:

```python
class MockRandom:
    def uniform(self, a: float, b: float) -> float:
        return 75.0  # Fixed value for testing

generator = StandardPrices(random_generator=MockRandom())
assert generator.standard_price_generation(3) == [75.0, 75.0, 75.0]
```

## Contributing

1. Follow SOLID principles
2. Add type hints to all functions
3. Include unit tests for new features
4. Update this README for new functionality

## License

[Your license here]
