import arcpy,os,shutil


def objectid (fc):

    num = 0
    fix = "yes"
    fields = arcpy.ListFields(fc)
    for field in fields:
        if "OBJECTID" == field.name:
            fix = "yes"
        if "OBJECTID" in field.name:
            num=num+1
	if "FID_" in field.name:
	    fix = "no"
	if "OID" in field.name:
	    fix = "no"

    if num == 1 and fix == "yes":
        return True
    else:
        return False


def objectidnom (fc):

    cursor = [row for row in arcpy.da.SearchCursor(fc,"*")]
    if cursor[0][0] == 1 or cursor[0][0]== 0:
        return True
    else:
        return False



newpath = r'C:\Repair_OBJECTID'
if not os.path.exists(newpath):
    os.makedirs(newpath)


Layers = arcpy.GetParameterAsText(0).split(";")

for Layer in Layers:

    delete_fields =[]
    new_fc = Layer.strip("'")
    BaseName = os.path.basename(new_fc)

    if objectid(new_fc) == True and objectidnom(new_fc) == True:
        arcpy.AddMessage("{0}{1}".format(BaseName.encode('utf-8')," - fix feature class "))
        continue
    

    new_name = BaseName + ".shp"
    Nativ = os.path.join(newpath,new_name)

    arcpy.FeatureClassToShapefile_conversion(new_fc,newpath)

    Fields = arcpy.ListFields(Nativ)
    for Field in Fields:
        if "OBJECTID" in Field.name:
            delete_fields.append(Field.name)
        if Field.type != "Geometry" and "Shape" in Field.name:
            delete_fields.append(Field.name)
        if "FID_" in Field.name:
            delete_fields.append(Field.name)
        if "OID" in Field.name:
            delete_fields.append(Field.name)

    if len(delete_fields) == 0:
        continue

    arcpy.DeleteField_management(Nativ,delete_fields)
    arcpy.Delete_management(new_fc)
    arcpy.FeatureClassToFeatureClass_conversion(Nativ,os.path.dirname(new_fc),BaseName)
    arcpy.AddMessage("{0}{1}".format(BaseName.encode('utf-8'), " - fix OBJECTID complete"))

shutil.rmtree(newpath)




