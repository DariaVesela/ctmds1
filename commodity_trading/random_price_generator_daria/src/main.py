import typer
from enum import Enum
from typing import Optional

# Import your generators
from interface import PriceGeneratorBase
from random_generator_standard import standardPrices
from random_generator_numpy import randomPricesNumpy

# Create a Typer app
app = typer.Typer()

# Define an enum 
class GeneratorType(str, Enum):
    STANDARD = "standard"
    NUMPY = "numpy"

@app.command()
def generate(
    count: int = typer.Argument(..., help="Number of random prices to generate"),
    generator: GeneratorType = typer.Option(
        GeneratorType.STANDARD, 
        help="Type of generator to use"
    ),
    output_file: Optional[str] = typer.Option(
        None, "--output", "-o", help="Output file to save the prices"
    )
):
    """Generate random prices using different implementations."""
    # Select the appropriate generator
    price_generator: PriceGeneratorBase = None
    if generator == GeneratorType.STANDARD:
        price_generator = standardPrices()
    elif generator == GeneratorType.NUMPY:
        price_generator = randomPricesNumpy()
    
    # Generate prices
    try:
        prices = price_generator.generate_prices(count)
        
        # Output the prices
        if output_file:
            with open(output_file, "w") as f:
                for price in prices:
                    f.write(f"{price}\n")
            typer.echo(f"Generated {count} prices and saved to {output_file}")
        else:
            typer.echo(f"Generated prices: {prices}")
    
    except RuntimeError as e:
        typer.echo(f"Error: {str(e)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()