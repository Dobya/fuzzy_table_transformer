# Fuzzy Table Converter

This utility allows you to convert a source CSV based on a provided template and save the converted data to a target CSV file.

## Installation

### Virtual Environment

Before installing the required Python packages, it's a good practice to set up a virtual environment. This ensures that the packages used in this project don't interfere with other projects or system-wide packages.

1. First, install `virtualenv` if you haven't already:

```bash
pip install virtualenv
```

2. Next, navigate to the project directory and set up a virtual environment:

```bash
virtualenv venv
```

3. Activate the virtual environment:

- On Windows:
  ```bash
  venv\Scripts\activate
  ```

- On macOS and Linux:
  ```bash
  source venv/bin/activate
  ```

### Installing Requirements

After activating the virtual environment, you can install the required Python packages using:

```bash
pip install -r requirements.txt
```

## Usage

You can use the `convert_table.py` script as follows:

```bash
usage: convert_table.py [-h] -s SOURCE -t TEMPLATE [-o TARGET] [--separator SEPARATOR] [--depth DEPTH]
```

### Options:

- `-h, --help`  
  Show the help message and exit.

- `-s SOURCE, --source SOURCE`  
  Path to the source CSV file.

- `-t TEMPLATE, --template TEMPLATE`  
  Path to the template CSV file.

- `-o TARGET, --target TARGET`  
  Path to the target CSV file where results will be saved. If not specified, the result will be printed to the console.

- `--separator SEPARATOR`  
  Separator used in the CSV files. Default is a comma `,`.

- `--d DEPTH, --depth DEPTH`  
  Count of sample values from table to use for a type inference. Default: 5