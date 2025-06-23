const bookList = document.getElementById("bookList");
const form = document.getElementById("bookForm");
const bookIdInput = document.getElementById("bookId");
const titleInput = document.getElementById("title");
const authorInput = document.getElementById("author");
const priceInput = document.getElementById("price");
const submitBtn = document.getElementById("submitBtn");

const searchForm = document.getElementById("searchForm");
const searchId = document.getElementById("searchId");
const searchResult = document.getElementById("searchResult");

function loadBooks() {
  fetch("/books")
    .then(res => res.json())
    .then(data => {
      bookList.innerHTML = "";
      data.forEach(book => {
        const li = document.createElement("li");
        li.className = "list-group-item shadow-sm";
        li.innerHTML = `
          <div>
            <strong>ID ${book.id}:</strong> ${book.title} by ${book.author} — ₹${book.price}
          </div>
          <div class="btn-group">
            <button class="btn btn-sm btn-primary" onclick="editBook(${book.id})">✏️ Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deleteBook(${book.id})">🗑️ Delete</button>
          </div>
        `;
        bookList.appendChild(li);
      });
    });
}

form.onsubmit = function (e) {
  e.preventDefault();
  const id = bookIdInput.value.trim();
  const bookData = {
    title: titleInput.value,
    author: authorInput.value,
    price: parseFloat(priceInput.value)
  };

  if (id && submitBtn.textContent.includes("Update")) {
    fetch(`/books/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bookData)
    }).then(() => {
      form.reset();
      submitBtn.textContent = "➕ Add Book";
      loadBooks();
    });
  } else {
    if (id) {
      bookData.id = parseInt(id);
    }
    fetch("/books", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(bookData)
    }).then(res => {
      if (!res.ok) {
        alert("Failed to add book. ID might already exist.");
      }
      form.reset();
      submitBtn.textContent = "➕ Add Book";
      loadBooks();
    });
  }
};

function editBook(id) {
  fetch(`/books/${id}`)
    .then(res => res.json())
    .then(book => {
      bookIdInput.value = book.id;
      titleInput.value = book.title;
      authorInput.value = book.author;
      priceInput.value = book.price;
      submitBtn.textContent = "✅ Update Book";
    });
}

function deleteBook(id) {
  fetch(`/books/${id}`, { method: "DELETE" })
    .then(() => loadBooks());
}

searchForm.onsubmit = function(e) {
  e.preventDefault();
  const id = searchId.value;
  fetch(`/books/${id}`)
    .then(res => {
      if (!res.ok) throw new Error("Book not found");
      return res.json();
    })
    .then(book => {
      searchResult.innerHTML = `
        <p><strong>ID:</strong> ${book.id}</p>
        <p><strong>Title:</strong> ${book.title}</p>
        <p><strong>Author:</strong> ${book.author}</p>
        <p><strong>Price:</strong> ₹${book.price}</p>
      `;
    })
    .catch(err => {
      searchResult.innerHTML = `<p class="text-danger">${err.message}</p>`;
    });
};

loadBooks();
