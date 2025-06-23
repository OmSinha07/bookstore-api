# Book Store API(Keploy API Fellowship task-2 and 3)

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


## Test Coverage

![Test Coverage Screenshot](test_Coverage.png)


For testing refer to tests_command.md



## 📁 Project Structure

```text
bookstore-api/
├── app/                               # Application package
│   ├── __init__.py                    # create_app(), db initialization
│   ├── config.py                      # Config classes for prod/test
│   ├── controllers.py                 # API route definitions
│   ├── models.py                      # SQLAlchemy models
│   ├── services.py                    # Business logic (CRUD, validation)
│   ├── templates/
│   │   └── index.html                 # Main frontend HTML page
│   └── static/                        # Static assets
│       ├── css/
│       │   └── style.css              # Custom styling
│       └── js/
│           └── script.js             # JS logic (fetch, UI actions)
│
├── tests/                             # All testing types
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_services.py          # Unit tests with/without mocks
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_api_crud.py          # API <-> DB integration tests
│   └── api/
│       ├── __init__.py
│       └── test_api_endpoints.py     # Endpoint response & behavior tests
│
├── Book Store API Documentation/      # Markdown docs, OpenAPI, JSONs
│   └── README_API.md (optional)       # Endpoint table, sample payloads
│
├── .env                               # PostgreSQL DATABASE_URL / TEST_DATABASE_URL
├── requirements.txt                   # pip install -r requirements.txt
├── README.md                          # Full project overview + setup
├── run.py                             # Entry script: from app import create_app
├── htmlcov/                           # coverage html output (auto-generated)
└── test_commands.md                   # Test + Coverage CLI commands
```



Contact

This project was built as part of the Keploy API Fellowship – Session 2 assignment.
For questions, collaboration, or issues — feel free to open an issue on GitHub or connect on LinkedIn.



