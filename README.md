# EMEC Drive End of Line tester for production
End of Line tester for EMEC CANOpen Drives (slewing and hovering drive)
Written in python ad using pyQt for UI and canopen module for CANOpen communication.

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

# Hardware

Since the application runs on PC or RPi a CAN converter is needed (normally USB2CAN).
The EMEC Drive have a M12 5 pole male connector.

**M12 5pole connection cable:**

| PIN | Core color     | Signal CANOpen | Description                           |
|-----|----------------|----------------|---------------------------------------|
| 1   | Shield (Brown) | (CAN_SHLD)     | Optional CAN Shield                   |
| 2   | Red    (White) | CAN_V+         | Optional CAN external positive supply |
| 3   | Black  (Blue)  | CAN_GND        | Ground / 0V / V-                      |
| 4   | White  (Black) | CAN_H          | CAN_H bus line                        |
| 5   | Blue   (Grey)  | CAN_L          | CAN_L bus line                        |




