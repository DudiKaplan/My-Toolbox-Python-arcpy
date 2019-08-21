import arcpy, os

#Get map document object
CurrentMXD = arcpy.mapping.MapDocument("CURRENT")

#Enumerate groups and layers
x = 1000
y = 100

#Iterate through layers
for Layer in arcpy.mapping.ListLayers(CurrentMXD): 
    if Layer.isGroupLayer:
        Layer.description = x
        x+=1
    else:
        Layer.description = y
        y+=1
