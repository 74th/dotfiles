reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "LayerDriver JPN" /t REG_SZ /d kbd101.dll
reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "OverrideKeyboardIdentifier" /t REG_SZ /d PCAT_101KEY
reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "OverrideKeyboardSubtype" /t REG_DWORD /d 0
reg add HKLM\SYSTEM\CurrentControlSet\Services\i8042prt\Parameters /f /v "OverrideKeyboardType" /t REG_DWORD /d 7
