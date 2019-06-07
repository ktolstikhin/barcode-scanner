# Barcode Scanner

![](../assets/barcode.png?raw=true)

This is a Python module for scanning barcodes using USB-CDC and HID-POS based scanner devices.

## Install

The dependencies are listed in `requirements.txt` file. One can use `pip` to install them:
```bash
pip3 install --user -r requirements.txt
```

## Usage

One can choose between CLI and GUI when using the scanner module:
```python
from barcode import BarcodeScanner

USE_GUI = True

scanner = BarcodeScanner('/path/to/input/device')
code = scanner.scan_code(USE_GUI)
```
As a result, the following window will pop up:

![](../assets/form.png?raw=true)

Next, try to scan a barcode using a connected scanner, and the code should appear in the text entry.

