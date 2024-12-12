# Hifz

A flashcard application.

## Development and Testing Setup

### 1. Clone the Repository

First, clone the repository from GitHub to your local machine:

```bash
git clone https://github.com/EthanHaque/hifz
cd hifz
```

### 2. Create a Virtual Environment

```bash
uv venv
source .venv/bin/activate
```

### 3. Install Dependencies

Now that you're in the project directory, install the required dependencies. The `pyproject.toml` file defines the necessary packages. Run the following command to install the base dependencies:

```bash
uv pip install -e .
```

If you want to install additional dependencies for testing and gui use:

```bash
uv pip install -e .[test,gui]
```

### 4. Running Tests

The project uses `pytest` as its test runner. Once you’ve installed the development and test dependencies, you can run the tests using:

```bash
pytest
```

This will look for tests in the `tests` directory and execute them.

### 5. Set Up Pre-Commit Hooks

The project uses `pre-commit` to enforce code standards before committing changes. To set up the pre-commit hooks, run:

```bash
uvx pre-commit install
```

### 6. Linting and Formatting Code

The project uses `ruff` for linting and formatting code. You can manually run the linter to check and fix code quality issues by executing:

```bash
uvx ruff check . --fix --show-fixes
uvx ruff format .
```

> [!TIP]
> We do not list pre-commit, ruff, and mypy as development dependencies. As they are tools, not dependencies. If you would like to use these tools in an isolated environment, use `uv tool install`, and you'll be able to run them anywhere for any relevant projects on your computer from an isolated environment.

## Usage

To see general program usage information, run:
```bash
uv run src/hifz -h
```

Here are some examples one can run the dummy data:
```bash
python -m pip install -e .[gui,tui]
python -m hifz cli random --source data/arabic_letters.json
python -m hifz gui mastery --source data/fruits.csv
python -m hifz gui mastery --source https://raw.githubusercontent.com/EthanHaque/hifz/refs/heads/main/data/fruits.csv
```
