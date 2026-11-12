# from qgis import processing
# from qgis.core import QgsProcessing, QgsProject
# import os


# # 设置输入文件路径
# for nlat in range(1, 23):
#     for nlon in range(1, 23):
#         # 使用正斜杠而不是反斜杠，并使用f-string正确格式化
#         input_dsm = f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_DSM_{nlon:02d}_{nlat:02d}.tif'
#         input_cdsm = f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_CDSM_{nlon:02d}_{nlat:02d}.tif'

#         # 设置输出文件路径
#         output_dir = 'D:/ZJU/research1/MRT/output/grid_tiles'
#         output_file = os.path.join(output_dir, f'hangzhou_SVF_{nlon:02d}_{nlat:02d}.zip')

#         # 设置SVF计算参数
#         params = {
#             'INPUT_DSM': input_dsm,
#             'INPUT_CDSM': input_cdsm,
#             'TRANS_VEG': 3,  # 植被透过率
#             'INPUT_TDSM': None,  # 树木DSM（可选）
#             'INPUT_THEIGHT': 25,  # 树木高度
#             'ANISO': True,  # 是否考虑各向异性
#             'OUTPUT_DIR': output_dir,
#             'OUTPUT_FILE': output_file,
#             # 分块处理参数
#             'TILE_SIZE': 60,  # 分块大小（像素）
#             'OVERLAP': 5,  # 重叠区域大小（像素）
#             'RESAMPLE': True,  # 启用重采样
#             'RESOLUTION': 10,  # 设置为10m分辨率
#         }

#         # 设置分块处理上下文
#         context = QgsProcessingContext()
#         context.setProject(QgsProject.instance())

#         # 运行UMEP Sky View Factor计算（分块处理）
#         result = processing.runAndLoadResults("umep:Urban Geometry: Sky View Factor", 
#                                             params,
#                                             context=context)
        
#         # 确保输出目录存在
#         if not os.path.exists(output_dir):
#             os.makedirs(output_dir)



#         # 设置分块处理上下文
#         context = QgsProcessingContext()
#         context.setProject(QgsProject.instance())




from qgis import processing
from qgis.core import QgsProcessing, QgsProject
from osgeo import gdal

#设置输入文件路径
for i in range(0, 50111):
    # 使用正斜杠而不是反斜杠，并使用f-string正确格式化
    input_dsm = f'E:/research2/DSM/grid_{i}.tif'
    input_cdsm = f'E:/research2/CDSM/grid_{i}.tif'

    # 使用QGIS中复制出来的代码格式，但修改输入和输出路径
    processing.run("umep:Urban Geometry: Sky View Factor", {
        'INPUT_DSM': input_dsm,
        'INPUT_CDSM': input_cdsm,
        'TRANS_VEG': 3,
        'INPUT_TDSM': None,
        'INPUT_THEIGHT': 25,
        'ANISO': True,
        'OUTPUT_FILE': f'E:/research2/SVF/SVF_{i}.tif'
    })
    print(f"完成分块 [{i}] 的SVF计算")
            




#             # 检查输出文件是否存在
#             if not os.path.exists(temp_output_file):
#                 print(f"警告: 网格 [{nlon},{nlat}] 的SVF计算可能失败，输出文件不存在")
#                 continue
                
#             # 创建SOLWEIG所需的ZIP文件
#             print(f"为网格 [{nlon},{nlat}] 创建SOLWEIG格式的ZIP文件...")
            
#             # 创建临时目录用于存放ZIP文件内容
#             zip_temp_dir = tempfile.mkdtemp()
            
#             try:
#                 # 1. 复制SVF TIF文件到临时目录，并重命名为SOLWEIG期望的文件名
#                 svf_file = os.path.join(zip_temp_dir, 'svf.tif')
#                 shutil.copy(temp_output_file, svf_file)
                
#                 # 2. 读取SVF文件获取地理信息
#                 ds = gdal.Open(temp_output_file)
#                 width = ds.RasterXSize
#                 height = ds.RasterYSize
#                 geotransform = ds.GetGeoTransform()
#                 projection = ds.GetProjection()
#                 ds = None
                
#                 # 3. 创建墙面可见度因子文件
#                 wvf_file = os.path.join(zip_temp_dir, 'wallvf.tif')
#                 driver = gdal.GetDriverByName('GTiff')
#                 wvf_ds = driver.Create(wvf_file, width, height, 1, gdal.GDT_Float32)
#                 wvf_ds.SetGeoTransform(geotransform)
#                 wvf_ds.SetProjection(projection)
#                 wvf_band = wvf_ds.GetRasterBand(1)
#                 wvf_band.Fill(0)  # 填充0值
#                 wvf_ds = None
                
