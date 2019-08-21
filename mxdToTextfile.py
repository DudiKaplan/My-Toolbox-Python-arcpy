import arcpy, os, csv
CurrentMXD = arcpy.mapping.MapDocument("CURRENT")
f = open(arcpy.GetParameterAsText(0), "w")
f.write("IsPublic,LayerCode,IsDownload,LayerName,LayerGroupId,Scale,GeometryType,FastInfoGroupId,LayerGroupName,Type,IsSelectable,IsInternet,IsIdentify,IsFreeSearch,IsTree,LayerNameEnglish,IsBaseLayer\n")
#default values for for both types
LayerId = ""
IsPublic = "1"
IsSelectable = "1"
IsInternet = "1"
IsIdentify = "1"
IsBaseLayer = "1"
IsFreeSearch = "1"
IsTree = "1"
LayerNameEnglish = "FutureUse"

for Layer in arcpy.mapping.ListLayers(CurrentMXD):
    if Layer.isGroupLayer:
        LayerCode = Layer.description
        IsDownload = ""
        LayerName = Layer.name
        LayerGroupId = ""
        Scale = ""
        GeometryType = ""
        FastInfoGroupId = ""
        LayerGroupName = ""
        Type = "Group Layer"
        myString1 = IsPublic + "," + LayerCode + "," + IsDownload + "," + LayerName + "," + LayerGroupId + "," + Scale + "," + GeometryType + "," + FastInfoGroupId + "," + LayerGroupName + "," + Type + "," + IsSelectable + "," + IsInternet + "," + IsIdentify + "," + IsFreeSearch + "," + IsTree + "," + LayerNameEnglish + "," + IsBaseLayer + "\n"
        f.write(myString1.encode('utf-8'))
        LayerGroupId = Layer.description
        LayerGroupName = Layer.name
    elif Layer.isFeatureLayer:
        LayerCode = Layer.description
        IsDownload = "1"
        LayerName = Layer.name
        #LayerGroupId - gets it from above
        Scale = "FutureUse"
        GeometryType = "FutureUse"
        FastInfoGroupId = ""
        #LayerGroupName - gets it from above
        Type = "Feature Layer"
        myString2 = IsPublic + "," + LayerCode + "," + IsDownload + "," + LayerName + "," + LayerGroupId + "," + Scale + "," + GeometryType + "," + FastInfoGroupId + "," + LayerGroupName + "," + Type + "," + IsSelectable + "," + IsInternet + "," + IsIdentify + "," + IsFreeSearch + "," + IsTree + "," + LayerNameEnglish + "," + IsBaseLayer + "\n"
        f.write(myString2.encode('utf-8'))
    else:
        f.write("-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "," + "-808" + "\n")
f.close()
