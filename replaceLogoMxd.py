import arcpy

mxds = arcpy.GetParameterAsText(0).split(";")

logo = arcpy.GetParameterAsText(1)

for pathmxd in mxds:
    mxd = arcpy.mapping.MapDocument(pathmxd)
    for elm in arcpy.mapping.ListLayoutElements(mxd,"PICTURE_ELEMENT","*logo*"):
        if elm.name == "logo":
            elm.sourceImage = logo
        mxd.save()
    del mxd
