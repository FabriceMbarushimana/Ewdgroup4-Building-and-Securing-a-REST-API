# Building and Securing a REST API

A REST API for managing SMS mobile money transactions with Basic Authentication.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/FabriceMbarushimana/Ewdgroup4-Building-and-Securing-a-REST-API.git

# Navigate to the project directory
cd Ewdgroup4-Building-and-Securing-a-REST-API

# Start the server
python api/server.py
```

## Project Structure

```
.
├── api/
│   ├── server.py           # Main HTTP server
│   ├── auth.py             # Authentication module
│   ├── routes_get.py       # GET endpoint handlers
│   └── routes_write.py     # POST/PUT/DELETE handlers
│
├── dsa/
│   ├── xml_parser.py       # XML to JSON parser
│   ├── search_linear.py    # Linear search implementation
│   └── search_dict.py      # Dictionary lookup implementation
│
├── docs/
│   └── api_docs.md         # API documentation
│
├── tests/
│   └── curl_tests.sh       # Bash test script (works on Linux/Mac/Git Bash)
│
├── modified_sms_v2.xml     # Source data
└── README.md               # This file
```

## Features

- Full CRUD operations (Create, Read, Update, Delete)
- Basic Authentication security
- XML data parsing
- Linear search and dictionary lookup comparison
- Comprehensive API documentation
- Test scripts included

## Requirements

- Python 3.x (no additional packages required)
- Git (for cloning the repository)

## Installation

### Clone the Repository

```bash
git clone https://github.com/FabriceMbarushimana/Ewdgroup4-Building-and-Securing-a-REST-API.git
cd Ewdgroup4-Building-and-Securing-a-REST-API
```

### Verify Python Installation

```bash
python --version   # Should be Python 3.x
```

> **Note:** No dependencies to install - uses only Python standard library.

## Running the Server

### On Linux/Mac

```bash
cd Ewdgroup4-Building-and-Securing-a-REST-API
python3 api/server.py
```

Or make the server script executable:

```bash
chmod +x api/server.py
python3 api/server.py
```

### On Windows (Command Prompt)

```cmd
cd Ewdgroup4-Building-and-Securing-a-REST-API
python api\server.py
```

### On Windows (PowerShell)

```powershell
cd Ewdgroup4-Building-and-Securing-a-REST-API
python api\server.py
```

The server will start on `http://localhost:8000`

You should see:

```
Loaded 20 transactions from XML
==================================================
Transaction API Server
==================================================
Server running at http://localhost:8000/
Available endpoints:
  GET    /transactions
  GET    /transactions/{id}
  POST   /transactions
  PUT    /transactions/{id}
  DELETE /transactions/{id}

Authentication required:
  Username: admin, Password: password123
  Username: user, Password: user123
  Username: test, Password: test123
==================================================
```

## Testing the API

### Using curl (Linux/Mac/Git Bash)

Run the test script:

```bash
bash tests/curl_tests.sh
```

Or test individual endpoints:

```bash
# Get all transactions
curl -X GET http://localhost:8000/transactions -u admin:password123

# Get single transaction
curl -X GET http://localhost:8000/transactions/5 -u admin:password123

# Create transaction
curl -X POST http://localhost:8000/transactions \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"type":"payment","amount":"1000","sender":"Alice","receiver":"Bob"}'

# Update transaction
curl -X PUT http://localhost:8000/transactions/5 \
  -u admin:password123 \
  -H "Content-Type: application/json" \
  -d '{"amount":"2000"}'

# Delete transaction
curl -X DELETE http://localhost:8000/transactions/5 -u admin:password123
```

> **Windows Users:** Use Git Bash or WSL to run the curl commands above.

### Using Postman

1. Open Postman
2. Create a new request
3. Set authorization:
   - Type: Basic Auth
   - Username: `admin`
   - Password: `password123`
4. Test endpoints:
   - GET: `http://localhost:8000/transactions`
   - GET: `http://localhost:8000/transactions/5`
   - POST: `http://localhost:8000/transactions` (with JSON body)
   - PUT: `http://localhost:8000/transactions/5` (with JSON body)
   - DELETE: `http://localhost:8000/transactions/5`

## API Endpoints

See full documentation in [docs/api_docs.md](docs/api_docs.md)

### Quick Reference

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /transactions | Get all transactions | Yes |
| GET | /transactions/{id} | Get single transaction | Yes |
| POST | /transactions | Create new transaction | Yes |
| PUT | /transactions/{id} | Update transaction | Yes |
| DELETE | /transactions/{id} | Delete transaction | Yes |

### API Response Summary

**Successful Response Format:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Transaction Object Fields:**
| Field | Description |
|-------|-------------|
| id | Unique transaction ID |
| type | received, payment, transfer, deposit |
| amount | Transaction amount in RWF |
| sender | Sender name |
| receiver | Receiver name |
| balance | Account balance after transaction |
| fee | Transaction fee |
| date | Transaction date/time |

## Authentication

All endpoints require Basic Authentication.

**Valid credentials:**
- `admin:password123`
- `user:user123`
- `test:test123`

## Testing DSA Performance

Test the search algorithms:

```bash
# Test linear search
python dsa/search_linear.py

# Test dictionary lookup
python dsa/search_dict.py
```

Compare performance:

```python
from dsa.xml_parser import parse_xml_to_json
from dsa.search_dict import compare_search_methods

transactions = parse_xml_to_json('modified_sms_v2.xml')
test_ids = list(range(1, 21))
results = compare_search_methods(transactions, test_ids)

print(f"Linear Search: {results['linear_search']['average_time']:.8f}s")
print(f"Dict Lookup: {results['dict_lookup']['average_time']:.8f}s")
print(f"Speedup: {results['speedup']:.2f}x")
```

## Troubleshooting

**Server won't start:**
- Check if port 8000 is already in use: `lsof -i :8000` (Linux/Mac) or `netstat -ano | findstr :8000` (Windows)
- Try a different port by editing `server.py`

**401 Unauthorized errors:**
- Verify credentials are correct
- Check Authorization header format

**Module import errors:**
- Make sure you're running from project root directory
- Check Python path includes project directory

**XML parsing errors:**
- Verify `modified_sms_v2.xml` is in project root
- Check file encoding is UTF-8
