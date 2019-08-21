import arcpy, os, csv

def name_type(name_type):

    if name_type == "Double" or name_type == "Integer" or name_type == "SmallInteger" or name_type == "Raster":
        new_name_type = "number"
    elif name_type == "String":
        new_name_type = "String"
    else:
        return name_type
    return new_name_type

    
CurrentMXD = arcpy.mapping.MapDocument("CURRENT")
f = open(arcpy.GetParameterAsText(0), "w")
f.write("LayerCode,Field,Type,MaxLength\n")


for Layer in arcpy.mapping.ListLayers(CurrentMXD):
    if Layer.isGroupLayer:
        continue

    if Layer.isFeatureLayer:
        
        list_fields = arcpy.ListFields(Layer)

        for field in list_fields:

            if "OBJECTID" in field.name or "OID" in field.name or "Shape" in field.name or "SHAPE" in field.name or "AREA" in field.name:
                continue

            LayerCode = str(Layer.description)
            Field = field.name
            Type = name_type(field.type)
            MaxLength = str(field.length)

            myString = LayerCode + "," + Field + "," + Type + "," + MaxLength +"\n"
            f.write(myString)



f.close()

0505235704

