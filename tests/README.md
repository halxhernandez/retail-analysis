# Tests Unitarios

## Ejecutar todos los tests

```bash

python -m pytest tests/ -v

```

O con unittest:

```bash

python -m unittest discover tests/ -v

```

## Ejecutar test específico

```bash

python -m unittest tests.test_data_loader.TestRetailDataLoader.test_clean_data_removes_nulls

```

## Coverage

```bash

coverage run -m pytest tests/

coverage report

coverage html

```
