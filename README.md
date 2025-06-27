# Book Store API(Keploy API Fellowship task-2,3 and 4)

A full-stack application built using **Flask** and **PostgreSQL** to perform CRUD operations on a collection of books. This project includes a RESTful backend API and a styled frontend interface for managing books.

---

## API Integrated

This application implements a custom RESTful API for managing books using Flask. It includes full CRUD functionality and is test-covered via unit, integration, and API-level testing.

----

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy  
- **Database**: PostgreSQL  
- **Frontend**: HTML, CSS, Vanilla JavaScript  
- **ORM**: SQLAlchemy  
-**Testing Tools**: pytest,pytest-mock,coverage.py
---

## Features

- Add new books  
- View all books  
- Retrieve a book by its ID  
- Update book details (including changing the book ID)  
- Delete a book  
- Search a book by ID using the frontend  
- Fully responsive and styled frontend interface  

---

## Getting Started (Local Setup)

### 1. Clone the Repository
git clone https://github.com/OmSinha07/bookstore-api.git <br>
cd bookstore-api


### 2. Install Python Dependencies
Make sure Python and pip are installed on your system. Then run:

bash<br>
pip install -r requirements.txt

### 3. Configure PostgreSQL
Create a PostgreSQL database named Books (or any name you prefer).

.env file is present in the project root and add your DB connection string:

```DATABASE_URL=postgresql://<username>:<password>@localhost:5432/Books```

Example:-
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/Books

sample is provided in .env file

### 4. Run the Application
bash<br>
python run.py
The server will run at:
http://127.0.0.1:5000


### 5. Launch the Frontend
This will open index.html in your browser following that Link.

API Endpoints
```text
Action	Method	URL	Request Body
Get all books	GET	/books	—
Get book by ID	GET	/books/<id>	—
Add new book	POST	/books	title, author, price
Update book by ID	PUT	/books/<id>	title, author, price, id (optional)
Delete book by ID	DELETE	/books/<id>	—
```

Sample JSON for Testing (POST / PUT)

```text
json
{
  "id": 10,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "price": 599.00
}
```

You can test the API using:
Postman or
curl

Also you can follow bookstore api documentation for any api related issue.

The built-in frontend (index.html)


# 🧪 Tests for Bookstore API

This folder contains all the tests for the API application, divided into:

- `unit/`: Unit tests (with and without mocking)
- `integration/`: Integration tests for CRUD operations
- `api/`: Endpoint behavior tests simulating actual client requests

##  Tools Used

- pytest
- coverage
- unittest.mock (via pytest-mock)

## Testing Commands

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





## Test Coverage

![Test Coverage Screenshot](testreport/test_Coverage.png)


##  Keploy AI Test Report

Here is a screenshot from the Keploy dashboard showing successful API test cases:

### test-summary

![Keploy Test Report](testreport/test-summary.png)


### test-details

![Keploy Test Report](testreport/test-details.png)




## 📁 Project Structure

```text
bookstore-api/
├── app/                               # ✅ Core app logic
│   ├── __init__.py                    # Flask app factory
│   ├── config.py                      # Environment config
│   ├── controllers.py                 # API route definitions
│   ├── models.py                      # SQLAlchemy models
│   ├── services.py                    # Business logic layer
│   ├── templates/
│   │   └── index.html                 # HTML frontend
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── script.js
│
├── tests/                             # ✅ Organized testing
│   ├── __init__.py
│   ├── unit/
│   │   └── test_services.py
│   ├── integration/
│   │   └── test_api_crud.py
│   └── api/
│       └── test_api_endpoints.py
│
├── curl_commands/                     # ✅ For Keploy replay
│   └── curl_*.sh or txt               # Curl API calls
│
├── testreport/            # ✅ Place for screenshots
│   └── test-summary.png
│   └── test-details.png
│   └── test_Coverage.png       
├── .github/workflows/
│   └── ci.yml                         # ✅ GitHub Actions config
│
├── keploy.yml                         # ✅ Keploy config
├── openapi.yaml                       # ✅ OpenAPI schema
├── .env                               # DB configs
├── .coverage                          # Code coverage file
├── requirements.txt                   # pip install -r requirements.txt
├── run.py                             # Flask app entrypoint
├── README.md                          # ✅ Final summary
├── Book Store API Documentation.pdf   # Optional doc PDF



```



Contact

This project was built as part of the Keploy API Fellowship – Session 2 assignment.
For questions, collaboration, or issues — feel free to open an issue on GitHub or connect on LinkedIn.



