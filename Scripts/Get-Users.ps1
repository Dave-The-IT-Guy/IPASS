$location = "S:\users.txt"

Try {
    Remove-Item -Path $location -Force | Out-Null
}

Catch {}

$AccountNames = Get-AdGroupMember -Identity Ubuntu

foreach($Account in $AccountNames) {
    If ($Account.objectClass -eq "user") {
        Out-File $location -InputObject $Account.SamAccountName -Encoding ascii -Append
    }
}