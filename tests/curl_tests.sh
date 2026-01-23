#!/bin/bash

URL="http://localhost:8000/transactions"

# POST
curl -X POST $URL \
-H "Content-Type: application/json" \
-d '{
"type":"Cash In",
"amount":5000,
"sender":"Alice",
"receiver":"Bob",
"timestamp":"2026-01-23 12:00:00"
}'

echo -e "\n"

# PUT
curl -X PUT $URL/1 \
-H "Content-Type: application/json" \
-d '{"amount":8000}'

echo -e "\n"
