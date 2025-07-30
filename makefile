.PHONY: test black-check black-format flake8 isort-check isort-format lint lint-fix all

# Run all tests
test:
	pytest tests/

# Check code formatting with black (no changes, just check)
black-check:
	black --check .

# Automatically format code with black
black-format:
	black --line-length 79 .

# Check code style with flake8
flake8:
	flake8 app tests

# Check import sorting with isort (no changes, just check)
isort-check:
	isort --check-only .

# Automatically sort imports with isort
isort-format:
	isort --line-length 79 .

# Run all quality checks
lint: black-check flake8 isort-check

# Run and fix all quality checks
lint-fix: black-format isort-format flake8

# Run tests and linting
all: lint-fix test