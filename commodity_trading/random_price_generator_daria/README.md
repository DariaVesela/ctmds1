# Random Price Generator Daria

This project provides a tool for generating random prices using two different implementations: a standard Python-based generator and a NumPy-based generator. It also includes functionality to compare the performance of these two implementations.

## Features

- Generate random prices using either a standard Python implementation or a NumPy-based implementation.
- Save generated prices to a file or display them in the terminal.
- Compare the performance of the two implementations.

## Requirements

- Python 3.11 or higher
- Dependencies listed in `pyproject.toml`:
  - `mypy`
  - `pytest`
  - `ruff`
  - `numpy`
  - `pandas`
  - `typer`

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd random_price_generator_daria
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

This project uses the `Typer` library to provide a command-line interface. Below are the available commands:

### 1. `generate`

Generate random prices using the specified generator.

#### Syntax:

```bash
python src/main.py generate [OPTIONS] COUNT
```

#### Options:

- `COUNT`: The number of random prices to generate.
- `--generator`: The type of generator to use (`standard` or `numpy`). Default is `standard`.
- `--output`, `-o`: The file to save the generated prices. If not provided, prices will be displayed in the terminal.

#### Example:

Generate 10 prices using the standard generator and display them in the terminal:

```bash
python src/main.py generate 10 --generator standard
```

Generate 20 prices using the NumPy generator and save them to a file:

```bash
python src/main.py generate 20 --generator numpy --output prices.txt
```

---

### 2. `compare`

Compare the performance of the standard and NumPy implementations.

#### Syntax:

```bash
python src/main.py compare [OPTIONS]
```

#### Options:

- `COUNT`: The number of random prices to generate for comparison. Default is 10,000.

#### Example:

Compare the performance of the two implementations for 10,000 prices:

```bash
python src/main.py compare
```

Compare the performance for 50,000 prices:

```bash
python src/main.py compare 50000
```

---

## Running Tests

To run the tests, use `pytest`:

```bash
pytest
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

Daria Vesela  
Email: daria1vesela@gmail.com
