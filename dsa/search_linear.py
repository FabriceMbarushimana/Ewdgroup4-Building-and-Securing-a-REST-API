import time

def linear_search(transactions, transaction_id):
    """
    Linear search implementation
    Search through list sequentially to find transaction by ID
    
    Args:
        transactions: List of transaction dictionaries
        transaction_id: ID to search for
    
    Returns:
        Transaction dict if found, None otherwise
    """
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return transaction
    return None

def linear_search_timed(transactions, transaction_id):
    """
    Linear search with timing
    Returns: (result, time_taken_in_seconds)
    """
    start_time = time.time()
    result = linear_search(transactions, transaction_id)
    end_time = time.time()
    
    time_taken = end_time - start_time
    return result, time_taken

def benchmark_linear_search(transactions, test_ids):
    """
    Benchmark linear search performance
    
    Args:
        transactions: List of transaction dictionaries
        test_ids: List of IDs to search for
    
    Returns:
        Dictionary with benchmark results
    """
    total_time = 0
    results = []
    
    for test_id in test_ids:
        result, time_taken = linear_search_timed(transactions, test_id)
        total_time += time_taken
        results.append({
            'id': test_id,
            'found': result is not None,
            'time': time_taken
        })
    
    avg_time = total_time / len(test_ids) if test_ids else 0
    
    return {
        'method': 'Linear Search',
        'total_searches': len(test_ids),
        'total_time': total_time,
        'average_time': avg_time,
        'results': results
    }

# Example usage
if __name__ == '__main__':
    from xml_parser import parse_xml_to_json
    
    # Load transactions
    transactions = parse_xml_to_json('../modified_sms_v2.xml')
    
    # Test search
    test_id = 5
    result, time_taken = linear_search_timed(transactions, test_id)
    
    if result:
        print(f"Found transaction {test_id}")
        print(f"Time taken: {time_taken:.8f} seconds")
    else:
        print(f"Transaction {test_id} not found")
    
    # Benchmark
    test_ids = list(range(1, 21))  # Test first 20 IDs
    benchmark = benchmark_linear_search(transactions, test_ids)
    
    print(f"\nBenchmark Results:")
    print(f"Method: {benchmark['method']}")
    print(f"Total searches: {benchmark['total_searches']}")
    print(f"Average time: {benchmark['average_time']:.8f} seconds")
