#!/usr/bin/env python3
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.search_dict import dict_search

def handle_get_all_transactions(handler, transactions):
    """
    GET /transactions
    Return all transactions
    
    Args:
        handler: HTTP request handler
        transactions: List of all transactions
    """
    handler.send_response(200)
    handler.send_header('Content-Type', 'application/json')
    handler.end_headers()
    
    response = {
        'success': True,
        'count': len(transactions),
        'data': transactions
    }
    
    handler.wfile.write(json.dumps(response, indent=2).encode())

def handle_get_transaction_by_id(handler, transaction_id, transaction_dict):
    """
    GET /transactions/{id}
    Return single transaction by ID
    
    Args:
        handler: HTTP request handler
        transaction_id: ID to search for
        transaction_dict: Dictionary of transactions
    """
    try:
        tid = int(transaction_id)
        transaction = dict_search(transaction_dict, tid)
        
        if transaction:
            handler.send_response(200)
            handler.send_header('Content-Type', 'application/json')
            handler.end_headers()
            
            response = {
                'success': True,
                'data': transaction
            }
            
            handler.wfile.write(json.dumps(response, indent=2).encode())
        else:
            send_404(handler, f"Transaction with ID {tid} not found")
    
    except ValueError:
        send_400(handler, "Invalid transaction ID format")

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
