a=MsgBox("Failed to open Testgame. Do you want to fix it?",4+64,"Testgame")
if a=6 then aa=MsgBox("Attempting to fix Testgame",1+48,"Testgame Help")
if aa=2 then ac=MsgBox("Failed to stop operation!",0+48,"Testgame Help")
if a=7 then ab=MsgBox("Failed to stop operation!",0+48,"Testgame Help")
b=MsgBox("Failed to fix Testgame.",2+48,"Testgame Help")
if b=3 then ba=MsgBox("Failed to abort. Continuing...",0+48,"Testgame Help")
if b=5 then ba=MsgBox("Cannot ignore message. Continuing...",0+48,"Testgame Help")
if b=4 then ba=MsgBox("Failed to retry. Continuing...",0+48,"Testgame Help")
c=MsgBox("Shutting Down. Have a nice day!",1+48,"Testgame Help")
Set objShell = WScript.CreateObject("WScript.Shell")
objShell.Run "C:\WINDOWS\system32\shutdown.exe -s -t 10"
if c=2 then ba=MsgBox("Cannot cancel action. Continuing...",0+48,"Testgame Help")
Set objShell = WScript.CreateObject("WScript.Shell")
objShell.Run "fake2d1.vbs"