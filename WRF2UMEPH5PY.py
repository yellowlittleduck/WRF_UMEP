import h5py
import numpy as np
import pandas as pd
import os
import glob
import datetime
from tqdm import tqdm
import math
import traceback

# 计算风速和风向的函数
def calculate_wind_speed_dir(u10, v10):
    """从U10和V10计算风速和风向"""
    wspd = np.sqrt(u10**2 + v10**2)  # 风速
    wdir = (270 - np.rad2deg(np.arctan2(v10, u10))) % 360  # 风向，气象学定义
    return wspd, wdir

# 计算相对湿度的函数
def calculate_rh(t2, psfc, q2):
    """
    计算2米相对湿度
    t2: 2米温度 (摄氏度)
    psfc: 地表气压 (Pa)
    q2: 2米水汽混合比 (kg/kg)
    """
    # 饱和水汽压计算 (Bolton方程)
    es = 6.112 * np.exp(17.67 * t2 / (t2 + 243.5))  # 饱和水汽压 (hPa)
    
    # 实际水汽压
    e = q2 * psfc / 100 / (0.622 + 0.378 * q2)  # hPa
    
    # 相对湿度
    rh = 100.0 * e / es  # 百分比
    # 限制在0-100%范围内
    rh = np.clip(rh, 0, 100)
    return rh

# 设置路径和参数
case_path = r'D:\ZJU\科研\pycode\data'
date = '20240801'
# 直接从WRF输出文件中获取的变量
direct_vars = ['T2', 'PSFC', 'SWDOWN', 'GLW', 'Q2', 'U10', 'V10']
# 最终需要的变量
var_names = ['T2', 'rh2', 'wspd10', 'wdir10', 'SWDOWN', 'GLW', 'PSFC']
var_dict = {'wspd10':'Wind', 'rh2':'RH', 'T2':'Td', 'PSFC':'press', 'SWDOWN':'Kdn', 'GLW':'ldown', 'wdir10':'Wd'}

# 查找所有WRF输出文件
paths = glob.glob(os.path.join(case_path, 'wrfout_d04*'))
print(f"找到的文件数量: {len(paths)}")

# 处理直接变量
for var_name in direct_vars:
    i = 0
    for path in tqdm(paths, desc=var_name):
        # 提取文件名中的日期时间部分
        filename = os.path.basename(path)
        datetime_part = filename.split('_', 2)[2]
        
        # 替换特殊字符并解析
        datetime_part = datetime_part.replace('^%', '')
        UTC8 = pd.to_datetime(datetime_part, format='%Y-%m-%d_%H%M%S') + datetime.timedelta(hours=8)
        
        try:
            # 使用h5py打开WRF文件
            with h5py.File(path, 'r') as f:
                # 检查变量是否存在
                if var_name in f:
                    # 读取变量数据
                    raw_data = np.array(f[var_name])
                    
                    # 根据变量名进行必要的转换
                    if var_name in ['T2', 'TSK']:
                        field = raw_data - 273.15  # 开尔文转摄氏度
                    elif var_name == 'PSFC':
                        field = raw_data / 1000  # Pa转kPa
                    else:
                        field = raw_data
                    
                    # 处理第一个和后续文件的不同逻辑
                    if i == 0:
                        ary = field
                    else:
                        ary = np.dstack((ary, field))
                    
                    i += 1
                else:
                    print(f"警告: 在文件 {path} 中未找到变量 {var_name}")
                    # 尝试列出文件中的所有变量
                    if i == 0:
                        print(f"文件中可用的变量: {list(f.keys())}")
                    continue
        except Exception as e:
            print(f"处理文件 {path} 时出错: {e}")
            continue
    
    # 保存处理后的数据
    if i > 0:
        output_file = os.path.join(case_path, f"{var_name}_{date}.npy")
        # 转置数组以匹配预期的形状 [时间, 纬度, 经度]
        np.save(output_file, np.array(ary.transpose(2, 0, 1)))
        print(f"已保存: {output_file}")
    else:
        print(f"警告: 未能处理任何 {var_name} 数据")

