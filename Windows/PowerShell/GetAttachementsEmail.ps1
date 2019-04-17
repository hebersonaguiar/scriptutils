#Opens up connection to outlook
$o = New-Object -ComObject Outlook.Application
$n = $o.GetNamespace("MAPI")

#sets inbox variable
$inbox=$n.GetDefaultFolder(6)

#sets filepaths for attachments to be saved to 
$filepath = ""

#set date and year for subject and date (TODAY)
#$date = (Get-Date -UFormat "%d/%m/%Y").ToString()
$date = (Get-Date).ToString("d")
$year = Get-Date -UFormat "%Y"

#set email from
$emailFrom = ""


#loops through each mail item
#saves attachment to filepath based on subject line
$inbox.Items | foreach{
   If($_.subject -match "ACOMP $($year) " -and $_.ReceivedTime.ToString() -like "*$($date)*" -and $_.SenderEmailAddress.ToString() -match $emailFrom){    
    #Write-Host $_.ReceivedTime
    #Write-Host $_.SenderEmailAddress    
   	$_.attachments | foreach{
	   #$_.saveasfile((Join-Path $filepathPick $_.filename))        
        #Write-Host $_.filename        
            $a = $_.filename
            If ($a.Contains("csv") -or $a.Contains("xls") -or $a.Contains("xlsx")) {
                $_.saveasfile((Join-Path $filepath $_.filename))                
           }
	}
   }
}
