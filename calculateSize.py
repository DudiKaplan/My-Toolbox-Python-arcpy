import os,arcpy
def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
            
    return total_size

GB = 1073741824
MB = 1048576
KB = 1024

path = r"D:\arcgisserver\directories\arcgiscache"
for folder in os.listdir(path):
    size = get_size(os.path.join(path,folder))



    if size >= GB:
        size_gb = size / GB
        if size_gb <= 10:
            arcpy.AddMessage("{0}{1}{2}{3}".format(folder," - ",str(size_gb)," GB"))
        if size_gb > 10 and size_gb < 20:
            arcpy.AddWarning("{0}{1}{2}{3}".format(folder," - ",str(size_gb)," GB"))
        if size_gb >= 20:
            arcpy.AddError("{0}{1}{2}{3}".format(folder," - ",str(size_gb)," GB"))

    if size < GB and size >= MB:
        arcpy.AddMessage("{0}{1}{2}{3}".format(folder," - ",str(size/MB)," MB"))

    if size < MB :
        arcpy.AddMessage("{0}{1}{2}{3}".format(folder," - ",str(size/KB)," KB"))
        
        
            
            





