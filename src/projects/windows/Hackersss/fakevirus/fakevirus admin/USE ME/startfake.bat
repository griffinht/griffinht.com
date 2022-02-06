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
copy copyshort.bat %AppData%\fakevirus
copy fakevirus.lnk %AppData%\fakevirus
start %AppData%\fakevirus\fakevirus.vbs
start %AppData%\fakevirus\killcmd.bat