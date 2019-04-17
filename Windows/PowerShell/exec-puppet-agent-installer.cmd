PowerShell -Command "Set-ExecutionPolicy Unrestricted" >> "C:\StartupLogPuppetAgent.txt" 2>&1 
PowerShell C:\Users\heberson\Desktop\puppet-agent-installer.ps1 >> "C:\StartupLogPuppetAgent.txt" 2>&1
PowerShell -Command "Remove-Item -Recurse -Force C:\Users\heberson\Desktop\puppet-agent-installer.ps1" >> "C:\StartupLogPuppetAgent.txt" 2>&1
