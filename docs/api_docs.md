# Transaction API Documentation

## Overview
REST API for managing SMS mobile money transactions. Built with Python's `http.server` module and secured with Basic Authentication.

## Base URL
```
http://localhost:8000
```

## Authentication
All endpoints require Basic Authentication.

**Valid Credentials:**
- Username: `admin`, Password: `password123`
- Username: `user`, Password: `user123`
- Username: `test`, Password: `test123`

**Header Format:**
```
Authorization: Basic <base64_encoded_credentials>
```

**Example:**
```bash
# For admin:password123
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

## Endpoints

### 1. GET /transactions
Retrieve all transactions.

**Request:**
```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 20,
  "data": [
    {
      "id": 1,
      "date": "10 May 2024 4:30:58 PM",
      "timestamp": "1715351458724",
      "body": "You have received 2000 RWF...",
      "type": "received",
      "amount": "2000",
      "sender": "Jane Smith",
      "receiver": "You",
      "balance": "2000",
      "fee": "0",
      "txid": "76662021700"
    }
  ]
}
```

---

### 2. GET /transactions/{id}
Retrieve a single transaction by ID.

**Request:**
```bash
curl -X GET http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "date": "10 May 2024 4:30:58 PM",
    "type": "received",
    "amount": "2000",
    "sender": "Jane Smith",
    "receiver": "You",
    "balance": "2000",
    "fee": "0"
  }
}
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Transaction with ID 999 not found"
}
```

---

### 3. POST /transactions
Create a new transaction.

**Request:**
```bash
curl -X POST http://localhost:8000/transactions \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "payment",
    "amount": "5000",
    "sender": "John Doe",
    "receiver": "Jane Smith"
  }'
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Transaction created successfully",
  "data": {
    "id": 21,
    "type": "payment",
    "amount": "5000",
    "sender": "John Doe",
    "receiver": "Jane Smith",
    "balance": "0",
    "fee": "0",
    "date": "",
    "timestamp": "",
    "body": "payment transaction",
    "txid": ""
  }
}
```

**Response (400 Bad Request):**
```json
{
  "success": false,
  "error": "Missing required fields: type, amount"
}
```

**Required Fields:**
- `type` (string): Transaction type (received, payment, transfer, deposit)
- `amount` (string): Transaction amount
- `sender` (string): Sender name
- `receiver` (string): Receiver name

---

### 4. PUT /transactions/{id}
Update an existing transaction.

**Request:**
```bash
curl -X PUT http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "3000",
    "fee": "50"
  }'
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction updated successfully",
  "data": {
    "id": 1,
    "type": "received",
    "amount": "3000",
    "sender": "Jane Smith",
    "receiver": "You",
    "balance": "2000",
    "fee": "50"
  }
}
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Transaction with ID 999 not found"
}
```

---

### 5. DELETE /transactions/{id}
Delete a transaction.

**Request:**
```bash
curl -X DELETE http://localhost:8000/transactions/1 \
  -H "Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM="
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Transaction 1 deleted successfully"
}
```

**Response (404 Not Found):**
```json
{
  "success": false,
  "error": "Transaction with ID 999 not found"
}
```

---

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request format or missing fields |
| 401 | Unauthorized | Invalid or missing credentials |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## Authentication Errors

**Missing Authorization Header:**
```bash
curl -X GET http://localhost:8000/transactions
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Unauthorized - Valid credentials required"
}
```

**Invalid Credentials:**
```bash
curl -X GET http://localhost:8000/transactions \
  -H "Authorization: Basic d3Jvbmc6Y3JlZGVudGlhbHM="
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Unauthorized - Valid credentials required"
}
```

---

## Testing with Curl

**Get all transactions:**
```bash
curl -X GET http://localhost:8000/transactions -u admin:password123
```

**Get single transaction:**
```bash
curl -X GET http://localhost:8000/transactions/5 -u admin:password123
```

**Create transaction:**
```bash
curl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"type":"payment","amount":"1000","sender":"Alice","receiver":"Bob"}'
```

**Update transaction:**
```bash
curl -X PUT http://localhost:8000/transactions/5 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"amount":"2000"}'
```

**Delete transaction:**
```bash
curl -X DELETE http://localhost:8000/transactions/5 -u admin:password123
```

---


---

## Data Structure

**Transaction Object:**
```json
{
  "id": 1,
  "date": "10 May 2024 4:30:58 PM",
  "timestamp": "1715351458724",
  "body": "Full SMS message text",
  "type": "received|payment|transfer|deposit",
  "amount": "2000",
  "sender": "Sender name",
  "receiver": "Receiver name",
  "balance": "2000",
  "fee": "0",
  "txid": "Transaction ID from SMS"
}
```
