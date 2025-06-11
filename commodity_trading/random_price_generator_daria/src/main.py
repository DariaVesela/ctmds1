import typer
from enum import Enum
from typing import Optional
import time
from pathlib import Path
import pendulum
from interface import PriceGeneratorBase
from random_generator_standard import StandardPrices
from random_generator_numpy import RandomPricesNumpy

# Create a Typer app
app = typer.Typer(help="Generate random prices using different implementations")

# Define an enum 
class GeneratorType(str, Enum):
    STANDARD = "standard"
    NUMPY = "numpy"

# Country base prices mapping
COUNTRY_BASE_PRICES = {
    "GB": 61,
    "FR": 58, 
    "NL": 52,
    "DE": 57,
    "BE": 62
}

def get_dst_info_for_date(date_str: str, country_code: str) -> dict:
    """Get DST information for a specific date and country using pendulum."""
    # Line 1: Parse date and set timezone based on country
    timezone_map = {
        "GB": "Europe/London",
        "FR": "Europe/Paris", 
        "NL": "Europe/Amsterdam",
        "DE": "Europe/Berlin",
        "BE": "Europe/Brussels"
    }
    
    # Line 2-3: Create pendulum datetime for the target date in local timezone
    tz = timezone_map[country_code]
    target_date = pendulum.parse(date_str).in_timezone(tz)
    
    # Line 4-5: Check the day before, target day, and day after for DST transitions
    day_before = target_date.subtract(days=1)
    day_after = target_date.add(days=1)
    
    # Line 6-8: Detect DST transitions by checking UTC offset changes
    target_offset = target_date.utc_offset()
    before_offset = day_before.utc_offset()
    after_offset = day_after.utc_offset()
    
    # Line 9-16: Determine the type of day
    if before_offset != target_offset:
        # DST transition happened between day_before and target_date
        if target_offset > before_offset:
            return {"type": "fall_back", "hours": 25}  # Gained an hour
        else:
            return {"type": "spring_forward", "hours": 23}  # Lost an hour
    elif target_offset != after_offset:
        # DST transition happens between target_date and day_after
        if after_offset > target_offset:
            return {"type": "fall_back", "hours": 25}  # Will gain an hour
        else:
            return {"type": "spring_forward", "hours": 23}  # Will lose an hour
    else:
        return {"type": "normal", "hours": 24}

def calculate_periods_for_date(date_str: str, granularity: str, country_code: str) -> int:
    """Calculate number of time periods for a given date considering DST."""
    # Line 1: Get DST info for the specific date and country
    dst_info = get_dst_info_for_date(date_str, country_code)
    hours = dst_info["hours"]
    
    # Line 2-6: Calculate periods based on granularity
    if granularity == "h":
        return hours
    elif granularity == "hh":
        return hours * 2  # Two 30-minute periods per hour
    else:
        raise ValueError(f"Invalid granularity: {granularity}")

def format_prices_with_time_labels(prices: list[float], date_str: str, granularity: str, country_code: str) -> list[str]:
    """Format prices with time labels like '0000: 57.35'."""
    # Line 1-2: Set up timezone and parse date
    timezone_map = {
        "GB": "Europe/London",
        "FR": "Europe/Paris", 
        "NL": "Europe/Amsterdam",
        "DE": "Europe/Berlin",
        "BE": "Europe/Brussels"
    }
    
    # Line 3-4: Create pendulum datetime for midnight of target date
    tz = timezone_map[country_code]
    target_date = pendulum.parse(date_str).in_timezone(tz).start_of('day')
    
    # Line 5-6: Get DST information for this date
    dst_info = get_dst_info_for_date(date_str, country_code)
    
    formatted_prices = []
    price_index = 0
    
    # Line 7-8: Start at midnight
    current_time = target_date
    
    # Line 9-10: Determine time increment based on granularity
    if granularity == "h":
        increment = pendulum.duration(hours=1)
    else:  # granularity == "hh"
        increment = pendulum.duration(minutes=30)
    
    # Line 11-35: Generate time labels for the entire day
    while price_index < len(prices):
        # Line 12-13: Format time as HHMM
        time_str = current_time.format("HHmm")
        
        # Line 14-15: Create the formatted string
        formatted_prices.append(f"{time_str}: {prices[price_index]:.2f}")
        
        # Line 16-17: Move to next time period
        price_index += 1
        next_time = current_time.add(**increment.total_seconds_dict())
        
        # Line 18-30: Handle DST transitions using pendulum's built-in logic
        if dst_info["type"] == "spring_forward":
            # Pendulum automatically handles the missing hour
            # If we're about to enter the non-existent hour, pendulum will skip it
            pass
        elif dst_info["type"] == "fall_back":
            # Pendulum handles the repeated hour automatically
            # We need to ensure we capture both instances of the repeated hour
            if current_time.format("HH") == "01" and next_time.format("HH") == "03":
                # We're about to skip the second occurrence of 02:xx
                # Add the second 02:xx hour manually
                temp_time = current_time.add(hours=1)  # This will be 02:xx again
                while temp_time.format("HH") == "02" and price_index < len(prices):
                    time_str = temp_time.format("HHmm")
                    formatted_prices.append(f"{time_str}: {prices[price_index]:.2f}")
                    price_index += 1
                    if price_index < len(prices):
                        temp_time = temp_time.add(**increment.total_seconds_dict())
                next_time = temp_time
        
        current_time = next_time
        
        # Line 31-32: Break if we've processed all prices or moved to next day
        if current_time.day != target_date.day and price_index >= len(prices):
            break
    
    return formatted_prices

