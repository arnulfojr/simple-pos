# Simple POS

A very simple POS

# API

## Products

- `/api/products/`
  + GET, POST
- `/api/products/<uuid:code>/`
  + PUT, DELETE, GET

## Transactions

- `/api/transactions/`
  + GET, POST
- `/api/transactions/<uuid:code>/`
  + GET, DELETE, PUT
- `/api/transactions/<uuid:code>/deliver/`
  + PUT

