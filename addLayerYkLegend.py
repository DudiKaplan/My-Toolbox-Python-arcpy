import arcpy,os

mxds = arcpy.GetParameterAsText(0).split(";")

lyrPath = arcpy.GetParameterAsText(1)

for mxdPath in mxds:

    mxd = arcpy.mapping.MapDocument(mxdPath)
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    lyrFile = arcpy.mapping.Layer(lyrPath)
    legend = arcpy.mapping.ListLayoutElements(mxd, "LEGEND_ELEMENT")[0]
    lyrers = arcpy.mapping.ListLayers(mxd)

    for lyr in lyrers:
        legend.removeItem(lyr)
        arcpy.mapping.RemoveLayer(df, lyr)

    arcpy.mapping.AddLayer(df, lyrFile, "TOP")
    lyr = arcpy.mapping.ListLayers(mxd)[0]
    legend.updateItem(lyr, "","", True)
    mxd.save()
    del mxd
