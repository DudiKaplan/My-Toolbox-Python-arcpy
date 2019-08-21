import arcpy

mxd = arcpy.mapping.MapDocument("CURRENT")
m=""
isGroupLayer = " - isGroupLayer"
isBroken = " - isBroken"
spac = " - "
LayerName = []
for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.isGroupLayer == True:
        arcpy.AddWarning("{0}".format(lyr.name.encode('utf-8'))) 
        LayerName.append(lyr.name.encode('utf-8'))
        m = lyr.name
    if lyr.name == m:
        continue
    if lyr.isBroken == True:
        arcpy.AddError("{0}{1}".format(lyr.name.encode('utf-8'),isBroken)) 
    else:
        arcpy.AddWarning("{0}".format(lyr.name.encode('utf-8')))
        LayerName.append(lyr.name.encode('utf-8'))
del mxd
count = 0
for i in LayerName:
    for j in LayerName:
        if i == j:
            count = count + 1
    if count>1:
        arcpy.AddWarning("{0}{1}".format(str(count),i))
        count =0
        
        
        

