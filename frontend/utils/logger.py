import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with the specified name and standardized configuration.
    
    Args:
        name: The name of the logger (typically module or component name)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("../../docs/console/logs/frontend")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%H%M%S_%Y%m%d")
    log_file = log_dir / f"frontend_{timestamp}.log"
    
    # Configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # File handler with detailed formatting
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler with simpler formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def cleanup_logs():
    """
    Clean up old log files according to retention policy:
    - Keep maximum 300 files
    - Remove files older than 30 days
    """
    log_dir = Path("../../docs/console/logs/frontend")
    if not log_dir.exists():
        return
        
    # Get all log files sorted by modification time
    log_files = sorted(
        log_dir.glob("*.log"),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )
    
    # Remove files beyond the 300 limit
    if len(log_files) > 300:
        for file in log_files[300:]:
            try:
                file.unlink()
            except Exception as e:
                print(f"Error deleting {file}: {e}")
    
    # Remove files older than 30 days
    thirty_days_ago = datetime.now().timestamp() - (30 * 24 * 60 * 60)
    for file in log_files:
        if file.stat().st_mtime < thirty_days_ago:
            try:
                file.unlink()
            except Exception as e:
                print(f"Error deleting {file}: {e}")

# Example usage:
# logger = setup_logger(__name__)
# logger.debug("Detailed diagnostic information")
# logger.info("General operational information")
# logger.warning("Warning message for non-critical issues")
# logger.error("Error message for failures")
# logger.critical("Critical failure message") 