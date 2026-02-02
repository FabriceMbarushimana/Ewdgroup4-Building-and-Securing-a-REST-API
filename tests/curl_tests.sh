#!/bin/bash

# Transaction API Test Script
# Tests all endpoints with valid and invalid credentials

BASE_URL="http://localhost:8000"
VALID_AUTH="admin:password123"
INVALID_AUTH="wrong:credentials"

echo "=================================================="
echo "Transaction API - Test Suite"
echo "=================================================="
echo ""

# Test 1: GET all transactions with valid auth
echo "Test 1: GET /transactions (Valid Auth)"
echo "--------------------------------------"
curl -s -X GET "$BASE_URL/transactions" -u "$VALID_AUTH" | python -m json.tool
echo ""
echo ""

# Test 2: GET all transactions without auth (should fail)
echo "Test 2: GET /transactions (No Auth - Should Fail)"
echo "------------------------------------------------"
curl -s -X GET "$BASE_URL/transactions"
echo ""
echo ""

# Test 3: GET all transactions with invalid auth (should fail)
echo "Test 3: GET /transactions (Invalid Auth - Should Fail)"
echo "-----------------------------------------------------"
curl -s -X GET "$BASE_URL/transactions" -u "$INVALID_AUTH"
echo ""
echo ""

# Test 4: GET single transaction by ID
echo "Test 4: GET /transactions/5 (Valid Auth)"
echo "---------------------------------------"
curl -s -X GET "$BASE_URL/transactions/5" -u "$VALID_AUTH" | python -m json.tool
echo ""
echo ""

# Test 5: GET non-existent transaction
echo "Test 5: GET /transactions/999 (Not Found)"
echo "----------------------------------------"
curl -s -X GET "$BASE_URL/transactions/999" -u "$VALID_AUTH" | python -m json.tool
echo ""
echo ""

# Test 6: POST new transaction
echo "Test 6: POST /transactions (Create New)"
echo "--------------------------------------"
curl -s -X POST "$BASE_URL/transactions" \
  -u "$VALID_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "payment",
    "amount": "5000",
    "sender": "Test User",
    "receiver": "Another User"
  }' | python -m json.tool
echo ""
echo ""

# Test 7: POST with missing fields (should fail)
echo "Test 7: POST /transactions (Missing Fields - Should Fail)"
echo "--------------------------------------------------------"
curl -s -X POST "$BASE_URL/transactions" \
  -u "$VALID_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "payment"
  }' | python -m json.tool
echo ""
echo ""

# Test 8: PUT update transaction
echo "Test 8: PUT /transactions/5 (Update)"
echo "-----------------------------------"
curl -s -X PUT "$BASE_URL/transactions/5" \
  -u "$VALID_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "10000",
    "fee": "100"
  }' | python -m json.tool
echo ""
echo ""

# Test 9: PUT non-existent transaction (should fail)
echo "Test 9: PUT /transactions/999 (Not Found)"
echo "----------------------------------------"
curl -s -X PUT "$BASE_URL/transactions/999" \
  -u "$VALID_AUTH" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "5000"
  }' | python -m json.tool
echo ""
echo ""

# Test 10: DELETE transaction
echo "Test 10: DELETE /transactions/10"
echo "--------------------------------"
curl -s -X DELETE "$BASE_URL/transactions/10" -u "$VALID_AUTH" | python -m json.tool
echo ""
echo ""

# Test 11: DELETE non-existent transaction (should fail)
echo "Test 11: DELETE /transactions/999 (Not Found)"
echo "--------------------------------------------"
curl -s -X DELETE "$BASE_URL/transactions/999" -u "$VALID_AUTH" | python -m json.tool
echo ""
echo ""

# Test 12: Verify GET after modifications
echo "Test 12: GET /transactions (Verify Changes)"
echo "------------------------------------------"
curl -s -X GET "$BASE_URL/transactions" -u "$VALID_AUTH" | python -m json.tool | head -30
echo ""

echo "=================================================="
echo "Test Suite Completed"
echo "=================================================="