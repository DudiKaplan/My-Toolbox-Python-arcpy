import arcpy

mxd = arcpy.mapping.MapDocument(arcpy.GetParameterAsText(0))
m=""
isGroupLayer = " - isGroupLayer"
isBroken = " - isBroken"
spac = " - "
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isGroupLayer == True:
        arcpy.AddWarning("{0}{1}".format(lyr.name.encode('utf-8'),isGroupLayer)) 
        m = lyr.name
    if lyr.name == m:
        continue
    if lyr.isBroken == True:
        arcpy.AddError("{0}{1}".format(lyr.name.encode('utf-8'),isBroken)) 
    else:
        arcpy.AddMessage("{0}{1}{2}{3}{4}".format(lyr.name.encode('utf-8'),spac.encode('utf-8'),lyr.dataSource.encode('utf-8'),spac.encode('utf-8'),lyr.datasetName.encode('utf-8')))

del mxd




