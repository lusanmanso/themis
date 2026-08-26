# 🛠️ Contributing

## Setup

```bash
# Clone and install all dependencies (including dev)
git clone https://github.com/lusanmanso/themis.git
cd themis
uv sync
```

---

## Running code

```bash
# Run any Python file
uv run python src/themis/holc.py

# Import interactively
uv run python -c "from themis import load_raw; print(load_raw().shape)"
```

---

## Tests

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run a single file
uv run pytest tests/test_holc.py

# Run a single test
uv run pytest tests/test_holc.py::test_extract_dominant_on_synthetic_data
```

---

## Linting & formatting (ruff)

```bash
# Check for errors
uv run ruff check .

# Auto-fix
uv run ruff check . --fix

# Format code
uv run ruff format .
```

---

## Adding dependencies

```bash
# Add a project dependency
uv add <package>

# Add a dev-only dependency
uv add --dev <package>
```

---

## Clear cache

```bash
ruff clean
uv cache clean
```
