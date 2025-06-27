curl -X 'PUT' \
  'http://127.0.0.1:5000/books/0' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "id": 0,
  "title": "String",
  "author": "string",
  "price": 0
}'