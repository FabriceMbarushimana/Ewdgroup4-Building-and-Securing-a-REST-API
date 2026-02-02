from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dsa.xml_parser import parse_xml_to_json
from dsa.search_dict import create_transaction_dict
from api.auth import authenticate, get_auth_response_headers
from api.routes_get import handle_get_all_transactions, handle_get_transaction_by_id
from api.routes_write import handle_post_transaction, handle_put_transaction, handle_delete_transaction

# Load transactions at startup
XML_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'modified_sms_v2.xml')
transactions = parse_xml_to_json(XML_FILE)
transaction_dict = create_transaction_dict(transactions)

print(f"Loaded {len(transactions)} transactions from XML")

class TransactionAPIHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for Transaction API"""
    
    def do_GET(self):
        """Handle GET requests"""
        # Check authentication
        if not self.check_auth():
            return
        
        # Route requests
        if self.path == '/transactions':
            handle_get_all_transactions(self, transactions)
        elif self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            handle_get_transaction_by_id(self, transaction_id, transaction_dict)
        else:
            self.send_404()
    
    def do_POST(self):
        """Handle POST requests"""
        # Check authentication
        if not self.check_auth():
            return
        
        # Route requests
        if self.path == '/transactions':
            handle_post_transaction(self, transactions, transaction_dict)
        else:
            self.send_404()
    
    def do_PUT(self):
        """Handle PUT requests"""
        # Check authentication
        if not self.check_auth():
            return
        
        # Route requests
        if self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            handle_put_transaction(self, transaction_id, transactions, transaction_dict)
        else:
            self.send_404()
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        # Check authentication
        if not self.check_auth():
            return
        
        # Route requests
        if self.path.startswith('/transactions/'):
            transaction_id = self.path.split('/')[-1]
            handle_delete_transaction(self, transaction_id, transactions, transaction_dict)
        else:
            self.send_404()
    
    def check_auth(self):
        """
        Check authentication for request
        Returns True if authenticated, False otherwise
        """
        auth_header = self.headers.get('Authorization')
        
        if not authenticate(auth_header):
            self.send_401()
            return False
        
        return True
    
    def send_401(self):
        """Send 401 Unauthorized response"""
        self.send_response(401)
        headers = get_auth_response_headers()
        for key, value in headers.items():
            self.send_header(key, value)
        self.end_headers()
        
        response = {
            'success': False,
            'error': 'Unauthorized - Valid credentials required'
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def send_404(self):
        """Send 404 Not Found response"""
        self.send_response(404)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        response = {
            'success': False,
            'error': 'Endpoint not found'
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def log_message(self, format, *args):
        """Custom log message format"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server(host='localhost', port=8000):
    """
    Start the HTTP server
    
    Args:
        host: Server host
        port: Server port
    """
    server_address = (host, port)
    httpd = HTTPServer(server_address, TransactionAPIHandler)
    
    print(f"\n{'='*50}")
    print(f"Transaction API Server")
    print(f"{'='*50}")
    print(f"Server running at http://{host}:{port}/")
    print(f"Available endpoints:")
    print(f"  GET    /transactions")
    print(f"  GET    /transactions/{{id}}")
    print(f"  POST   /transactions")
    print(f"  PUT    /transactions/{{id}}")
    print(f"  DELETE /transactions/{{id}}")
    print(f"\nAuthentication required:")
    print(f"  Username: admin, Password: password123")
    print(f"  Username: user, Password: user123")
    print(f"  Username: test, Password: test123")
    print(f"{'='*50}\n")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
        httpd.shutdown()
        print("Server stopped.")

if __name__ == '__main__':
    run_server()
