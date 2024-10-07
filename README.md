## Development and Testing Setup

This guide will help you get your local environment set up for development and testing.

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

If you want to install additional dependencies for development and testing, use:

```bash
uv pip install -e .[dev,test]
```

### 4. Set Up Pre-Commit Hooks

The project uses `pre-commit` to enforce code standards before committing changes. To set up the pre-commit hooks, run:

```bash
pre-commit install
```

### 5. Running Tests

The project uses `pytest` as its test runner. Once you’ve installed the development and test dependencies, you can run the tests using:

```bash
pytest
```

This will look for tests in the `tests` directory and execute them.

### 6. Linting and Formatting Code

The project uses `ruff` for linting and formatting code. You can manually run the linter to check and fix code quality issues by executing:

```bash
uvx ruff check . --fix
uvx ruff format .
```
