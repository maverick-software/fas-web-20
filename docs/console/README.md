# Console Logging System Documentation

## Overview
The Financial Analysis System v2.0 implements a comprehensive logging system for both frontend and backend components. The system follows structured logging practices with automated cleanup and retention policies.

## Directory Structure
```
docs/console/
├── logs/
│   ├── frontend/     # Frontend application logs
│   └── backend/      # Backend API logs
└── README.md        # This documentation file
```

## Logging Configuration

### Frontend Logging (`frontend/utils/logger.py`)
- Log files named: `frontend_HHMMSS_YYYYMMDD.log`
- Log levels: DEBUG (file), INFO (console)
- Detailed formatting for file logs
- Simplified formatting for console output

### Backend Logging (`backend/utils/logger.py`)
- Log files named: `backend_HHMMSS_YYYYMMDD.log`
- Log levels: DEBUG (file), INFO (console)
- Endpoint decorator for API call logging
- Request timing and error tracking

## Retention Policy
- Maximum 300 log files per component
- 30-day retention period
- Automated cleanup via scheduled task

## Log Cleanup
- Script: `scripts/cleanup_logs.py`
- Scheduler: `scripts/schedule_log_cleanup.bat`
- Runs daily at 3 AM
- Requires administrator privileges for scheduling

## Usage Examples

### Frontend Logging
```python
from utils.logger import setup_logger

logger = setup_logger("component_name")
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error details")
logger.critical("Critical system error")
```

### Backend API Logging
```python
from utils.logger import setup_logger, log_endpoint

logger = setup_logger("api")

@log_endpoint(logger)
async def your_endpoint():
    # Your endpoint code here
    pass
```

## Maintenance
- Log files are automatically cleaned up based on retention policy
- Manual cleanup can be triggered by running `cleanup_logs.py`
- Monitor `docs/console/logs/_change.logs` for system changes

## Troubleshooting
1. If logs are not being created:
   - Check directory permissions
   - Verify logger configuration
   - Ensure correct import paths

2. If cleanup task fails:
   - Run scheduler script with administrator privileges
   - Check Task Scheduler for task status
   - Verify Python environment is accessible to scheduled task 