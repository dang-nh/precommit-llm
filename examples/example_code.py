#!/usr/bin/env python3
"""
Example Python file with some issues for testing the LLM pre-commit hook.
"""
import os
import sys
import json
import random
from typing import List, Dict, Any


def calculate_total(a, b, c):
    """Calculate the total of three numbers."""
    return a + b + c


def process_data(data_file):
    """
    Process data from a file.
    
    Args:
        data_file: Path to the data file.
    """
    # Security issue: using eval on file content
    with open(data_file, 'r') as f:
        content = f.read()
        result = eval(content)  # Security risk!
    
    # Potential bug: result might be used before assignment if file open fails
    return result


def complex_function(input_data, options=None):
    """
    A complex function with multiple issues.
    
    Args:
        input_data: The input data to process.
        options: Optional configuration.
    """
    if options == None:  # Should use 'is None' instead
        options = {}
    
    # Overly complex nested loops
    results = []
    for i in range(10):
        for j in range(10):
            for k in range(10):
                # Magic numbers
                value = i * 100 + j * 10 + k
                if value % 2 == 0:
                    results.append(value)
    
    # Unused variable
    temp_value = "This variable is never used"
    
    # Inconsistent return type
    if len(results) > 0:
        return results
    else:
        return None


class DataProcessor:
    """A class with various issues."""
    
    def __init__(self):
        self.data = []
        self.processed = False
    
    def add_data(self, item):
        """Add an item to the data list."""
        self.data.append(item)
    
    def process(self):
        """Process the data."""
        # Long method that should be broken down
        result = []
        for item in self.data:
            # Complex processing
            if isinstance(item, dict):
                for key, value in item.items():
                    if isinstance(value, (int, float)):
                        result.append(value * 2)
                    elif isinstance(value, str):
                        result.append(value.upper())
                    else:
                        result.append(str(value))
            elif isinstance(item, list):
                for element in item:
                    if isinstance(element, (int, float)):
                        result.append(element * 2)
                    else:
                        result.append(str(element))
            else:
                result.append(item)
        
        self.processed = True
        return result


if __name__ == "__main__":
    # Hardcoded credentials
    API_KEY = "sk_test_abcdefghijklmnopqrstuvwxyz123456789"
    
    # Unused import
    import datetime
    
    # Call function with magic numbers
    total = calculate_total(10, 20, 30)
    print(f"Total: {total}")
    
    # Create and use DataProcessor
    processor = DataProcessor()
    processor.add_data({"name": "John", "age": 30})
    processor.add_data([1, 2, 3, "test"])
    result = processor.process()
    print(f"Processed data: {result}") 