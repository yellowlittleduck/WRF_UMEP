import os
from qgis import processing

wrf2umep_path = 'D:/ZJU/research1/pycode/data/wrf2umep'


for nlat in range(1,23):
    for nlon in range(1,23):

        Output_dir = f'D:/ZJU/research1/MRT/output/MRT/MRT_{nlon:02d}_{nlat:02d}'
        if not os.path.exists(Output_dir):
            os.mkdir(Output_dir)
        
        DEM_path =      f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_DEM_{nlon:02d}_{nlat:02d}.tif'     
        DSM_path =      f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_DSM_{nlon:02d}_{nlat:02d}.tif'
        Aspect_path =   f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_aspect_{nlon:02d}_{nlat:02d}.tif'
        Height_path =   f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_height_{nlon:02d}_{nlat:02d}.tif'
        LC_path =       'your_path_to_input_data/05UMEPLC/UMEPLC_%.2d_%.2d.tif' 
        CDSM_path =     f'D:/ZJU/research1/MRT/output/grid_tiles/hangzhou_CDSM_{nlon:02d}_{nlat:02d}.tif' 
        TDSM_path =     'your_path_to_input_data/06DSMs/tdsm_%.2d_%.2d.tif'
        SVF_path =      f'D:/ZJU/research1/MRT/output/grid_tiles/SVF/SVF_{nlon:02d}_{nlat:02d}/svfs.zip' 

        # 正确的方式（使用UMEP格式的文本文件）
        MET_path = os.path.join(wrf2umep_path, f'wrf2umep_{nlon:02d}_{nlat:02d}.txt')
        
        processing.run("umep:Outdoor Thermal Comfort: SOLWEIG",
        {'INPUT_DSM':DSM_path,
        'INPUT_SVF':SVF_path,
        'INPUT_HEIGHT':Height_path,
        'INPUT_ASPECT':Aspect_path,
        'INPUT_CDSM':CDSM_path,
        'TRANS_VEG':3,'LEAF_START':97,'LEAF_END':300,'CONIFER_TREES':False,
        'INPUT_TDSM':None,
        'INPUT_THEIGHT':25,
        'INPUT_LC':None,'USE_LC_BUILD':False,
        'INPUT_DEM':DEM_path,'SAVE_BUILD':False,'INPUT_ANISO':'','ALBEDO_WALLS':0.2,'ALBEDO_GROUND':0.15,'EMIS_WALLS':0.9,'EMIS_GROUND':0.95,'ABS_S':0.7,'ABS_L':0.95,'POSTURE':0,'CYL':True,
        'INPUTMET':MET_path,'ONLYGLOBAL':True,'UTC':8,
        'POI_FILE':None,'POI_FIELD':'','AGE':35,'ACTIVITY':80,'CLO':0.9,'WEIGHT':75,'HEIGHT':180,'SEX':0,'SENSOR_HEIGHT':10,'OUTPUT_TMRT':True,'OUTPUT_KDOWN':False,'OUTPUT_KUP':False,'OUTPUT_LDOWN':False,'OUTPUT_LUP':False,'OUTPUT_SH':False,'OUTPUT_TREEPLANTER':False,
        'OUTPUT_DIR':Output_dir})

        print(f"完成分块 [{nlat},{nlon}] 的SOLWEIG计算")
