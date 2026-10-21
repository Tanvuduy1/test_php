@echo off
echo Dang khoi chay Edge o che do Remote Debugging Port 9222...
if not exist "D:\Tan\work\test_php\.edge_profile" mkdir "D:\Tan\work\test_php\.edge_profile"
start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --remote-debugging-port=9222 --user-data-dir="D:\Tan\work\test_php\.edge_profile" "https://dev-85.midesk.vn/vi?c=ticket&id=default"
echo Da khoi chay xong!
