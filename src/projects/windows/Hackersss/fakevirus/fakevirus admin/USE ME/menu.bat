@echo off
:start
cls
echo -info (get info on fakevirus)
echo -help (lists possible commands)
echo -execute (executes various fakevirus programs)
echo -exit (exits this menu)
echo.
set /p CHOICE1= 
goto %CHOICE1%

:help
cls
echo -start (goes to the start of menu)
echo -info (get info on fakevirus)
echo -notepad (opens info.txt)
echo -console (opens info in this menu)
echo -location (tells the location of fakevirus)
echo -fake (gives info about fakevirus)
echo -execute (gives a list of commands to execute various fakevirus programs)
echo -startall (starts the spreading and program of fakevirus)
echo -spread (spreads fakevirus to AppData)
echo -abort (cancels shutdown)
echo -killcmd (kills all cmd windows and processes)
echo -startfake (starts fakevirus)
echo -exit (exits this menu)
echo -shutdown (shuts down your machine)
echo.
set /p CHOICE2=
goto %CHOICE2%

:info
cls
echo -notepad (opens info.txt)
echo -console (opens in this menu)
echo.
set /p CHOICE3=
goto %CHOICE3%

:notepad
cls
start info.txt
pause
goto start

:console
cls
echo -location (tells the location of fakevirus)
echo -fake (gives info about fakevirus)
echo.
set /p CHOICE4=
goto %CHOICE4%

:location
cls
echo  %appdata%\fakevirus
echo.
set /p CHOICE5=
goto %CHOICE5%

:fake
cls
echo Fakevirus is a fake virus that shuts down your computer after a series of fake propmts.
echo.
set /p CHOICE6=
goto %CHOICE6%

:execute
cls
echo -startall (starts the spreading and program of fakevirus)
echo -spread (spreads fakevirus to AppData)
echo -abort (cancels shutdown)
echo -killcmd (kills all cmd windows and processes)
echo -startfake (starts fakevirus)
echo -shutdown (shuts down your machine)
echo.
set /p CHOICE7=
goto %CHOICE7%

:startall
cls
echo Spreading fakevirus...
start spread.bat
echo Starting fakevirus...
start startfake.bat
echo Success!
echo.
set /p CHOICE8=
goto %CHOICE8%

:spread
cls
echo Spreading fakevirus...
start spread.bat
echo Success!
echo.
set /p CHOICE9=
goto %CHOICE9%

:abort
cls
echo Aborting fakevirus shutdown...
start abortadmin.vbs
echo Success!
echo.
set /p CHOICE10=
goto %CHOICE10%

:killcmd
cls
echo Stopping Command Prompt (cmd.exe)
start killcmd.bat
echo Success!
echo.
set /p CHOICE11=
goto %CHOICE11%

:startfake
cls
echo Starting fakevirus
start startfake.bat
echo Success!
echo.
set /p CHOICE12=
goto %CHOICE12%

:shutdown
cls
echo Shutting down in 30 seconds...
start shutdownadmin.vbs
echo Suucces!
echo -abort (aborts the shutdown)
echo.
set /p CHOICE13=
goto %CHOICE13%
:exit
exit