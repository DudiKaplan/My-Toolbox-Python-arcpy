import arcpy,os


Layers = arcpy.GetParameterAsText(0).split(";")


for fc in Layers:
    cont_list = [row for row in arcpy.da.SearchCursor(fc,"*")]
    if len(cont_list ) == 0:
        arcpy.Delete_management(fc.strip("'"))
        arcpy.AddMessage("{0}{1}".format(os.path.basename(fc.strip("'"))," - deleted"))

                                                





