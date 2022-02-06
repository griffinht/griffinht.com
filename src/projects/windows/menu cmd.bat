@echo off
echo Type in a command
set /p CHOICE=
goto:%CHOICE%
:command
echo Type in a command
set /p CHOICE=
%CHOICE%
goto:cmdSet
:abortShutdown
shutdown /a
echo Attempting to abort shutdown
echo Type in a command
set /p CHOICE=
goto:%CHOICE%
:dir
echo Type a directory
set /p CHOICE=
dir %CHOICE%
echo Type in a command
set /p CHOICE=
goto:%CHOICE%
:users
:user
echo Type a user
set /p CHOICE=
dir C:\Users\%CHOICE%
echo Type in a command
set /p CHOICE=
goto:%CHOICE%
:shutdown
set /p CHOICE=Normal Shutdown?[Y,N]_
if /i %CHOICE% == y shutdown /p
if /i %CHOICE% == n set /p CHOICE=Local or Remote?[1,2]_
if /i %CHOICE% == 1 goto:local
if /i %CHOICE% == 2 set /p CHOICE=Type the local IP Adress of the targeted computer (on your network running Windows)MUST NOT BE BLOCKED_
shutdown /i %CHOICE%
echo Attempting to shut down remote computer
:local
echo Local shutdown. Custom[1], GUI[2], Log off[3], Shutdown & Restart[4], Abort a shutdown[5], Hibernate[6], Shutdown with a custom message[7], Shutdown with a time limit[8]
set /p CHOICE=Type a number_
if /i %CHOICE% == 1 (
  set /p CMD=Type shutdown command options (e.g. /a /m computerName)_
  shutdown %CMD%
)
if /i %CHOICE% == 2 shutdown /i
if /i %CHOICE% == 3 shutdown /l
if /i %CHOICE% == 4 shutdown /r
if /i %CHOICE% == 5 goto:abortShutdown
if /i %CHOICE% == 6 shutdown /h
if /i %CHOICE% == 7 (
  set /p CHOICE=Type your custom message_
  shutdown /s /c %CHOICE%
)
if /i %CHOICE% == 8 (
  set /p CHOICE=Type the time limit
  shutdown /s /t %CHOICE%
}
