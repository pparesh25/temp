import wmi

def get_hard_disk_serial_numbers():
    disk_serial_numbers = {}
    wmi_obj = wmi.WMI()
    for disk in wmi_obj.Win32_DiskDrive():
        disk_serial_numbers[disk.DeviceID] = disk.SerialNumber.strip()
    return disk_serial_numbers

# Get hard disk serial numbers
serial_numbers = get_hard_disk_serial_numbers()

# Print the serial numbers
for device, serial_number in serial_numbers.items():
    print(f"Device: {device}\nSerial Number: {serial_number}\n")
