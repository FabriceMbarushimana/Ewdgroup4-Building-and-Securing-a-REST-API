import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

def parse_xml_to_json(xml_file):
    """
    Parse modified_sms_v2.xml and convert to JSON format
    Returns: List of transaction dictionaries
    """
    # Read and fix XML if needed
    with open(xml_file, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    # Fix malformed closing tag if present
    xml_content = xml_content.replace('</smses/>', '</smses>')
    
    # Parse XML from string
    root = ET.fromstring(xml_content)
    
    transactions = []
    
    for idx, sms in enumerate(root.findall('sms'), start=1):
        body = sms.get('body', '')
        
        # Extract transaction details from the body
        transaction = {
            'id': idx,
            'date': sms.get('readable_date', ''),
            'timestamp': sms.get('date', ''),
            'body': body,
            'type': determine_transaction_type(body),
            'amount': extract_amount(body),
            'sender': extract_sender(body),
            'receiver': extract_receiver(body),
            'balance': extract_balance(body),
            'fee': extract_fee(body),
            'txid': extract_txid(body)
        }
        
        transactions.append(transaction)
    
    return transactions

def determine_transaction_type(body):
    """Determine transaction type from message body"""
    body_lower = body.lower()
    
    if 'received' in body_lower:
        return 'received'
    elif 'payment' in body_lower:
        return 'payment'
    elif 'transferred' in body_lower:
        return 'transfer'
    elif 'deposit' in body_lower:
        return 'deposit'
    else:
        return 'other'

def extract_amount(body):
    """Extract amount from transaction body"""
    match = re.search(r'(\d+,?\d*)\s*RWF', body)
    if match:
        return match.group(1).replace(',', '')
    return '0'

def extract_sender(body):
    """Extract sender from transaction body"""
    if 'from' in body.lower():
        match = re.search(r'from\s+([A-Za-z\s]+)\s*\(', body, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r'from\s+(\d+)', body, re.IGNORECASE)
        if match:
            return match.group(1)
    return 'Unknown'

def extract_receiver(body):
    """Extract receiver from transaction body"""
    if 'to' in body.lower():
        match = re.search(r'to\s+([A-Za-z\s]+)\s*\(', body, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        match = re.search(r'to\s+([A-Za-z\s]+)\s+\d', body, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    elif 'received' in body.lower():
        match = re.search(r'from\s+([A-Za-z\s]+)\s*\(', body, re.IGNORECASE)
        if match:
            return 'You'
    return 'Unknown'

def extract_balance(body):
    """Extract new balance from transaction body"""
    match = re.search(r'balance[:\s]+(\d+,?\d*)\s*RWF', body, re.IGNORECASE)
    if match:
        return match.group(1).replace(',', '')
    return '0'

def extract_fee(body):
    """Extract fee from transaction body"""
    match = re.search(r'fee\s+was[:\s]+(\d+,?\d*)\s*RWF', body, re.IGNORECASE)
    if match:
        return match.group(1).replace(',', '')
    return '0'

def extract_txid(body):
    """Extract transaction ID from body"""
    match = re.search(r'TxId[:\s]+(\d+)', body, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r'Transaction Id[:\s]+(\d+)', body, re.IGNORECASE)
    if match:
        return match.group(1)
    return ''

def save_json(transactions, output_file='transactions.json'):
    """Save transactions to JSON file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2, ensure_ascii=False)
    return output_file

# Example usage
if __name__ == '__main__':
    xml_file = '../modified_sms_v2.xml'
    transactions = parse_xml_to_json(xml_file)
    
    print(f"Parsed {len(transactions)} transactions")
    print("\nSample transaction:")
    print(json.dumps(transactions[0], indent=2))
    
    # Save to file
    output = save_json(transactions)
    print(f"\nSaved to {output}")
