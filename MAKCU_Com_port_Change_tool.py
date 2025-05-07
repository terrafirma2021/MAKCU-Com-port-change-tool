import winreg
import ctypes
import sys
import importlib
import subprocess
import keyboard
import serial.tools.list_ports
import time
import os
import signal
from colorama import init, Fore

init()

VID = 0x1A86
PID = 0x55D3
TARGET_DESC = "USB-Enhanced-SERIAL CH343"
DEFAULT_NAME = "USB-SERIAL CH340"
MAX_NAME_LENGTH = 40

def install_module(module_name):
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

try:
    from colorama import init, Fore
except ImportError:
    print("Installing colorama...")
    install_module("colorama")
    from colorama import init, Fore

init()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        os.kill(os.getpid(), signal.SIGTERM)
    except:
        sys.exit()

def get_device_info(vid, pid):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.vid == vid and port.pid == pid:
            return port.description or "Unknown", port.device
    return None, None

def list_usb_devices():
    ports = serial.tools.list_ports.comports()
    dev_list = []
    for port in ports:
        vid = f"{port.vid:04X}" if port.vid else "N/A"
        pid = f"{port.pid:04X}" if port.pid else "N/A"
        name = port.description or "Unknown"
        dev_list.append(f"Port: {port.device}, VID: {vid}, PID: {pid}, Name: {name}")
    return dev_list

def update_registry_name(vid, pid, new_name):
    key_path = f"SYSTEM\\CurrentControlSet\\Enum\\USB\\VID_{vid:04X}&PID_{pid:04X}"
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
        for i in range(winreg.QueryInfoKey(key)[0]):
            subkey_name = winreg.EnumKey(key, i)
            subkey_path = f"{key_path}\\{subkey_name}"
            subkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, subkey_path, 0, winreg.KEY_ALL_ACCESS)
            winreg.SetValueEx(subkey, "FriendlyName", 0, winreg.REG_SZ, new_name)
            winreg.CloseKey(subkey)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Registry update failed: {e}. Try running as Administrator.")
        return False

def reenumerate_usb():
    try:
        CFGMGR32 = ctypes.WinDLL('cfgmgr32')
        CM_Reenumerate_DevNode = CFGMGR32.CM_Reenumerate_DevNode
        CM_Locate_DevNodeW = CFGMGR32.CM_Locate_DevNodeW
        dev_inst = ctypes.c_uint32()
        CM_Locate_DevNodeW(ctypes.byref(dev_inst), None, 0)
        CM_Reenumerate_DevNode(dev_inst, 0)
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Reenumeration failed: {e}")
        return False

def main():
    os.system('title MAKCU com port changer tool')  # Set terminal title
    if not is_admin():
        print("This script requires administrative privileges. Attempting to relaunch as Administrator...")
        run_as_admin()
    
    last_set_name = None
    while True:
        os.system('cls')
        device_name, com_port = get_device_info(VID, PID)
        display_name = last_set_name if last_set_name else device_name
        if device_name is None:
            print("Target device not found (VID: 1A86, PID: 55D3). Please insert the device.")
            print("\nConnected USB devices:")
            usb_devices = list_usb_devices()
            if usb_devices:
                for dev in usb_devices:
                    print(dev)
            else:
                print("No USB devices detected. Check permissions, drivers, or run as Administrator.")
        else:
            print(f"Device name: {display_name} (Port: {com_port})")
            if TARGET_DESC in device_name:
                print(Fore.GREEN + "Status * Original" + Fore.RESET)
            else:
                print(Fore.RED + "Status * Spoofed" + Fore.RESET)
        
        print("\nMenu:")
        print("1. Restore original name")
        print("2. Spoof kmbox / arduino: USB-SERIAL CH340")
        print("3. Set custom name")
        print("4. Check device again")
        print("5. Exit")
        choice = input("Select option (1-5): ")
        
        if choice == '1':
            if device_name is None:
                print("Device not found. Please insert the device.")
                continue
            if update_registry_name(VID, PID, TARGET_DESC):
                if reenumerate_usb():
                    last_set_name = TARGET_DESC
                    print(f"Device name reverted to {TARGET_DESC}")
                else:
                    print("Reenumeration failed. Try manual scan in Device Manager.")
        elif choice == '2':
            if device_name is None:
                print("Device not found. Please insert the device.")
                continue
            if update_registry_name(VID, PID, DEFAULT_NAME):
                if reenumerate_usb():
                    last_set_name = DEFAULT_NAME
                    print(f"Device name set to {DEFAULT_NAME}")
                else:
                    print("Reenumeration failed. Try manual scan in Device Manager.")
        elif choice == '3':
            if device_name is None:
                print("Device not found. Please insert the device.")
                continue
            print(f"Enter new name (max {MAX_NAME_LENGTH} chars, press Esc to cancel):")
            new_name = ""
            while True:
                if keyboard.is_pressed('esc'):
                    break
                new_name = input()
                if new_name:
                    if len(new_name) > MAX_NAME_LENGTH:
                        print(f"Name too long, max {MAX_NAME_LENGTH} characters")
                    else:
                        if update_registry_name(VID, PID, new_name):
                            if reenumerate_usb():
                                last_set_name = new_name
                                print(f"Device name set to {new_name}")
                            else:
                                print("Reenumeration failed. Try manual scan in Device Manager.")
                        break
        elif choice == '4':
            last_set_name = None
            continue
        elif choice == '5':
            break
        else:
            print("Invalid option")
            input("Press Enter to continue...")
        
        if device_name and com_port:
            try:
                ser = serial.Serial(com_port, 9600, timeout=1)
                ser.close()
            except:
                pass

if __name__ == "__main__":
    main()