@echo off
echo Scheduling daily log cleanup...

:: Create a Windows Task Scheduler task to run cleanup_logs.py daily at 3 AM
schtasks /create /tn "FAS_LogCleanup" /tr "python %~dp0cleanup_logs.py" /sc daily /st 03:00 /f

if %ERRORLEVEL% EQU 0 (
    echo Log cleanup task scheduled successfully.
    echo Task will run daily at 3 AM.
) else (
    echo Failed to schedule log cleanup task.
    echo Please run this script with administrator privileges.
)

pause 