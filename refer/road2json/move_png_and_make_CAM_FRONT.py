import os 
import shutil

def move_png_and_make_CAM_FRONT(old_dir):
    
    if os.path.isdir(old_dir + '\\CAM_FRONT') != True:
        os.mkdir(old_dir + '\\CAM_FRONT')

    file_list = os.listdir(old_dir)
    
    file_list = [tmp_file for tmp_file in file_list if tmp_file[-3:] == 'jpg']
    
    new_dir = old_dir + '\\CAM_FRONT'
    
    
    for tmp_file in file_list:
        shutil.move(old_dir + '\\' + tmp_file, new_dir + '\\' + tmp_file)
    
if __name__ == "__main__":
    from tqdm import tqdm
    total_list = os.listdir(r'J:\OP_SAMPLE_2\raw\차선_횡단보도_인지_영상_수도권')
    for test_num in tqdm(total_list):
        test_dir = r'J:\OP_SAMPLE_2\raw\차선_횡단보도_인지_영상_수도권\\' + test_num
        move_png_and_make_CAM_FRONT(test_dir)
    # test_dir = r'J:\OP_SAMPLE_2\raw\차선_횡단보도_인지_영상_수도권\001'
    
    # move_png_and_make_CAM_FRONT(test_dir)
    