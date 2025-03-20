"""
Script to clean up log files according to retention policy.
Run this script periodically (e.g., daily) to maintain log storage.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from frontend.utils.logger import cleanup_logs as cleanup_frontend_logs
from backend.utils.logger import cleanup_logs as cleanup_backend_logs

def main():
    """
    Main function to clean up all log directories.
    """
    print("Starting log cleanup...")
    
    try:
        print("Cleaning frontend logs...")
        cleanup_frontend_logs()
        
        print("Cleaning backend logs...")
        cleanup_backend_logs()
        
        print("Log cleanup completed successfully.")
    except Exception as e:
        print(f"Error during log cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 