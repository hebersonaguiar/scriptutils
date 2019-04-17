# This script installs the windows puppet agent on windows 
# from the master's pe_repo by downloading it to C:\tmp first and then running
# msiexec on it from there.

$app = '*Puppet*'
$targetdir = "C:\tmp"
$puppetDir = "C:\Program Files\Puppet Labs\"
$puppetCacheDir = "C:\ProgramData\PuppetLabs\"
$pupeptBat = "C:\Program Files\Puppet Labs\Puppet\bin\"
$msiexec_path = "C:\Windows\System32\msiexec.exe"

function Get-InstalledApps{

    if ([IntPtr]::Size -eq 4) {
        $regpath = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
    }
    else {
        $regpath = @(
            'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*'
            'HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*'
        )
    }
    Get-ItemProperty $regpath | .{process{if($_.DisplayName -and $_.UninstallString) { $_ } }} | Select DisplayName

}

$result = Get-InstalledApps | where {$_.DisplayName -like $app}

function Create-Dir {

    if( -Not (Test-Path -Path $targetdir ) )
    {
        New-Item -ItemType directory -Path $targetdir
        Write-Host "Directory $targetdir Created"
    }else {
        Write-Host "Directory $targetdir Exists"
    }

}

function Enable-WinRM{

    Enable-PSRemoting -Force
    Set-Item wsman:\localhost\client\trustedhosts * -force
    Restart-Service WinRM

}

function Exec-Puppet-Agent {

    Set-Location -Path $pupeptBat
    cmd.exe /C puppet.bat agent -t
    Set-Location -Path C:\
    
}

function Install-Agent {
    
    $puppet_master_server = "srv043.mme.gov.br"
    $version_agent = "5.5.6"
    $msi_source = "http://172.16.1.14/puppet-agent-msi/puppet-agent-$version_agent-x64.msi"
    #$msi_source = "https://downloads.puppetlabs.com/windows/puppet5/puppet-agent-$version_agent-x64.msi"

    Create-Dir

    $msi_dest = "C:\tmp\puppet-agent-$version_agent-x64.msi"
    Invoke-WebRequest -Uri $msi_source -OutFile $msi_dest

    # Start the agent installation process and wait for it to end before continuing.
    Write-Host "Installing puppet agent from $msi_dest"

    # Determine system hostname and primary DNS suffix to determine certname
    $objIPProperties = [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties()
    $name_components = @($objIPProperties.HostName, $objIPProperties.DomainName) | ? {$_}
    $certname = $name_components -Join "."

    $msiexec_args = "/qn /i $msi_dest PUPPET_MASTER_SERVER=$puppet_master_server PUPPET_AGENT_CERTNAME=$certname"

    Start-Process -FilePath $msiexec_path $msiexec_args -Wait -PassThru 

    Write-Host "Removing  Temporary directory $targetdir"    
    Remove-Item -Recurse -Force $targetdir
    
}

function Uninstall-Agent {

    $versionInstalled = ((Get-ItemProperty HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*| 
    Select-Object DisplayName, DisplayVersion) | 
    Where-Object { $_.DisplayName -like "*Puppet*" -and  $_.DisplayVersion } ) |
    Select-Object -Property DisplayVersion |
    select -ExpandProperty DisplayVersion [0] ;

    Write-Host "Program $app Installed and Version $versionInstalled"

    Write-Host "Removing Puppet-Agent-$versionInstalled"

    $targetdir = "C:\tmp"
    $msi_source = "http://172.16.1.14/puppet-agent-msi/puppet-agent-$versionInstalled-x64.msi"
    #$msi_source = "https://downloads.puppetlabs.com/windows/puppet5/puppet-agent-$versionInstalled-x64.msi"

    Create-Dir

    $msi_dest = "C:\tmp\puppet-agent-$versionInstalled-x64.msi"
    Invoke-WebRequest -Uri $msi_source -OutFile $msi_dest

    $msiexec_args = "/qn /norestart /x $msi_dest"
    Start-Process -FilePath $msiexec_path $msiexec_args -Wait -PassThru 

    Write-Host "Puppet-Agent-$versionInstalled Removed"

    Write-Host "Removing  Temporary Directory $targetdir"    
    Remove-Item -Recurse -Force $targetdir

    Write-Host "Removing  Agent Directory $puppetDir"    
    Remove-Item -Recurse -Force $puppetDir

    Write-Host "Removing  Puppet Cache Directory $puppetCacheDir"    
    Remove-Item -Recurse -Force $puppetCacheDir
}

If ($result -eq $null) {
       
    Install-Agent

} Else {

    Uninstall-Agent
    Install-Agent
    Write-Host "Executing Puppet Agent"
    Exec-Puppet-Agent
    Enable-WinRM
    
}

