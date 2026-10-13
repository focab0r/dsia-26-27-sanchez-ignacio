# Project I

The project I is composed of two exercises.

## Exercise A

Pipeline:

- Execute the pipeline by using `cli.py`
- Read the CSV (by default [ventas.csv](data/ventas.csv))
- Process and secure the data
- Save the data in another file

### Files

```
├── src
│   └── ventas_app
│       ├── cli.py			# Main code
│       ├── contract.py		# Contract that specifies the order and type of the data. Made with pydantic
│       ├── __init__.py
│       ├── loader.py		# Load the data from a path
│       └── preprocess.py	# Process and clean the data. Check the validity by using the contract
│
├── tests
│   └── ventas_app
│       └── test.py
```

### Execution

Run it from the root of the repo by using `uv`. Omit the `--project` parameter if running from the project I folder.
```
$> uv run --project proyectos/proyecto_i/ python -m ventas_app.cli

usage: cli.py [-h] --input INPUT [--output OUTPUT]
cli.py: error: the following arguments are required: --input
```

Arguments:
- `--input`: Required argument. Specify the input CSV to read. If nothing is specified (`""`), it will use the default one located at [data/ventas.csv](data/ventas.csv).
- `--output`: Save the result inside a new CSV. If not specified, it will just process the data but not save it.

Example of execution:
```
$> uv run --project proyectos/proyecto_i/ python -m ventas_app.cli --input "" --output new_data.csv

[-] Unable to process row 54
[-] Unable to process row 63
[-] Unable to process row 66
[-] Unable to process row 84
[-] Unable to process row 88
[-] Unable to process row 109
[-] Unable to process row 134
[-] Unable to process row 149
```

### Tests

5 tests are saved at [test.py](tests/ventas_app/test.py). Run them with the following command:
```
$> uv run --project proyectos/proyecto_i/ pytest proyectos/proyecto_i/tests/ventas_app/test.py

============================== test session starts ==============================
platform linux -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0
rootdir: [REDACTED]/proyectos/proyecto_i
configfile: pyproject.toml
collected 5 items                                                                                                                                                             

proyectos/proyecto_i/tests/ventas_app/test.py .....                      [100%]

============================== 5 passed in 0.38s ==============================
```


## Exercise B

In this exercise we will try to predict the rain during the summer. Starting from the amount of rain we have observed during each month of the year, the target variable will be the rain during the july and august months. The DataFrame will follow the following format:


Year | September | October | November | December | January | February | March | April | May | June | Target (July+August) |
-----|-----------|---------|----------|----------|---------|----------|-------|-------|-----|------|----------------------|
1990 | 3         | 56      | 10       | 24       | 30      | 35       | 80    | 67    | 15  | 10   | X                    |

The data is extracted from the [open-meteo](https://open-meteo.com/) API, that saves historical weather data from 1940. **For this reason, the dataset will be small** (only 85 rows), as there is no way to extract more data from the past.

Pipeline:

- Execute the pipeline by using `cli.py`
- Download the data from the API
- Process and secure the data
- Save the data in a CSV file, ready to be ingested into the model

### API 

```
https://archive-api.open-meteo.com/v1/archive?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=precipitation_sum&timezone=Europe/Madrid
```
Parameters:
- **latitude**: By default `40.42` (defaults to Madrid)
- **longitude**: By default `-3.70` (defaults to Madrid)
- **start_date**: By default `1940-01-02` (default to the first date saved)
- **end_date**:  By default `2026-10-05`. This will be changed in the future to select the last data available.

### Files

```
├── src
│   └── proyecto_i
│       ├── cli.py			# Main code
│       ├── contract.py		# Contract that specifies the order and type of the data. Made with pydantic
│       ├── __init__.py
│       ├── loader.py		# Download the data from the API
│       └── preprocess.py	# Process and clean the data. Check the validity by using the contract
│
├── tests
│   └── proyecto_i
│       └── test.py
```

An example of the output CSV can be found at [here](data/rain_data.csv)

### Execution

Run it from the root of the repo by using `uv`. Omit the `--project` parameter if running from the project I folder.
```
$> uv run --project proyectos/proyecto_i/ python -m proyecto_i.cli

usage: cli.py [-h] --output OUTPUT
cli.py: error: the following arguments are required: --output
```

Arguments:
- `--output`: Required argument. Save the result inside a CSV.

Example of execution:
```
$> uv run --project proyectos/proyecto_i/ python -m proyecto_i.cli --output new_data.csv

[*] Downloading content...
[+] Content downloaded
[*] Starting preprocess...
[*] Added year 1940 to list
[*] Added year 1941 to list
[*] Added year 1942 to list
[*] Added year 1943 to list
[*] Added year 1944 to list
[*] Added year 1945 to list
[*] Added year 1946 to list
[*] Added year 1947 to list
[...SNIP...]
[*] Added year 2017 to list
[*] Added year 2018 to list
[*] Added year 2019 to list
[*] Added year 2020 to list
[*] Added year 2021 to list
[*] Added year 2022 to list
[*] Added year 2023 to list
[*] Added year 2024 to list
[*] Added year 2025 to list
[+] Finished preprocess
[+] Data sed to file new_data.csv
[+++] Finished
```

### Tests

3 tests are saved at [test.py](tests/proyecto_i/test.py). Run them with the following command:
```
$> uv run --project proyectos/proyecto_i/ pytest proyectos/proyecto_i/tests/proyecto_i/test.py

============================== test session starts ==============================
platform linux -- Python 3.12.14, pytest-9.1.1, pluggy-1.6.0
rootdir: [REDACTED]/proyectos/proyecto_i
configfile: pyproject.toml
collected 3 items                                                                                                                                                             

proyectos/proyecto_i/tests/proyecto_i/test.py ...                        [100%]

============================== 3 passed in 0.69s ==============================
```