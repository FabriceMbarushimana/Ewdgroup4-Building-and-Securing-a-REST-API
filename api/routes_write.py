import json
def read_json(handler):
    length = int(handler.headers.get("Content-Length", 0))
    body = handler.rfile.read(length)
    return json.loads(body.decode("utf-8"))

# POST /transactions
def handle_post(handler, transactions):
    if handler.path != "/transactions":
        handler.send_response(404)
        handler.end_headers()
        return

    try:
        data = read_json(handler)

        required = ["type", "amount", "sender", "receiver", "timestamp"]
        for field in required:
            if field not in data:
                handler.send_response(400)
                handler.end_headers()
                handler.wfile.write(b"Missing required fields")
                return

        # Assign new ID
        new_id = max([t["id"] for t in transactions], default=0) + 1
        data["id"] = new_id

        # Add transaction
        transactions.append(data)

        # Return created transaction
        handler.send_response(201)  
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode())

    except Exception as e:
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(f"Error: {str(e)}".encode())

# PUT
def handle_put(handler, transactions):
    if not handler.path.startswith("/transactions/"):
        handler.send_response(404)
        handler.end_headers()
        return

    try:
        transaction_id = int(handler.path.split("/")[-1])
        data = read_json(handler)

        for t in transactions:
            if t["id"] == transaction_id:
                t.update(data)

                handler.send_response(200)  
                handler.send_header("Content-Type", "application/json")
                handler.end_headers()
                handler.wfile.write(json.dumps(t).encode())
                return

        handler.send_response(404)
        handler.end_headers()
        handler.wfile.write(b"Transaction not found")

    except Exception as e:
        handler.send_response(400)
        handler.end_headers()
        handler.wfile.write(f"Error: {str(e)}".encode())

