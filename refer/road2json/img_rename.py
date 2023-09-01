import os 
import glob
from natsort import natsorted
from tqdm import tqdm
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    
    for i in range(1,147):
        

        # target_dir = r'\\192.168.75.251\Shares\OpenPlatform\yh\2_DATA\3_FOT_CN7\CN7_030323_pcd\CN7_030323_' + str(i).zfill(3)
        target_dir = r'J:\OP_SAMPLE_2\raw\차선_횡단보도_인지_영상_수도권' + "\\" + str(i).zfill(3) +  '\\CAM_FRONT'
    # target_dir = r'\\192.168.75.251\Shares\OpenPlatform\yh\2_DATA\3_FOT_CN7\CN7_030323_image\CN7_030323_016'
        
        # os.listdir(target_dir)
        
        jpg_list = natsorted([file for file in os.listdir(target_dir) if file.endswith(".jpg")])
        
        for idx, tmp_file in tqdm(enumerate(jpg_list)):
            os.rename(target_dir + "\\" + tmp_file, target_dir + "\\" + "CAM_FRONT_" + str(idx) + ".jpg")
        
        # pcd_list = natsorted([file for file in os.listdir(target_dir) if file.endswith(".pcd")])
        # png_list = natsorted([file for file in os.listdir(target_dir) if file.endswith(".png")])
        # png_list2 = natsorted(glob.glob(target_dir + r"\*.png"))
        
        # for idx, tmp_file in tqdm(enumerate(pcd_list)):
        #     os.rename(target_dir + "\\" + tmp_file, target_dir + "\\" + "LIDAR_TOP_" + str(idx*2) + ".pcd")
            # os.rename(target_dir + "\\" + tmp_file, target_dir + "\\" + "LIDAR_TOP_" + str(idx) + ".png")
        
    