@app.command()
def generate(
    for_date: str = typer.Argument(..., help="Date for hourly prices (YYYY-MM-DD)"),
    country_code: str = typer.Argument(..., help="Country code (GB, FR, NL, DE, BE)"),
    generator: GeneratorType = typer.Option(
        GeneratorType.STANDARD, 
        help="Type of generator to use"
    ),
    granularity: str = typer.Option(
        "h", 
        "--granularity", 
        help="Granularity: 'h' for hourly, 'hh' for half-hourly"
    ),
    output_file: Optional[Path] = typer.Option(
        None, "--output", "-o", help="Output file to save the prices"
    )
):
    """Generate random hourly/half-hourly prices for a specific date and country."""
    
    # Line 1-2: Validate country code
    if country_code not in COUNTRY_BASE_PRICES:
        typer.echo(f"Error: Unsupported country code: {country_code}. Supported: {list(COUNTRY_BASE_PRICES.keys())}", err=True)
        raise typer.Exit(code=1)
    
    # Line 3-4: Validate granularity
    if granularity not in ["h", "hh"]:
        typer.echo("Error: Granularity must be 'h' or 'hh'", err=True)
        raise typer.Exit(code=1)
    
    # Line 5-6: Validate and parse date
    try:
        pendulum.parse(date_str)
    except ValueError:
        typer.echo("Error: Date must be in YYYY-MM-DD format", err=True)
        raise typer.Exit(code=1)
    
    try:
        # Line 7-8: Calculate number of time periods needed
        count = calculate_periods_for_date(for_date, granularity, country_code)
        
        # Line 9-10: Get base price for the country
        base_price = COUNTRY_BASE_PRICES[country_code]
        
        # Line 11-13: Set price range for normal distribution simulation
        # Using ±20% of base price as reasonable bounds for normal distribution
        std_dev = base_price * 0.1  # 10% standard deviation
        min_price = base_price - (2 * std_dev)  # About 95% of values within this range
        max_price = base_price + (2 * std_dev)
        
        # Line 14-18: Create the appropriate generator with calculated price range
        if generator == GeneratorType.STANDARD:
            price_generator = StandardPrices(min_price=min_price, max_price=max_price)
        elif generator == GeneratorType.NUMPY:
            price_generator = RandomPricesNumpy(min_price=min_price, max_price=max_price)
        else:
            typer.echo(f"Error: Unknown generator type: {generator}", err=True)
            raise typer.Exit(code=1)
        
        # Line 19-20: Generate the prices
        typer.echo(f"Generating {count} prices for {country_code} on {for_date} ({granularity} granularity)...")
        start_time = time.time()
        prices = price_generator.generate_prices(count)
        generation_time = time.time() - start_time
        
        # Line 21-22: Format prices with time labels
        formatted_prices = format_prices_with_time_labels(prices, for_date, granularity, country_code)
        
        # Line 23-35: Output the results
        if output_file:
            try:
                with open(output_file, "w") as f:
                    for formatted_price in formatted_prices:
                        f.write(f"{formatted_price}\n")
                typer.echo(f"Generated {count} prices for {country_code} on {for_date} and saved to {output_file}")
                typer.echo(f"Generation time: {generation_time:.4f} seconds")
            except IOError as e:
                typer.echo(f"Error writing to file: {e}", err=True)
                raise typer.Exit(code=1)
        else:
            typer.echo(f"\nGenerated prices for {country_code} on {for_date}:")
            for formatted_price in formatted_prices:
                typer.echo(formatted_price)
            typer.echo(f"\nGeneration time: {generation_time:.4f} seconds")
            typer.echo(f"Base price for {country_code}: {base_price}")
    
    except (RuntimeError, ValueError) as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)

# Keep your existing compare function unchanged
@app.command()
def compare(
    count: int = typer.Argument(10000, help="Number of random prices to generate"),
    min_price: float = typer.Option(0.01, "--min", help="Minimum price value"),
    max_price: float = typer.Option(100.0, "--max", help="Maximum price value"),
    runs: int = typer.Option(3, "--runs", help="Number of runs for more accurate timing")
):
    """Compare the performance of standard and numpy implementations."""
    # Your existing compare function code here...
    pass

if __name__ == "__main__":
    app()