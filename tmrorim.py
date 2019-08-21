import arcpy,os,shutil

def delete_fields (fc_gdb):
    god_fields = ["FID","Shape","Layer","GAR_KEY","ToSYS","symbol_sig","ts_text"]
    delete_fields = []
    fields = arcpy.ListFields(fc_gdb)
    for field in fields:
        if field.name not in god_fields:
            delete_fields.append(field.name)
    arcpy.DeleteField_management(fc_gdb,delete_fields)
            


def calculate_link (fc):
    arcpy.AddField_management(fc, "ToSYS", "TEXT", "" , "", 255, "למערכת ניהול", "", "")
    arcpy.CalculateField_management(fc, "ToSYS", "\"http://handasa.complot.co.il/general/cartesettamrur.asp?itemcode=\"&[GAR_KEY]", "VB", "")
    

newpath = arcpy.GetParameterAsText(0)
if not os.path.exists(newpath):
    os.makedirs(newpath)

arcpy.CreateFileGDB_management(newpath,"tmrurim", "CURRENT")

dwg_east = arcpy.GetParameterAsText(1)
dwg_west = arcpy.GetParameterAsText(2)

TS_PT1 = arcpy.GetParameterAsText(3)
TS_LN1 = arcpy.GetParameterAsText(4)

fc = os.path.join(newpath,"tmrurim.gdb")

work_BaseName = ['Point','Polyline','Polygon']

for work in work_BaseName:
    arcpy.Merge_management([os.path.join(dwg_east,work),os.path.join(dwg_west,work)],os.path.join(fc,work+"_Merge"))
    arcpy.DeleteField_management(os.path.join(fc,work+"_Merge"),['Entity', 'Handle', 'LyrFrzn', 'LyrLock', 'LyrOn', 'LyrVPFrzn', 'LyrHandle', 'Color', 'EntColor', 'LyrColor', 'BlkColor', 'Linetype', 'EntLinetype', 'LyrLnType', 'BlkLinetype', 'Elevation', 'Thickness', 'LineWt', 'EntLineWt', 'LyrLineWt', 'BlkLineWt', 'LTScale', 'ExtX', 'ExtY', 'ExtZ', 'DocName', 'DocPath', 'DocType', 'DocVer','ROTATE'])


arcpy.JoinField_management(os.path.join(fc,"Polyline_Merge"), "GAR_KEY" ,TS_PT1,"GAR_KEY",["symbol_sig","ts_text"])

arcpy.Select_analysis(TS_PT1,os.path.join(fc,"T4202"), "\"LAYER\" = '4202'")

arcpy.Select_analysis(os.path.join(fc,"Point_Merge"),os.path.join(fc,"T4200"), "\"Layer\" = '4200'")
arcpy.Select_analysis(os.path.join(fc,"Polyline_Merge"),os.path.join(fc,"sings"), "Layer IN ( '4201', '4202')")
arcpy.Select_analysis(os.path.join(fc,"Polyline_Merge"),os.path.join(fc,"SingsR"), "Layer IN ( '4203', '4204' ,'4211','4217','4222','4230','4231','4232')")
arcpy.Select_analysis(TS_LN1,os.path.join(fc,"sings_append"),"Layer IN ('4205','4206','4207','4208','4209','4210','4213','4214','4215','4216','4218','4219','4221','4224','4225','4226','4427','4235','4250','4209_DOUBLE_NEW803')")
arcpy.Select_analysis(os.path.join(fc,"Polygon_Merge"),os.path.join(fc,"parking"), "RefName IN ('PARK_RECT_NACHE','PARK_RECT_BLUE', 'PARK_RECT_BLUE_OLD')")
arcpy.Select_analysis(os.path.join(fc,"Polygon_Merge"),os.path.join(fc,"T4226"),"\"Layer\" = '4226'")
arcpy.Select_analysis(os.path.join(fc,"Polyline_Merge"),os.path.join(fc,"tichnun_even_safa"),"\"Layer\" = 'tichnun_even_safa'")

arcpy.Append_management(os.path.join(fc,"sings_append"),os.path.join(fc,"SingsR"),"NO_TEST","","")


delete_fc = ['Point_Merge','Polyline_Merge','Polygon_Merge','sings_append']
arcpy.env.workspace = fc
featureclasses = arcpy.ListFeatureClasses()
for fc in featureclasses:
    if fc in delete_fc:
        arcpy.Delete_management(fc)
        arcpy.AddMessage(fc)
    else:
        arcpy.DefineProjection_management(fc, "PROJCS['Israel_TM_Grid',GEOGCS['GCS_Israel',DATUM['D_Israel',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',219529.584],PARAMETER['False_Northing',626907.39],PARAMETER['Central_Meridian',35.20451694444445],PARAMETER['Scale_Factor',1.0000067],PARAMETER['Latitude_Of_Origin',31.73439361111111],UNIT['Meter',1.0]]")
        calculate_link(fc) 
        arcpy.FeatureClassToShapefile_conversion(fc,newpath)


path = os.path.join(newpath,"tmrurim.gdb")
arcpy.Append_management(os.path.join(path,"sings"),os.path.join(path,"SingsR"),"NO_TEST","","")

delete_fc = ['T4202','SingsR']

for fc in featureclasses:
    if fc not in delete_fc:
        arcpy.Delete_management(fc)


delete_fields(os.path.join(newpath,"sings.shp"))
delete_fields(os.path.join(newpath,"SingsR.shp"))




