@echo off
:home
cls
echo -shutdown (shuts down)
echo -help (lists possible commands)
echo -execute (showa a list various executable programs)
echo -exit (exit)
echo.
set /p CHOICE1= 
goto %CHOICE1%

:help
cls
echo -home (goes to the start of menu)
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

:execute
cls
echo -chrome
echo -coding
echo -steam
echo -games
echo.
set /p CHOICE2=
goto %CHOICE2%

:chrome
cls
echo Starting Chrome
start chrome.lnk
echo.
set /p CHOICE2=
goto %CHOICE2%

:coding
cls
echo -hackers
echo -codebits
echo -code_tools
echo.
set /p CHOICE3=
goto %CHOICE3%

:shutdown
cls
echo Shutting down in 30 seconds...
start shutdownadmin.vbs
echo Success!
echo -abort (aborts the shutdown)
echo.
set /p CHOICE5=
goto %CHOICE5%