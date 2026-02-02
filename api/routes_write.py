import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.search_dict import dict_search

def handle_post_transaction(handler, transactions, transaction_dict):
    """
    POST /transactions
    Add a new transaction
    
    Args:
        handler: HTTP request handler
        transactions: List of all transactions
        transaction_dict: Dictionary of transactions
    """
    try:
        # Read request body
        content_length = int(handler.headers.get('Content-Length', 0))
        body = handler.rfile.read(content_length).decode('utf-8')
        new_transaction = json.loads(body)
        
        # Validate required fields
        required_fields = ['type', 'amount', 'sender', 'receiver']
        missing_fields = [field for field in required_fields if field not in new_transaction]
        
        if missing_fields:
            send_400(handler, f"Missing required fields: {', '.join(missing_fields)}")
            return
        
        # Generate new ID
        new_id = max([t['id'] for t in transactions]) + 1 if transactions else 1
        new_transaction['id'] = new_id
        
        # Add default fields if not provided
        if 'balance' not in new_transaction:
            new_transaction['balance'] = '0'
        if 'fee' not in new_transaction:
            new_transaction['fee'] = '0'
        if 'date' not in new_transaction:
            new_transaction['date'] = ''
        if 'timestamp' not in new_transaction:
            new_transaction['timestamp'] = ''
        if 'body' not in new_transaction:
            new_transaction['body'] = f"{new_transaction['type']} transaction"
        if 'txid' not in new_transaction:
            new_transaction['txid'] = ''
        
        # Add to storage
        transactions.append(new_transaction)
        transaction_dict[new_id] = new_transaction
        
        # Send response
        handler.send_response(201)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        
        response = {
            'success': True,
            'message': 'Transaction created successfully',
            'data': new_transaction
        }
        
        handler.wfile.write(json.dumps(response, indent=2).encode())
    
    except json.JSONDecodeError:
        send_400(handler, "Invalid JSON format")
    except Exception as e:
        send_500(handler, str(e))

def handle_put_transaction(handler, transaction_id, transactions, transaction_dict):
    """
    PUT /transactions/{id}
    Update an existing transaction
    
    Args:
        handler: HTTP request handler
        transaction_id: ID of transaction to update
        transactions: List of all transactions
        transaction_dict: Dictionary of transactions
    """
    try:
        tid = int(transaction_id)
        
        # Check if transaction exists
        existing = dict_search(transaction_dict, tid)
        if not existing:
            send_404(handler, f"Transaction with ID {tid} not found")
            return
        
        # Read request body
        content_length = int(handler.headers.get('Content-Length', 0))
        body = handler.rfile.read(content_length).decode('utf-8')
        update_data = json.loads(body)
        
        # Update transaction (keep the same ID)
        update_data['id'] = tid
        
        # Find and update in list
        for i, t in enumerate(transactions):
            if t['id'] == tid:
                transactions[i].update(update_data)
                break
        
        # Update in dictionary
        transaction_dict[tid].update(update_data)
        
        # Send response
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        
        response = {
            'success': True,
            'message': 'Transaction updated successfully',
            'data': transaction_dict[tid]
        }
        
        handler.wfile.write(json.dumps(response, indent=2).encode())
    
    except ValueError:
        send_400(handler, "Invalid transaction ID format")
    except json.JSONDecodeError:
        send_400(handler, "Invalid JSON format")
    except Exception as e:
        send_500(handler, str(e))

def handle_delete_transaction(handler, transaction_id, transactions, transaction_dict):
    """
    DELETE /transactions/{id}
    Delete a transaction
    
    Args:
        handler: HTTP request handler
        transaction_id: ID of transaction to delete
        transactions: List of all transactions
        transaction_dict: Dictionary of transactions
    """
    try:
        tid = int(transaction_id)
        
        # Check if transaction exists
        existing = dict_search(transaction_dict, tid)
        if not existing:
            send_404(handler, f"Transaction with ID {tid} not found")
            return
        
        # Remove from list
        transactions[:] = [t for t in transactions if t['id'] != tid]
        
        # Remove from dictionary
        del transaction_dict[tid]
        
        # Send response
        handler.send_response(200)
        handler.send_header('Content-Type', 'application/json')
        handler.end_headers()
        
        response = {
            'success': True,
            'message': f'Transaction {tid} deleted successfully'
        }
        
        handler.wfile.write(json.dumps(response, indent=2).encode())
    
    except ValueError:
        send_400(handler, "Invalid transaction ID format")
    except Exception as e:
        send_500(handler, str(e))

def send_400(handler, message):
    """Send 400 Bad Request response"""
    handler.send_response(400)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    
    response = {
        'success': False,
        'error': message
    }
    
    handler.wfile.write(json.dumps(response, indent=2).encode())

def send_404(handler, message):
    """Send 404 Not Found response"""
    handler.send_response(404)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    
    response = {
        'success': False,
        'error': message
    }
    
    handler.wfile.write(json.dumps(response, indent=2).encode())

def send_500(handler, message):
    """Send 500 Internal Server Error response"""
    handler.send_response(500)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    
    response = {
        'success': False,
        'error': f'Internal server error: {message}'
    }
    
    handler.wfile.write(json.dumps(response, indent=2).encode())
