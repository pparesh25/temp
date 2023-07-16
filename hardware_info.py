import platform
import psutil
import socket

def get_system_info():
    system_info = {
        'System': platform.system(),
        'Node Name': platform.node(),
        'Release': platform.release(),
        'Version': platform.version(),
        'Processor': platform.processor(),
        'Architecture': platform.machine(),
        'RAM': f'{round(psutil.virtual_memory().total / (1024**3), 2)} GB',
        'CPU Usage': f'{psutil.cpu_percent()}%',
        'Disk Usage': f'{psutil.disk_usage("/").percent}%',
        'Battery': psutil.sensors_battery().percent if psutil.sensors_battery() else 'N/A',
    }

    # Get hard disk information
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            disk_usage = psutil.disk_usage(partition.mountpoint)
            disk_info.append({
                'Device': partition.device,
                'Mount Point': partition.mountpoint,
                'File System': partition.fstype,
                'Total Size': f'{round(disk_usage.total / (1024**3), 2)} GB',
                'Used': f'{round(disk_usage.used / (1024**3), 2)} GB',
                'Free': f'{round(disk_usage.free / (1024**3), 2)} GB',
                'Usage': f'{disk_usage.percent}%'
            })
        except PermissionError as e:
            print(f"PermissionError: {e}")
    
    system_info['Hard Disk'] = disk_info

    return system_info

# Get system information
system_info = get_system_info()

# Print system information
for key, value in system_info.items():
    if isinstance(value, list):
        print(f'{key}:')
        for item in value:
            for k, v in item.items():
                print(f'  {k}: {v}')
    else:
        print(f'{key}: {value}')
