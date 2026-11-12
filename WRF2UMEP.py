from netCDF4 import Dataset
from wrf import getvar, to_np
import numpy as np
import pandas as pd
import os
import glob
import datetime
from tqdm import tqdm

# 计算风速和风向
def calculate_wind_speed_dir(u10, v10):
    wspd = np.sqrt(u10**2 + v10**2)
    wdir = (270 - np.rad2deg(np.arctan2(v10, u10))) % 360
    return wspd, wdir

case_path = r'D:\ZJU\科研\pycode\data'
date = '20240801'
# 修改变量列表，只包含WRF输出文件中直接存在的变量
direct_vars = ['T2', 'PSFC', 'SWDOWN', 'GLW', 'Q2', 'U10', 'V10']
# 最终需要的变量
var_names = ['T2', 'rh2', 'wspd10', 'wdir10', 'SWDOWN', 'GLW', 'PSFC']
var_dict = {'wspd10':'Wind', 'rh2':'RH', 'T2':'Td', 'PSFC':'press', 'SWDOWN':'Kdn', 'GLW':'ldown', 'wdir10':'Wd'}

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
            # 使用netCDF4和wrf-python处理
            ncfile = Dataset(path)
            
            if var_name in ['T2', 'TSK']:
                field = to_np(getvar(ncfile, var_name) - 273.15)
            elif var_name == 'PSFC':
                field = to_np(getvar(ncfile, var_name) / 1000)  # Pa to kPa
            else:
                field = to_np(getvar(ncfile, var_name))
                
            if i == 0:
                ary = field
            else:
                ary = np.dstack((ary, field))
                
            i += 1
            ncfile.close()
        except Exception as e:
            print(f"处理文件 {path} 时出错: {e}")
            continue
    
    # 保存处理后的数据
    if i > 0:
        output_file = os.path.join(case_path, f"{var_name}_{date}.npy")
        np.save(output_file, np.array(ary.transpose(2, 0, 1)))
        print(f"已保存: {output_file}")

# 计算派生变量
# 1. 计算相对湿度 (rh2)
try:
    t2_data = np.load(os.path.join(case_path, f"T2_{date}.npy"))
    q2_data = np.load(os.path.join(case_path, f"Q2_{date}.npy"))
    psfc_data = np.load(os.path.join(case_path, f"PSFC_{date}.npy"))
    
    # 转换回K和Pa进行计算
    t2_k = t2_data + 273.15
    psfc_pa = psfc_data * 1000
    
    # 计算相对湿度
    rh_data = np.zeros_like(t2_data)
    for i in range(t2_data.shape[0]):
        # 简化计算，实际应使用更精确的公式
        t2c = t2_data[i] # 已经是摄氏度
        es = 6.112 * np.exp(17.67 * t2c / (t2c + 243.5))
        e = q2_data[i] * psfc_pa[i] / 100 / (0.622 + 0.378 * q2_data[i])
        rh_data[i] = 100.0 * e / es
        rh_data[i] = np.clip(rh_data[i], 0, 100)  # 限制在0-100%范围内
    
    np.save(os.path.join(case_path, f"rh2_{date}.npy"), rh_data)
    print(f"已保存: {os.path.join(case_path, f'rh2_{date}.npy')}")
except Exception as e:
    print(f"计算相对湿度时出错: {e}")

# 2. 计算风速和风向
try:
    u10_data = np.load(os.path.join(case_path, f"U10_{date}.npy"))
    v10_data = np.load(os.path.join(case_path, f"V10_{date}.npy"))
    
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
except Exception as e:
    print(f"计算风速风向时出错: {e}")