#                 # 4. 创建高度文件
#                 height_file = os.path.join(zip_temp_dir, 'height.tif')
#                 height_ds = driver.Create(height_file, width, height, 1, gdal.GDT_Float32)
#                 height_ds.SetGeoTransform(geotransform)
#                 height_ds.SetProjection(projection)
#                 height_band = height_ds.GetRasterBand(1)
#                 height_band.Fill(0)  # 填充0值
#                 height_ds = None
                
#                 # 5. 创建ZIP文件
#                 with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
#                     zipf.write(svf_file, os.path.basename(svf_file))
#                     zipf.write(wvf_file, os.path.basename(wvf_file))
#                     zipf.write(height_file, os.path.basename(height_file))
                
#                 print(f"网格 [{nlon},{nlat}] 的SOLWEIG格式ZIP文件创建成功: {output_zip}")
            
#             finally:
#                 # 清理临时目录
#                 shutil.rmtree(zip_temp_dir)
                
#         except Exception as e:
#             print(f"处理网格 [{nlon},{nlat}] 时出错: {str(e)}")
#             continue

# print("所有网格的SVF计算和ZIP文件创建完成！")

# import numpy as np
# from qgis import processing
# from qgis.core import QgsProcessing, QgsProject
# from osgeo import gdal
# import os
# import zipfile
# import tempfile
# import shutil

# # 设置输入文件路径
# input_dsm = 'D:/ZJU/科研/MRT/hangzhou_D&B_mask_16bit_0.tif'
# input_cdsm = 'D:/ZJU/科研/MRT/hangzhou_tree_mask_32bit_000.tif'

# # 设置输出文件路径
# output_dir = 'D:/ZJU/科研/MRT/output'
# output_tif = os.path.join(output_dir, 'hangzhou_svf_10m.tif')
# output_zip = os.path.join(output_dir, 'hangzhou_svf_10m.zip')  # 新增ZIP输出路径

# # 确保输出目录存在
# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# # 读取原始DSM获取尺寸信息
# dsm_dataset = gdal.Open(input_dsm)
# width = dsm_dataset.RasterXSize
# height = dsm_dataset.RasterYSize
# geotransform = dsm_dataset.GetGeoTransform()
# projection = dsm_dataset.GetProjection()
# dsm_dataset = None  # 释放资源

# print(f"原始DSM尺寸: {width}x{height}像素")

# # 分块参数
# tile_size = 100
# overlap = 20

# # 计算分块数量
# num_tiles_x = int(np.ceil(width / (tile_size - overlap)))
# num_tiles_y = int(np.ceil(height / (tile_size - overlap)))

# print(f"将分成 {num_tiles_x}x{num_tiles_y} 个分块进行处理")

# # 创建临时输出目录
# temp_output_dir = os.path.join(output_dir, 'temp_tiles')
# if not os.path.exists(temp_output_dir):
#     os.makedirs(temp_output_dir)

# # 分块处理
# tile_outputs = []
# for i in range(num_tiles_x):
#     for j in range(num_tiles_y):
#         # 计算当前块的范围
#         x_min = max(0, i * (tile_size - overlap))
#         y_min = max(0, j * (tile_size - overlap))
#         x_max = min(width, x_min + tile_size)
#         y_max = min(height, y_min + tile_size)
        
#         print(f"处理分块 [{i},{j}]: 像素范围 ({x_min},{y_min}) 到 ({x_max},{y_max})")
        
#         # 裁剪DSM和CDSM
#         tile_dsm = os.path.join(temp_output_dir, f'dsm_tile_{i}_{j}.tif')
#         tile_cdsm = os.path.join(temp_output_dir, f'cdsm_tile_{i}_{j}.tif')
        
#         # 使用GDAL裁剪栅格
#         # 注意：GDAL的projWin参数需要地理坐标，而不是像素坐标
#         # 计算地理坐标
#         ulx = geotransform[0] + x_min * geotransform[1]
#         uly = geotransform[3] + y_min * geotransform[5]
#         lrx = geotransform[0] + x_max * geotransform[1]
#         lry = geotransform[3] + y_max * geotransform[5]
        
#         gdal.Translate(tile_dsm, input_dsm, projWin=[ulx, uly, lrx, lry])
#         gdal.Translate(tile_cdsm, input_cdsm, projWin=[ulx, uly, lrx, lry])
        
