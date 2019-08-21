# -*- coding: cp1255 -*-
import arcpy,os,shutil

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def lots1 (lots1):

    add_fields = [["ToSite",254,"לאתר הנדסי"],["internet",254,"���� ��� ����"],["gush_txt",15,"���"],["helka_txt",10,"����"],["infopage",254,"��� ����"],["ToSYS",150,"������ �������"]]
    Calculate_Field = ["Gush","Helka"]
    for field in add_fields:
        arcpy.AddField_management(lots1, field[0], "TEXT", "", "", field[1], field[2], "NULLABLE", "NON_REQUIRED", "")
        Calculate_Field.append(field[0])
    with arcpy.da.UpdateCursor(lots1, Calculate_Field) as cursor:
        for row in cursor:
            row[2] = "http://handasi.complot.co.il/handasi2016/redirects/unf.htm?sid="+SiteID+"&g="+str(int(row[0]))+"&h="+str(int(row[1]))
            row[3] = "http://handasi.complot.co.il/handasi2016/Redirects/cgf.htm?sid="+SiteID+"&g="+str(int(row[0]))+"&h="+str(int(row[1]))
            row[4] = str(int(row[0]))
            row[5] = str(int(row[1]))
            row[6] = "http://handasi.complot.co.il/handasi2016/redirects/inf.htm?sid="+SiteID+"&g="+str(int(row[0]))+"&h="+str(int(row[1]))
            row[7] = "http://handasa.complot.co.il/general/"+aspfile+".asp?itemcode=10194,"+CityCode+","+str(int(row[0]))+","+str(int(row[1]))
            cursor.updateRow(row)
    
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def index (index):

    arcpy.AddField_management(index,"TbToSite", "TEXT", "", "", "254", "����� ���", "NULLABLE", "NON_REQUIRED", "")
    with arcpy.da.UpdateCursor(index,["Taba_Numer","TbToSite"]) as cursor:
        for row in cursor:
            row[1] = "http://handasi.complot.co.il/handasi2016/redirects/csf.htm?sid="+SiteID+"&n="+str(int(row[0]))
            cursor.updateRow(row)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            
def Cadaster (Cadaster):

    add_fields = [["ToSite",254,"���� �����"],["gush_txt",15,"���"],["helka_txt",10,"����"],["infopage",100,"��� ����"],["internet",100,"���� ��� ����"],["ToSYS",100,"������ �������"]]
    Calculate_Field = ["Gush","Helka"]
    for field in add_fields:
        arcpy.AddField_management(Cadaster, field[0], "TEXT", "", "", field[1], field[2], "NULLABLE", "NON_REQUIRED", "")
        Calculate_Field.append(field[0])
    with arcpy.da.UpdateCursor(Cadaster, Calculate_Field) as cursor:
        for row in cursor:
            row[2] = "http://handasi.complot.co.il/handasi2016/redirects/unf.htm?sid="+SiteID+"&g="+str(int(row[0]))+"&h="+str(int(row[1]))
            row[6] = "http://handasi.complot.co.il/handasi2016/Redirects/cgf.htm?sid="+SiteID+"&g="+str(int(row[0]))+"&h="+str(int(row[1]))
            row[3] = str(int(row[0]))
            row[4] = str(int(row[1]))
            row[5] = "http://handasi.complot.co.il/handasi2016/redirects/inf.htm?sid="+SiteID+"&g="+str(int(row[0]))+"&h="+str(int(row[1]))
            row[7] = "http://handasa.complot.co.il/general/"+aspfile+".asp?itemcode=10194,"+CityCode+","+str(int(row[0]))+","+str(int(row[1]))
            cursor.updateRow(row)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    

