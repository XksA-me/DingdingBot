import psutil as psu
import os
from time import time
from datetime import timedelta

'''
系统数据获取和预警设置模块
'''


'''
云服务器基础数据
服务器已运行时间、负载状态、CPU使用率、运行内存使用率、物理内存使用率
'''
def get_server_info():
    # 获取系统的基本数据
    # 服务器已运行时间
    run_times = str(timedelta(seconds=int(time())-int(psu.boot_time())))
    # 系统负载状态（最近1、5、15分钟）
    loadavg = [round(i, 2) for i in os.getloadavg()]
    # CPU使用率 测试间隔0.3秒
    cpu_in_use = psu.cpu_percent(interval=0.3)
    # 系统运行内存使用率
    # 内存使用率大于80% 触发报警
    vm_in_use = psu.virtual_memory().percent
    vm_available = round(psu.virtual_memory().available/(1024**3), 2)
    # 系统物理存储使用率
    disk_in_use = psu.disk_usage('/').percent
    disk_free = round(psu.disk_usage('/').free/(1024**3), 2)
    
    # 还可以添加进程、线程等信息，后面专门安排一篇文章写
    
    base_info = f"""### 服务器基本信息
> 您的云服务器已运行-{run_times}，机器负载情况为(最近1、5、15分钟)：{loadavg}
![](https://img-blog.csdnimg.cn/246a90c55c4e46dca089731c5fd00833.png)
- 目前CPU使用率为：{cpu_in_use}%，
- 系统运行内存使用率为：{vm_in_use}%，
- 剩余可用运行内存为：{vm_available}GiB，
- 系统存储内存使用率为：{disk_in_use}%，
- 剩余可用存储内存为：{disk_free}GiB
\n**{'机器CPU使用率正常' if cpu_in_use<=80 else '机器CPU使用率过高，可能触发预警'}**
"""
    return base_info, loadavg, cpu_in_use, vm_in_use, disk_in_use
    
    
'''
服务器预警设置
本篇先简单点，只设置负载和CPU使用率预警
'''
def get_warning():
    base_info, loadavg, cpu_in_use, vm_in_use, disk_in_use = get_server_info()
    # 首先判断服务器负载情况
    # 只看近一分钟和近十五分钟情况 应该<= 0.7*CPU数量
    loadavg_max = psu.cpu_count() * 0.7
    loadavg_max = 0.01   # 测试使用，正式环境请注释掉
    if loadavg[0] >= loadavg_max and loadavg[2] >= loadavg_max:
        warning1 = f'⚠️<font color="#d30c0c">【警告】</font>您的云服务器当前负载率为(最近1、5、15分钟)-{loadavg}，负载率已达<font color="#d30c0c">{round(loadavg[2]/loadavg_max, 2)*100}%</font>，请及时检查系统是否存在问题，也可以@我，发送：基础信息，查看云服务器基础信息。'
        return warning1
        
    if cpu_in_use >= 80:
        warning2 = f'⚠️<font color="#d30c0c">【警告】</font>您的云服务器当前CPU使用率为<font color="#d30c0c">{cpu_in_use}%</font>，请及时检查系统是否存在问题，也可以@我，发送：基础信息，查看云服务器基础信息。'
        return warning2
    return 'ok'
