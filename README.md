# Book Store API

A full-stack application built using **Flask** and **PostgreSQL** to perform CRUD operations on a collection of books. This project includes a RESTful backend API and a styled frontend interface for managing books.

---

## Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy  
- **Database**: PostgreSQL  
- **Frontend**: HTML, CSS, Vanilla JavaScript  
- **ORM**: SQLAlchemy  

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

 1. Clone the Repository

```bash```
git clone https://github.com/OmSinha07/bookstore-api.git
cd bookstore-api

2. Install Python Dependencies
Make sure Python and pip are installed on your system. Then run:

bash
pip install -r requirements.txt

3. Configure PostgreSQL
Create a PostgreSQL database named Books (or any name you prefer).

Create a .env file in the project root and add your DB connection string:

DATABASE_URL=postgresql://<username>:<password>@localhost:5432/Books

Example:-
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/Books


4. Run the Application
bash
python app.py
The server will run at:
http://127.0.0.1:5000


5. Launch the Frontend
Open frontend.html in your browser to access the user interface.

API Endpoints
Action	Method	URL	Request Body
Get all books	GET	/books	—
Get book by ID	GET	/books/<id>	—
Add new book	POST	/books	title, author, price
Update book by ID	PUT	/books/<id>	title, author, price, id (optional)
Delete book by ID	DELETE	/books/<id>	—

Sample JSON for Testing (POST / PUT)
json
{
  "id": 10,
  "title": "Clean Code",
  "author": "Robert C. Martin",
  "price": 599.00
}
You can test the API using:
Postman
curl

The built-in frontend (index.html)

Project Structure
bookstore-api
│
├── app.py                         # Flask backend server
├── templates/
│   └── frontend.html              # Frontend user interface (HTML)
├── requirements.txt               # Python dependencies
├── .env                           # Environment variables (e.g., PostgreSQL credentials)
├── README.md                      # Project documentation
└── Book Store API Documentation/  # API documentation assets (Markdown, examples, diagrams, etc.)


Contact
This project was built as part of the Keploy API Fellowship – Session 2 assignment.
For questions, collaboration, or issues — feel free to open an issue on GitHub or connect on LinkedIn.