#         # 为每个分块计算SVF
#         tile_output = os.path.join(temp_output_dir, f'svf_tile_{i}_{j}.tif')
#         tile_params = {
#             'INPUT_DSM': tile_dsm,
#             'INPUT_CDSM': tile_cdsm,
#             'TRANS_VEG': 3,
#             'INPUT_TDSM': None,
#             'INPUT_THEIGHT': 25,
#             'ANISO': True,
#             'OUTPUT_DIR': temp_output_dir,
#             'OUTPUT_FILE': tile_output
#         }
        
#         # 设置分块处理上下文
#         context = QgsProcessingContext()
#         context.setProject(QgsProject.instance())
        
#         # 运行SVF计算
#         try:
#             processing.run("umep:Urban Geometry: Sky View Factor", tile_params, context=context)
#             tile_outputs.append(tile_output)
#             print(f"完成分块 [{i},{j}] 的SVF计算")
#         except Exception as e:
#             print(f"处理分块 [{i},{j}] 时出错: {str(e)}")
#             continue

# # 最后合并所有分块结果
# if len(tile_outputs) > 0:
#     print(f"开始合并 {len(tile_outputs)} 个分块结果...")
    
#     # 创建VRT虚拟栅格
#     vrt_file = os.path.join(temp_output_dir, 'svf_mosaic.vrt')
#     vrt_options = gdal.BuildVRTOptions(resampleAlg='bilinear', addAlpha=False)
#     gdal.BuildVRT(vrt_file, tile_outputs, options=vrt_options)
    
#     # 从VRT生成最终输出
#     gdal.Translate(output_tif, vrt_file, format='GTiff', 
#                   creationOptions=['COMPRESS=LZW', 'TILED=YES', 'BIGTIFF=YES','NBITS=16'])
    
#     print(f"SVF分块计算和合并完成！TIF输出文件保存在: {output_tif}")
    
#     # 创建SOLWEIG所需的ZIP文件
#     print("正在创建SOLWEIG格式的ZIP文件...")
    
#     # 创建临时目录用于存放ZIP文件内容
#     zip_temp_dir = tempfile.mkdtemp()
    
#     try:
#         # 1. 复制SVF TIF文件到临时目录，并重命名为SOLWEIG期望的文件名
#         svf_file = os.path.join(zip_temp_dir, 'svf.tif')
#         shutil.copy(output_tif, svf_file)
        
#         # 2. 创建墙面可见度因子文件（如果有的话，否则创建一个空的）
#         # 注意：这里我们创建一个与SVF相同大小的空墙面可见度因子文件
#         # 实际应用中，你可能需要计算真实的墙面可见度因子
#         ds = gdal.Open(output_tif)
#         width = ds.RasterXSize
#         height = ds.RasterYSize
#         geotransform = ds.GetGeoTransform()
#         projection = ds.GetProjection()
#         ds = None
        
#         # 创建墙面可见度因子文件
#         wvf_file = os.path.join(zip_temp_dir, 'wallvf.tif')
#         driver = gdal.GetDriverByName('GTiff')
#         wvf_ds = driver.Create(wvf_file, width, height, 1, gdal.GDT_Float32)
#         wvf_ds.SetGeoTransform(geotransform)
#         wvf_ds.SetProjection(projection)
#         wvf_band = wvf_ds.GetRasterBand(1)
#         wvf_band.Fill(0)  # 填充0值
#         wvf_ds = None
        
#         # 3. 创建高度和高宽比文件（如果需要）
#         height_file = os.path.join(zip_temp_dir, 'height.tif')
#         driver = gdal.GetDriverByName('GTiff')
#         height_ds = driver.Create(height_file, width, height, 1, gdal.GDT_Float32)
#         height_ds.SetGeoTransform(geotransform)
#         height_ds.SetProjection(projection)
#         height_band = height_ds.GetRasterBand(1)
#         height_band.Fill(0)  # 填充0值
#         height_ds = None
        
#         # 4. 创建ZIP文件
#         with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
#             zipf.write(svf_file, os.path.basename(svf_file))
#             zipf.write(wvf_file, os.path.basename(wvf_file))
#             zipf.write(height_file, os.path.basename(height_file))
        
#         print(f"SOLWEIG格式的ZIP文件创建成功！保存在: {output_zip}")
    
#     finally:
#         # 清理临时目录
#         shutil.rmtree(zip_temp_dir)
# else:
#     print("没有成功处理的分块，无法合并结果")

# # 可选：清理临时文件
# import shutil
# shutil.rmtree(temp_output_dir)

