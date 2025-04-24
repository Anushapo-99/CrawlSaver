"""
Unit tests for the CrawlSaver checkpoint functionality.

This module contains tests to verify the core functionality of the CrawlSaver class,
focusing on checkpoint save, load, and clear operations.

The tests validate that:
1. Checkpoints can be properly saved to disk with specified data
2. Checkpoint data can be loaded back accurately from disk
3. Checkpoint files can be successfully removed using the clear_checkpoint method

Tests:
    test_checkpoint(): Tests basic checkpoint save/load/clear functionality

Dependencies:
    - os: For file system operations and path validation
    - json: For data serialization (used by CrawlSaver internally)
    - CrawlSaver.checkpoint.CrawlSaver: The main class being tested

Usage:
    Run with pytest:
        pytest tests/test_checkpoint.py
    
    Or with a specific test:
        pytest tests/test_checkpoint.py::test_checkpoint
"""

import os
import json
from CrawlSaver.checkpoint import CrawlSaver

def test_checkpoint():

    """
    Test the basic checkpoint save, load, and clear functionality of CrawlSaver.
    
    This test verifies that:
    - The save_checkpoint method correctly writes data to the specified file
    - The load_checkpoint method correctly retrieves previously saved data
    - The clear_checkpoint method successfully removes the checkpoint file
    
    The test uses a simple dictionary with a page number as test data.
    
    Steps:
    1. Create a CrawlSaver instance with a test file path
    2. Save test data to the checkpoint
    3. Verify the checkpoint file exists
    4. Load the checkpoint data and verify it matches the original data
    5. Clear the checkpoint
    6. Verify the checkpoint file has been removed
    
    Args:
        None
        
    Returns:
        None
        
    Raises:
        AssertionError: If any of the checkpoint operations fail
    """
    test_file = "test_checkpoint.txt"
    saver = CrawlSaver(test_file)
    data = {"page": 5}
    saver.save_checkpoint(data)
    assert os.path.exists(test_file)
    assert saver.load_checkpoint() == data
    saver.clear_checkpoint()
    assert not os.path.exists(test_file)

