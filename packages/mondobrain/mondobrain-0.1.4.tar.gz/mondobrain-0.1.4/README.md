# MondoBrain Python SDK

MondoBrain Python SDK is a python wrapper for the MondoBrain API that provides additional functionality such as dataframe ingest and one-off processing

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install mondobrain.

```bash
pip install mondobrain
```

## Dependencies

- [python3](https://www.python.org/downloads/)

## Install from source

In the `mondobrain-python` directory (same directory as this README.md file), run this command in your terminal:
```bash
pip install -e .
```

## Usage
```python
import mondobrain as mb

# Set your credentials
mb.api_key = "<API-KEY>"
mb.api_secret = "<API-SECRET>"

# Build a pandas dataframe and store in `df` (not shown)

# Convert your pandas df to a mondobrain df
mdf = mb.MondoDataFrame(df)

# Select a column as your outcome column & specify a target class
outcome = mdf["column_name"]

# for a discrete column
outcome.target_class = "Some_modality"

# for a continuous column the value should be `min` or `max`
outcome.target_class = "max"

# Get a dataframe of all columns you want to explor
explorable = mdf[["column_a", "column_b"]]

# Create a solver instance
solver = mb.Solver()

# Fit your data
solver.fit(explorable, outcome)

# Check your results
solver.rule
```

See documentation and `SDK Example.ipynb` in the `mondobrain-python` directory for more in depth examples.

The package includes documentation to provide explanation and examples of usage.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Take a look at `CONTRIBUTING.md` for more info

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)