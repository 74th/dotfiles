reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "LayerDriver JPN" /t REG_SZ /d kbd106.dll
reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "OverrideKeyboardIdentifier" /t REG_SZ /d PCAT_106KEY
reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "OverrideKeyboardSubtype" /t REG_DWORD /d 2
reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "OverrideKeyboardType" /t REG_DWORD /d 7
