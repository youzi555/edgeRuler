import psutil
import sched
import time
import threading

def getMemoryUse():
    mem = psutil.virtual_memory()
    return mem.percent

def getCPUUse():
    cpu = psutil.cpu_percent(interval=1)
    return cpu

def scheduleMonitor():
    memUse = getMemoryUse()
    cpuUse = getCPUUse()
    threading.Timer(300, scheduleMonitor).start()
    
threading.Timer(300, scheduleMonitor).start()