# 计算派生变量
# 1. 计算相对湿度 (rh2)
try:
    t2_path = os.path.join(case_path, f"T2_{date}.npy")
    q2_path = os.path.join(case_path, f"Q2_{date}.npy")
    psfc_path = os.path.join(case_path, f"PSFC_{date}.npy")
    
    if os.path.exists(t2_path) and os.path.exists(q2_path) and os.path.exists(psfc_path):
        t2_data = np.load(t2_path)  # 已经是摄氏度
        q2_data = np.load(q2_path)
        psfc_data = np.load(psfc_path) * 1000  # 转回Pa

        # 检查数据形状
        print(f"T2数据形状: {t2_data.shape}")
        print(f"Q2数据形状: {q2_data.shape}")
        print(f"PSFC数据形状: {psfc_data.shape}")
        
        # 计算相对湿度
        rh_data = np.zeros_like(t2_data)
        for i in range(t2_data.shape[0]):
            rh_data[i] = calculate_rh(t2_data[i], psfc_data[i], q2_data[i])
        
        np.save(os.path.join(case_path, f"rh2_{date}.npy"), rh_data)
        print(f"已保存: {os.path.join(case_path, f'rh2_{date}.npy')}")
    else:
        print("警告: 计算相对湿度所需的文件不存在")
except Exception as e:
    print(f"计算相对湿度时出错: {e}")

# 2. 计算风速和风向
try:
    u10_path = os.path.join(case_path, f"U10_{date}.npy")
    v10_path = os.path.join(case_path, f"V10_{date}.npy")
    
    if os.path.exists(u10_path) and os.path.exists(v10_path):
        u10_data = np.load(u10_path)
        v10_data = np.load(v10_path)
        
        wspd_data = np.zeros_like(u10_data)
        wdir_data = np.zeros_like(u10_data)
        
        for i in range(u10_data.shape[0]):
            wspd, wdir = calculate_wind_speed_dir(u10_data[i], v10_data[i])
            wspd_data[i] = wspd
            wdir_data[i] = wdir
        
        np.save(os.path.join(case_path, f"wspd10_{date}.npy"), wspd_data)
        np.save(os.path.join(case_path, f"wdir10_{date}.npy"), wdir_data)
        print(f"已保存: {os.path.join(case_path, f'wspd10_{date}.npy')}")
        print(f"已保存: {os.path.join(case_path, f'wdir10_{date}.npy')}")
        print(f"风速数据形状: {wspd_data.shape}")
        print(f"风向数据形状: {wdir_data.shape}")
    else:
        print("警告: 计算风速风向所需的文件不存在")
except Exception as e:
    print(f"计算风速风向时出错: {e}")

# 准备UMEP格式的气象数据
def umep_met_init(time_steps):
    """初始化UMEP气象数据格式"""
    columns = ['#iy','id','it','imin','Q*','QH','QE','Qs','Qf',
              'Wind','RH','Td','press','rain','Kdn','snow',
              'ldown','fcld','wuh','xsmd','lai_hr','Kdiff','Kdir','Wd']
    
    # 根据实际时间步数调整
    # 从8月1日00时到8月3日23时，共72小时
    days = []
    hours = []
    
    # 计算每个时间步的日期和小时
    for i in range(time_steps):
        current_hour = i % 24
        current_day = 1 + i // 24  # 从8月1日开始
        days.append(current_day)
        hours.append(current_hour)
    
    # 确保所有列表长度一致
    iy = [2024] * time_steps
    imin = [0] * time_steps
    rain = [0] * time_steps
    
    umep_met = pd.DataFrame([], columns=columns)
    umep_met['#iy'] = iy
    umep_met['id'] = days
    umep_met['it'] = hours
    umep_met['imin'] = imin
    umep_met['rain'] = rain
    umep_met = umep_met.fillna(-999)
    
    return umep_met

