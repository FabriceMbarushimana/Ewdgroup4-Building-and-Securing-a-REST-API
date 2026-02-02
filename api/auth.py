#!/usr/bin/env python3
import base64
# Valid credentials (username:password)
VALID_USERS = {
    'admin': 'password123',
    'user': 'user123',
    'test': 'test123'
}

def parse_auth_header(auth_header):
    """
    Parse Authorization header
    
    Args:
        auth_header: String from Authorization header
    
    Returns:
        Tuple (username, password) or (None, None)
    """
    if not auth_header:
        return None, None
    
    # Remove 'Basic ' prefix
    if not auth_header.startswith('Basic '):
        return None, None
    
    try:
        # Decode Base64
        encoded_credentials = auth_header[6:]  # Remove 'Basic '
        decoded_bytes = base64.b64decode(encoded_credentials)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Split username:password
        if ':' in decoded_str:
            username, password = decoded_str.split(':', 1)
            return username, password
        else:
            return None, None
    except Exception:
        return None, None

def validate_credentials(username, password):
    """
    Validate username and password
    
    Args:
        username: String username
        password: String password
    
    Returns:
        True if valid, False otherwise
    """
    if username in VALID_USERS:
        return VALID_USERS[username] == password
    return False

def authenticate(auth_header):
    """
    Authenticate request using Basic Auth
    
    Args:
        auth_header: Authorization header value
    
    Returns:
        True if authenticated, False otherwise
    """
    username, password = parse_auth_header(auth_header)
    
    if username is None or password is None:
        return False
    
    return validate_credentials(username, password)

def get_auth_response_headers():
    """
    Get headers for 401 Unauthorized response
    
    Returns:
        Dictionary of headers
    """
    return {
        'WWW-Authenticate': 'Basic realm="Transaction API"',
        'Content-Type': 'application/json'
    }

# Example usage
if __name__ == '__main__':
    # Test valid credentials
    auth_header = 'Basic ' + base64.b64encode(b'admin:password123').decode('utf-8')
    print(f"Testing: {auth_header}")
    print(f"Valid: {authenticate(auth_header)}")
    
    # Test invalid credentials
    auth_header = 'Basic ' + base64.b64encode(b'admin:wrongpass').decode('utf-8')
    print(f"\nTesting: {auth_header}")
    print(f"Valid: {authenticate(auth_header)}")
    
    # Test no credentials
    print(f"\nTesting: None")
    print(f"Valid: {authenticate(None)}")
