import os
import shutil

root_src_dir = r'C:\Users\Davidk\Desktop\New folder\bne brak.gdb'
root_dst_dir = r'C:\Users\Davidk\Desktop\New folder (2)\bne brak.gdb'

for src_dir, dirs, files in os.walk(root_src_dir):
    dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for file_ in files:
        src_file = os.path.join(src_dir, file_)
        dst_file = os.path.join(dst_dir, file_)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        shutil.copy(src_file, dst_dir)



#replase gdb data
##root_src_dir = r'D:\Taibeh\Taibe.gdb'
##root_dst_dir = r'D:\gis_data\data\taibe\Taibe.gdb'

)
