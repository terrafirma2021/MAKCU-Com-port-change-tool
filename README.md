# MAKCU COM Port Changer Tool

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

The **MAKCU COM Port Changer Tool** is a Python utility that modifies the friendly name of USB serial devices with Vendor ID (VID) `0x1A86` and Product ID (PID) `0x55D3` (e.g., MAKCU devices with CH343 chipset). It enables users to rename the device in the Windows registry to restore its original name, spoof it as another device, or set a custom name. Notably, it allows spoofing the device as `USB-SERIAL CH340` to enable compatibility with cheats or software expecting a kmbox B Pro device.

## Features

- **Restore Original Name**: Reverts the device name to `USB-Enhanced-SERIAL CH343`.
- **Spoof kmbox B Pro**: Sets the device name to `USB-SERIAL CH340`, allowing cheats or software designed for kmbox B Pro to connect to a MAKCU device.
- **Custom Name**: Supports user-defined device names (up to 40 characters).
- **Device Detection**: Lists all connected USB serial devices with their port, VID, PID, and name.
- **Registry Modification**: Updates the Windows registry's `FriendlyName` for the target device.
- **USB Reenumeration**: Automatically reenumerates USB devices to apply changes.
- **Admin Privileges**: Auto-requests elevation if not running as administrator.

## Use Case

This tool is ideal for users needing to make a MAKCU device appear as a kmbox B Pro device (`USB-SERIAL CH340`) to work with specific software or cheats that require this device name for compatibility.

## Requirements

- **OS**: Windows (due to `winreg` and `cfgmgr32` dependencies).
- **Python**: 3.x.
- **Dependencies**:
  - `pyserial`: For USB serial port detection.
  - `colorama`: For colored console output.
  - `keyboard`: For Esc key detection during custom name input.
- **Admin Privileges**: Required for registry modifications and USB reenumeration.

## Installation

1. Clone or download the repository:
   ```bash
   git clone https://github.com/your-username/makcu-com-port-changer.git
   ```
2. Navigate to the project directory:
   ```bash
   cd makcu-com-port-changer
   ```
3. Install dependencies:
   ```bash
   pip install pyserial colorama keyboard
   ```

## Usage

1. Run the script as an administrator:
   ```bash
   python com_port_changer.py
   ```
   - The script will request elevation if not run as administrator.
2. Choose from the menu:
   - **1**: Restore original name (`USB-Enhanced-SERIAL CH343`).
   - **2**: Spoof kmbox B Pro (`USB-SERIAL CH340`).
   - **3**: Set a custom name (max 40 characters; Esc to cancel).
   - **4**: Refresh device information.
   - **5**: Exit.
3. Select an option by entering 1–5. The tool updates the registry and reenumerates the device automatically.

## Example Output

```
Device name: USB-SERIAL CH340 (Port: COM3)
Status * Spoofed

Menu:
1. Restore original name
2. Spoof kmbox / arduino: USB-SERIAL CH340
3. Set custom name
4. Check device again
5. Exit
Select option (1-5):
```

## Notes

- **Admin Privileges**: Required for registry access and USB reenumeration.
- **Device Not Found**: If the target device (VID: `0x1A86`, PID: `0x55D3`) isn’t detected, the tool lists all USB serial devices for troubleshooting.
- **Reenumeration Failure**: If automatic reenumeration fails, manually scan for hardware changes in Device Manager.
- **Windows Only**: The tool uses Windows-specific APIs and is not cross-platform.

## Disclaimer

This tool modifies the Windows registry and USB device configurations. Use at your own risk. The author is not responsible for damages from improper use. Spoofing device names for cheats may violate software terms of service.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Submit a pull request or open an issue to discuss improvements or bugs.
