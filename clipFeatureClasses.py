import arcpy


gdb = arcpy.GetParameterAsText(0)
poly = arcpy.GetParameterAsText(1)

arcpy.env.workspace = gdb

featureclasses = arcpy.ListFeatureClasses()

polyLayer = 'polyLayer'

arcpy.MakeFeatureLayer_management(poly,polyLayer)


for fc in featureclasses:
    fcLayer = 'fcLayer'
    arcpy.MakeFeatureLayer_management(fc,fcLayer)
    arcpy.SelectLayerByLocation_management(fcLayer, 'intersect', 'polyLayer')
    arcpy.SelectLayerByAttribute_management(fcLayer,'SWITCH_SELECTION')
    if int(arcpy.GetCount_management(fcLayer).getOutput(0)) > 0:
        arcpy.DeleteFeatures_management(fcLayer)

