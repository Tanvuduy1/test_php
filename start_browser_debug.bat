@echo off
echo Dang khoi chay Chrome che do go loi Remote Debugging Port 9222...
if not exist "D:\Tan\work\test_php\.chrome_profile" mkdir "D:\Tan\work\test_php\.chrome_profile"
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="D:\Tan\work\test_php\.chrome_profile" "https://dev-85.midesk.vn/vi?c=ticket&id=default"
echo Da khoi chay xong!
