import tkinter as tk
import GPUtil
import platform
import psutil
import socket
import datetime
from screeninfo import get_monitors
from tkinter import ttk

# 創建Tkinter窗口
root = tk.Tk()
root.title("系統資訊顯示工具")

# 設定視窗寬度
root.geometry("800x600")

# 創建Treeview
tree = ttk.Treeview(root, height=20)
tree["columns"] = ("value")
tree.heading("#0", text="項目")
tree.heading("value", text="數值")
tree.column("#0", width=300)
tree.column("value", width=450)
tree.pack()

def get_display_info():
    monitors = get_monitors()
    monitor_info = []
    for monitor in monitors:
        monitor_info.append(f"{monitor.name}: {monitor.width}x{monitor.height} @ {monitor.width_mm}mm x {monitor.height_mm}mm")
    return "\n".join(monitor_info)

def get_gpu_info():
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = []
        for gpu in gpus:
            gpu_info.append(f"{gpu.name}: {gpu.memoryFree:.2f} MB 可用 / {gpu.memoryTotal:.2f} MB 總共")
        return "\n".join(gpu_info)
    except ImportError:
        return "未能獲取顯示卡資訊"

def get_gpu_temperature():
    try:
        gpus = GPUtil.getGPUs()
        gpu_temp_info = []
        for gpu in gpus:
            gpu_temp_info.append(f"GPU {gpu.id}: {gpu.temperature}°C")
        return "\n".join(gpu_temp_info)
    except Exception as e:
        return f"獲取GPU溫度失敗: {e}"

def get_network_speed():
    net_io = psutil.net_io_counters()
    return f"上行速度: {format(net_io.bytes_sent / 1024 / 1024, '.2f')} MB/s，下行速度: {format(net_io.bytes_recv / 1024 / 1024, '.2f')} MB/s"

def get_system_users():
    users = psutil.users()
    user_names = [user.name for user in users]
    return "，".join(user_names)

def get_ram_info():
    virtual_memory = psutil.virtual_memory()
    total_ram = virtual_memory.total / (1024 ** 3)  # GB
    used_ram = virtual_memory.used / (1024 ** 3)    # GB
    available_ram = virtual_memory.available / (1024 ** 3)  # GB
    return f"總內存: {total_ram:.2f} GB，已用內存: {used_ram:.2f} GB，可用內存: {available_ram:.2f} GB"

def get_system_load():
    load_avg = psutil.getloadavg()  # 获取平均负载
    cpu_load = psutil.cpu_percent(interval=1)
    memory_load = psutil.virtual_memory().percent
    return f"平均負載: {load_avg}, CPU負載: {cpu_load:.2f}%, 內存負載: {memory_load:.2f}%"

def get_disk_info():
    disk_info = []
    partitions = psutil.disk_partitions()
    for partition in partitions:
        partition_info = psutil.disk_usage(partition.mountpoint)
        disk_info.append(f"硬碟 {partition.device}({partition.mountpoint}): 大小 {partition_info.total / (1024 ** 3):.2f} GB, 類型 {partition.fstype}")
    return "\n".join(disk_info)

def get_system_uptime():
    boot_time = psutil.boot_time()
    current_time = datetime.datetime.now().timestamp()
    uptime_seconds = current_time - boot_time

    uptime_timedelta = datetime.timedelta(seconds=uptime_seconds)
    days = uptime_timedelta.days
    hours, remainder = divmod(uptime_timedelta.seconds, 3600)
    minutes = remainder // 60

    if days > 0:
        uptime_str = f"{days}天{hours}小時{minutes}分鐘前"
    elif hours > 0:
        uptime_str = f"{hours}小時{minutes}分鐘前"
    else:
        uptime_str = f"{minutes}分鐘前"

    return uptime_str

def get_cpu_info():
    cpu_info = []
    cpu_count = psutil.cpu_count(logical=False)  # 獲取實際物理核心數
    cpu_freq = psutil.cpu_freq().current / 1000  # 獲取當前CPU頻率（轉換為GHz）
    cpu_info.append(f"CPU核心數: {cpu_count} 個, CPU頻率: {cpu_freq:.2f} GHz")
    return "\n".join(cpu_info)

def update_tree():
    system_info = get_system_info()
    tree.delete(*tree.get_children())
    for key, value in system_info.items():
        tree.insert("", "end", text=key, values=(value,))

def get_system_info():
    system_info = {
        "系統": platform.system(),
        "版本": platform.release(),
        "架構": platform.machine(),
        "處理器": platform.processor(),
        "記憶體": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
        "IP位置": socket.gethostbyname(socket.gethostname()),
        "主機名稱": socket.gethostname(),
        "顯示器": get_display_info(),
        "顯示卡": get_gpu_info(),
        "顯示卡溫度": get_gpu_temperature(),
        "網絡速度": get_network_speed(),
        "用戶名稱": get_system_users(),
        "記憶體": get_ram_info(),
        "系統負載": get_system_load(),
        "硬碟資訊": get_disk_info(),
        "CPU核心數和頻率": get_cpu_info(),
        "距離上一次開機的運行時間": get_system_uptime()
    }
    return system_info

# 創建刷新按鈕
update_button = tk.Button(root, text="刷新按鈕", command=update_tree)
update_button.pack()

# 初始化顯示系統信息
update_tree()

# 開始Tkinter主循環
root.mainloop()