# emec_drv_eol_tester
End of Line tester for EMEC CANOpen Drives (slewing and hovering drive)

## Convert UI

Execute pyside6-uic to generate .py from .ui file.
```console
pyside6-uic main.ui > ui_main.py
```
or

Open *Formular->Python-Code anzeigen...* in Qt Designer

**Note:** This project requires to change the following code in *ui_main.py* after it have been converted.
```cosole
import resources_rc --> from . resources_rc import *
```

## Convert QRC
```console
pyside6-rcc resources.qrc -o resources_rc.py
```