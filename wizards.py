import arcpy

shape = arcpy.GetParameterAsText(0)

output = arcpy.GetParameterAsText(1)





arcpy.ImportToolbox("C:/Program Files (x86)/ET SpatialTechniques/ET GeoWizards 11.0 for ArcGIS 10.2/ET GeoWizards.tbx")  
 

arcpy.ET_GPSortShapes (shape, output, "Shlav_Date")
