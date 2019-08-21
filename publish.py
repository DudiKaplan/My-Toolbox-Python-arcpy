import arcpy,os,shutil


newpath = r'C:/Project'
if os.path.exists(newpath):
    mapDocdel = arcpy.mapping.MapDocument('c:\Project\Taibe_Main.mxd')
    del mapDocdel
    shutil.rmtree(newpath)


os.makedirs(newpath)


arcpy.Delete_management(r"D:\gis_data\mxd\taibe\Taibe_Main.mxd")
shutil.copyfile('D:\Taibeh\MXD\Taibe_Main.mxd',r"D:\gis_data\mxd\taibe\Taibe_Main.mxd")
shutil.copyfile('D:\Taibeh\MXD\Taibe_Main.mxd','C:\Project\Taibe_Main.mxd')


new_gdb = r'D:\Taibeh\Taibe.gdb'
old_gdb = r'D:\gis_data\data\taibe\Taibe.gdb'

arcpy.env.workspace = r'D:\gis_data\data\taibe\Taibe.gdb'

featureclasses = arcpy.ListFeatureClasses()

for fc in featureclasses:
    arcpy.Delete_management(fc)

arcpy.env.workspace = r'D:\Taibeh\Taibe.gdb'

featureclasses = arcpy.ListFeatureClasses()

for fc in featureclasses:
    arcpy.FeatureClassToFeatureClass_conversion(fc,old_gdb ,os.path.basename(fc))


 #define local variables
wrkspc = 'C:/Project/'
mapDoc = arcpy.mapping.MapDocument(wrkspc + 'Taibe_Main.mxd')
con = 'GIS Servers/arcgis on v5.gis-net.co.il (admin).ags' 
service = 'Taibe_Main'
sddraft = wrkspc + service + '.sddraft'
sd = wrkspc + service + '.sd'
summary = 'Population Density by County'
tags = 'county, counties, population, density, census'

 #create service definition draft
analysis = arcpy.mapping.CreateMapSDDraft(mapDoc, sddraft, service, 'ARCGIS_SERVER', 
                                          con, False, 'Taibe', summary, tags)

 #stage and upload the service if the sddraft analysis did not contain errors
if analysis['errors'] == {}:
    # Execute StageService
    arcpy.StageService_server(sddraft, sd)
    # Execute UploadServiceDefinition
    arcpy.UploadServiceDefinition_server(sd, con)
else: 
    # if the sddraft analysis contained errors, display them
    arcpy.AddMessage(analysis['errors'])

del mapDoc
del analysis