def compilation(fc):

    geomterySet = set()
    geomteryDic = {}
    geomteryList = []

    with arcpy.da.SearchCursor(fc,["SHAPE@","NUM"]) as cursor:
        for row in cursor:
            geomterySet.add(int(row[1]))
            
    geomteryList = list(geomterySet)

    
    tmp_dis = arcpy.Dissolve_management(in_features=fc,out_feature_class=r"in_memory\dis",dissolve_field="NUM")

    for geo in geomteryList:
        expression = u'NUM = {}'.format(geo)
        geomteryDic[geo] = [f[0] for f in arcpy.da.SearchCursor(tmp_dis, "SHAPE@" ,where_clause=expression)]

    for geo in geomteryList:
        for key in geomteryDic.keys():
            if (geo < key):
                shapeAllPlan = geomteryDic[key][0]
                if geomteryDic[geo][0] <> shapeAllPlan:
                    shapeD = shapeAllPlan.intersect(geomteryDic[geo][0],4)
                    if (shapeD.area/shapeAllPlan.area)> 0 :
                        expression = u'NUM = {}'.format(geo)
                        with arcpy.da.UpdateCursor(fc, "SHAPE@", where_clause=expression) as cursor:
                            for row in cursor:
                                if row[0] > 0: 
                                    shape = shapeAllPlan.intersect(row[0],4)
                                    if (shape.area/shapeAllPlan.area)> 0 :
                                        shape = row[0].difference(shapeAllPlan)
                                        row[0] = shape
                                        cursor.updateRow(row)

        arcpy.AddMessage("NUM = {} is complote".format(str(geo)))
                        
    
    arcpy.Delete_management("in_memory\dis")

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def addLinks(fc):

    Layer = "Layer"
    arcpy.AddField_management(fc, "Gush_Helka", "TEXT", "", "", "100", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "ToSys", "TEXT", "", "", "200", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(fc, "ToSys", "\"http://handasi.complot.co.il/general/\" & \"{}\" & \".asp?itemcode=10194,\" & \"{}\" & \",\"&[Gush]&\",\"&[Helka]".format(aspfile,SiteID), "VB", "")
    arcpy.AddField_management(fc, "gush_txt", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "helka_txt", "TEXT", "", "", "10", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(fc, "gush_txt", "[Gush]", "VB", "")
    arcpy.CalculateField_management(fc, "helka_txt", "[Helka]", "VB", "")
    arcpy.AddField_management(fc, "taba", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(fc, "infopage", "TEXT", "", "", "150", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(fc, "infopage", "\"http://handasi.complot.co.il/handasi2016/redirects/inf.htm?sid=\" & \"{}\" & \"&g=\" &[Gush] & \"&h=\" & [Helka]".format(SiteID), "VB", "")
    arcpy.CalculateField_management(fc, "taba", "\"http://handasi.complot.co.il/handasi2016/redirects/csf.htm?sid=\" & \"{}\" & \"&n=\" & [Numerator]".format(SiteID), "VB", "")

    arcpy.MakeFeatureLayer_management(fc, Layer)
    arcpy.SelectLayerByAttribute_management(Layer, "NEW_SELECTION",  u"\"SingleOrig\" = 'כן'")
    arcpy.CalculateField_management(Layer, "Gush_Helka", "[OriginGush] & \",\" & [OriginHelk]", "VB", "")
    arcpy.SelectLayerByAttribute_management(Layer, "NEW_SELECTION",  u"\"SingleOrig\" = 'לא'")
    arcpy.CalculateField_management(Layer, "Gush_Helka", "\"http://handasi.complot.co.il/handasi2016/Redirects/cgf.htm?sid=\" & \"{}\" & \"&g=\" &[Gush] & \"&h=\" & [Helka]".format(SiteID), "VB", "")


#----------------------------------------------------------------------------------------------------------------------------------------------------

shapefils = arcpy.GetParameterAsText(0).split(";")

CityCode = arcpy.GetParameterAsText(1)

ci1 = arcpy.GetParameterAsText(2)

SiteID = arcpy.GetParameterAsText(3)

aspfile = arcpy.GetParameterAsText(4)

data = arcpy.GetParameterAsText(5)

ShitaHadasha = arcpy.GetParameterAsText(6)

newpath = r'C:\kovezh_ironi'
if not os.path.exists(newpath):
    os.makedirs(newpath)

arcpy.CreateFileGDB_management(newpath,"ironi", "CURRENT")
gdb = os.path.join(newpath,"ironi.gdb")

shapsfils_for_Geodatabase = []
FeatureClasses_for_Geodatabase = []


for shape in shapefils:

    new_shape = shape.strip("'")
    shapsfils_for_Geodatabase.append(new_shape)
    arcpy.DefineProjection_management(new_shape, "PROJCS['Israel_TM_Grid',GEOGCS['GCS_Israel',DATUM['D_Israel',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',219529.584],PARAMETER['False_Northing',626907.39],PARAMETER['Central_Meridian',35.20451694444445],PARAMETER['Scale_Factor',1.0000067],PARAMETER['Latitude_Of_Origin',31.73439361111111],UNIT['Meter',1.0]]")
    BaseName = os.path.basename(new_shape.replace(".shp",""))

    if BaseName == "Plan_MigMP" and ShitaHadasha:

        tmpSelectFc = arcpy.Select_analysis(new_shape, r"in_memory\SelectFc", "\"ShowUpper\" =1 OR \"IsUpper\" =1")

        arcpy.AddField_management(tmpSelectFc, "ShlavDate", "DATE")
        arcpy.AddField_management(tmpSelectFc, "NUM", "SHORT")
        arcpy.CalculateField_management(tmpSelectFc, "ShlavDate", "[Shlav_Date]", "VB", "")

        tmpSortFc =  arcpy.Sort_management(tmpSelectFc, r"in_memory\SortFc", [["ShlavDate", "ASCENDING"]])

        NUM = 0
        TOCHNIT = "NULL"
        with arcpy.da.UpdateCursor(tmpSortFc,["TOCHNIT", "NUM"]) as cursor:
            for row in cursor:
                if TOCHNIT <> row[0]:
                    NUM = NUM + 1 
                    TOCHNIT = row[0]
                    row[1] = NUM
                else:
                    row[1] = NUM
                cursor.updateRow(row)

        tmpShowUpperFc = arcpy.Select_analysis(tmpSortFc, r"in_memory\ShowUpperFc", "\"ShowUpper\" =1")
        compilation(tmpShowUpperFc)
        arcpy.CalculateField_management(tmpShowUpperFc, "NUM", "{}".format(NUM + 1) , "VB", "")


        tmpIsUpperFc = arcpy.Select_analysis(tmpSortFc, r"in_memory\IsUpperFc", "\"ShowUpper\" =0")

        arcpy.Append_management(tmpShowUpperFc, tmpIsUpperFc , "TEST")
        compilation(tmpIsUpperFc)

        arcpy.Delete_management(new_shape)
        arcpy.Select_analysis(tmpIsUpperFc,new_shape)  


        arcpy.Delete_management(tmpSelectFc)
        arcpy.Delete_management(tmpSortFc)
        arcpy.Delete_management(tmpShowUpperFc)
        arcpy.Delete_management(tmpIsUpperFc)

        addLinks(new_shape)
        arcpy.DeleteField_management(new_shape, ["Shlav_Date","NUM"])
        arcpy.RepairGeometry_management(new_shape)



    FeatureClasses_for_Geodatabase.append(os.path.join(gdb,BaseName))
    arcpy.AddMessage(BaseName)
    arcpy.Delete_management(os.path.join(data,BaseName))


arcpy.FeatureClassToGeodatabase_conversion(shapsfils_for_Geodatabase,gdb)



for fc in FeatureClasses_for_Geodatabase:

    BaseName = os.path.basename(fc)
    
    if "lots" in BaseName:
        lots1(fc)
        arcpy.FeatureClassToFeatureClass_conversion(fc,data,BaseName)
    elif "index" in BaseName :
        index(fc)
        arcpy.FeatureClassToFeatureClass_conversion(fc,data,BaseName)
    elif "cadaster" in BaseName:
        Cadaster(fc)
        arcpy.FeatureClassToFeatureClass_conversion(fc,data,BaseName)
    else:
        arcpy.FeatureClassToFeatureClass_conversion(fc,data,BaseName)

      

shutil.rmtree(newpath)