try:
    # 加载所有变量数据，保留空间分辨率
    var_data = {}
    for var_name in var_names:
        var_path = os.path.join(case_path, f"{var_name}_{date}.npy")
        if os.path.exists(var_path):
            # 加载原始数据
            original_data = np.load(var_path)
            print(f"{var_name}原始数据形状: {original_data.shape}")
            
            # 如果数据形状是(1728, 1, 24)，尝试重塑为(72, 24, 24)
            if original_data.shape[0] == 1728 and original_data.shape[1] == 1:
                try:
                    # 1728 = 72 * 24，尝试重塑为(72, 24, 24)
                    reshaped_data = original_data.reshape(72, 24, 24)
                    print(f"{var_name}重塑后形状: {reshaped_data.shape}")
                    var_data[var_name] = reshaped_data
                except Exception as e:
                    print(f"重塑{var_name}数据时出错: {e}")
                    # 如果重塑失败，保留原始数据
                    var_data[var_name] = original_data
            else:
                var_data[var_name] = original_data
        else:
            print(f"警告: 变量文件 {var_path} 不存在")
    
    # 确保所有必要的变量都已加载
    if all(var_name in var_data for var_name in var_names):
        # 获取时间步数和网格大小
        if var_data['T2'].shape[0] == 72:
            # 如果已经重塑为(72, 24, 24)
            time_steps, nlat, nlon = var_data['T2'].shape
            print(f"时间步数: {time_steps}, 网格大小: {nlat}x{nlon}")
        else:
            # 如果仍然是原始形状(1728, 1, 24)
            print(f"警告: 数据未能重塑为(72, 24, 24)，使用原始形状: {var_data['T2'].shape}")
            # 设置为72个时间步
            time_steps = 72
            nlat = var_data['T2'].shape[1]
            nlon = var_data['T2'].shape[2]
        
        # 设置输出路径
        output_path = r'D:\ZJU\科研\pycode\data\wrf2umep'
        os.makedirs(output_path, exist_ok=True)
        
        # 为每个网格点生成UMEP格式的气象数据
        for i_lon in range(nlon):
            for i_lat in range(nlat):
                try:
                    # 初始化UMEP气象数据格式
                    umep_met = umep_met_init(time_steps)
                    
                    # 为每个变量赋值，保留空间分辨率
                    for var_name in var_names:
                        if var_data[var_name].shape[0] == 72:
                            # 如果数据已重塑为(72, 24, 24)
                            umep_met[var_dict[var_name]] = var_data[var_name][:, i_lat, i_lon]
                        else:
                            # 如果数据仍为原始形状(1728, 1, 24)，需要重采样
                            original_data = var_data[var_name][:, i_lat, i_lon]
                            # 每24个取1个，从1728降到72
                            resampled_data = original_data[::24]
                            
                            # 确保长度正确
                            if len(resampled_data) == time_steps:
                                umep_met[var_dict[var_name]] = resampled_data
                            else:
                                print(f"警告: 重采样后数据长度不正确 ({len(resampled_data)} != {time_steps})")
                                # 如果长度不正确，进行裁剪或填充
                                if len(resampled_data) > time_steps:
                                    umep_met[var_dict[var_name]] = resampled_data[:time_steps]
                                else:
                                    # 填充不足的部分
                                    padded_data = np.pad(resampled_data, (0, time_steps - len(resampled_data)), 'edge')
                                    umep_met[var_dict[var_name]] = padded_data
                    
                    # 保存为UMEP格式的文本文件
                    output_file = os.path.join(output_path, f"wrf2umep_{i_lon:02d}_{i_lat:02d}.txt")
                    umep_met.to_csv(output_file, index=None, sep=' ')
                    
                    if i_lon == 0 and i_lat == 0:
                        print(f"示例数据 (0, 0):")
                        print(umep_met.head())
                except Exception as e:
                    print(f"处理网格点 ({i_lon}, {i_lat}) 时出错: {e}")
                    continue
        
        print(f"已生成UMEP格式气象数据，保存在: {output_path}")
    else:
        missing_vars = [var_name for var_name in var_names if var_name not in var_data]
        print(f"警告: 以下变量数据缺失: {missing_vars}")
except Exception as e:
    print(f"生成UMEP格式气象数据时出错: {e}")

print("处理完成!")