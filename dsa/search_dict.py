import time

def create_transaction_dict(transactions):
    """
    Create dictionary with transaction ID as key
    
    Args:
        transactions: List of transaction dictionaries
    
    Returns:
        Dictionary {id: transaction}
    """
    return {transaction['id']: transaction for transaction in transactions}

def dict_search(transaction_dict, transaction_id):
    """
    Dictionary lookup implementation
    Direct key lookup in dictionary
    
    Args:
        transaction_dict: Dictionary {id: transaction}
        transaction_id: ID to search for
    
    Returns:
        Transaction dict if found, None otherwise
    """
    return transaction_dict.get(transaction_id)

def dict_search_timed(transaction_dict, transaction_id):
    """
    Dictionary search with timing
    Returns: (result, time_taken_in_seconds)
    """
    start_time = time.time()
    result = dict_search(transaction_dict, transaction_id)
    end_time = time.time()
    
    time_taken = end_time - start_time
    return result, time_taken

def benchmark_dict_search(transaction_dict, test_ids):
    """
    Benchmark dictionary search performance
    
    Args:
        transaction_dict: Dictionary {id: transaction}
        test_ids: List of IDs to search for
    
    Returns:
        Dictionary with benchmark results
    """
    total_time = 0
    results = []
    
    for test_id in test_ids:
        result, time_taken = dict_search_timed(transaction_dict, test_id)
        total_time += time_taken
        results.append({
            'id': test_id,
            'found': result is not None,
            'time': time_taken
        })
    
    avg_time = total_time / len(test_ids) if test_ids else 0
    
    return {
        'method': 'Dictionary Lookup',
        'total_searches': len(test_ids),
        'total_time': total_time,
        'average_time': avg_time,
        'results': results
    }

def compare_search_methods(transactions, test_ids):
    """
    Compare linear search vs dictionary lookup
    
    Returns:
        Comparison results
    """
    from search_linear import benchmark_linear_search
    
    # Create dictionary
    transaction_dict = create_transaction_dict(transactions)
    
    # Benchmark both methods
    linear_results = benchmark_linear_search(transactions, test_ids)
    dict_results = benchmark_dict_search(transaction_dict, test_ids)
    
    # Calculate speedup
    speedup = linear_results['average_time'] / dict_results['average_time'] if dict_results['average_time'] > 0 else float('inf')
    
    return {
        'linear_search': linear_results,
        'dict_lookup': dict_results,
        'speedup': speedup,
        'winner': 'Dictionary Lookup' if dict_results['average_time'] < linear_results['average_time'] else 'Linear Search'
    }

# Example usage
if __name__ == '__main__':
    from xml_parser import parse_xml_to_json
    
    # Load transactions
    transactions = parse_xml_to_json('../modified_sms_v2.xml')
    transaction_dict = create_transaction_dict(transactions)
    
    # Test search
    test_id = 5
    result, time_taken = dict_search_timed(transaction_dict, test_id)
    
    if result:
        print(f"Found transaction {test_id}")
        print(f"Time taken: {time_taken:.8f} seconds")
    else:
        print(f"Transaction {test_id} not found")
    
    # Compare methods
    test_ids = list(range(1, 21))  # Test first 20 IDs
    comparison = compare_search_methods(transactions, test_ids)
    
    print(f"\nComparison Results:")
    print(f"Linear Search - Average: {comparison['linear_search']['average_time']:.8f} seconds")
    print(f"Dict Lookup - Average: {comparison['dict_lookup']['average_time']:.8f} seconds")
    print(f"Speedup: {comparison['speedup']:.2f}x faster")
    print(f"Winner: {comparison['winner']}")
