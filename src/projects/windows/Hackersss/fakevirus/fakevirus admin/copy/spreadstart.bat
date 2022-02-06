@echo off
mkdir %AppData%\fakevirus
copy fakevirus.vbs %AppData%\fakevirus
copy runadmin.vbs %AppData%\fakevirus
copy shutdown.bat %AppData%\fakevirus
copy startfake.bat %AppData%\fakevirus
copy abortadmin.vbs %AppData%\fakevirus
copy abortshutdown.bat %AppData%\fakevirus
copy info.txt %AppData%\fakevirus
copy killcmd.bat %AppData%\fakevirus
copy menu.bat %AppData%\fakevirus
copy spreadstart.bat %AppData%\fakevirus
copy fakevirusrun.exe %AppData%\fakevirus
start %AppData%\fakevirus\startfake.bat