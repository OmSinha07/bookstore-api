# 🧪 Tests for Bookstore API

This folder contains all the tests for the API application, divided into:

- `unit/`: Unit tests (with and without mocking)
- `integration/`: Integration tests for CRUD operations
- `api/`: Endpoint behavior tests simulating actual client requests

##  Tools Used

- pytest
- coverage
- unittest.mock (via pytest-mock)

##  Commands

### Run All Tests

bash<br>
python -m pytest


## Run Only Unit Tests

bash<br>
python -m pytest tests/unit/<br>
python -m pytest --cov=app tests/unit/ --cov-report=term-missing<br>  

## Run Integration Tests

bash<br>
python -m pytest tests/integration/

## Run API Tests

bash<br>
python -m pytest tests/api/

## Run with Coverage

bash

python -m coverage report -m<br>
python -m coverage html<br>
Open htmlcov/index.html for the full report.<br>


```text

| Test Type         | Test File                            | Total Cases |
| ----------------- | ------------------------------------ | ----------- |
| Unit Tests        | `tests/unit/test_services.py`        | 25          |
| Integration Tests | `tests/integration/test_api_crud.py` | 6           |
| API Tests         | `tests/api/test_api_endpoints.py`    | 14          |
| **Total**         | –                                    | **45**      |
```


