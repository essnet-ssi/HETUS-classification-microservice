import pandas as pd

lang="EN" # TODO parameter into json file


def Init():
    global  DescrActivity,DescrGP2Activity_map,DescrOSM2tus_place_map,DescrLG,DescrGP2tus_place_map,DescrGP2TusPlace_map ,FreqTUS,TSTable
    
    # TODO file name into param file
    DescrLG=pd.read_csv("../TUS_Istat/TUS_PLACE_COD_"+lang+".csv",sep=";",dtype={"TUS_PLACE":"str"}).set_index("TUS_PLACE")["TUS_PLACE_DESCR_"+lang].to_dict()
    #print(DescrLG)
    
    #global DescrActivity
    # TODO file name into param file
    DescrActivity=pd.read_csv("../TUS_Istat/HETUS_ACTIVITY_COD_"+lang+".csv",sep=";").set_index("code").descr.to_dict()
    #print(DescrActivity)
    
    #global DescrGP2Activity_map
    DescrGP2Activity_map=pd.read_csv("../TUS_Istat/GP2HETUS_MAP.csv",sep=";").set_index("GOOGLE_PLACE").HETUS.to_dict()
    #print(PLACE2HETUS_dict_GP)
    
    #global DescrGP2tus_place_map
    DescrGP2TusPlace_map =pd.read_csv("../TUS_Istat/GP2TUS_PLACE_MAP.csv",sep=";",dtype="str").set_index("GOOGLE_PLACE").TUS_PLACE.to_dict()
    
    #global DescrOSM2tus_place_map
    DescrOSM2tus_place_map=pd.read_csv("../TUS_Istat/OSM2TUS_PLACE_MAP.csv",sep=";",dtype="str").set_index("OSM_TAG").TUS_PLACE.to_dict()    
    #print(DescrOSM2tus_place_map)

    FreqTUS=pd.read_csv("../TUS_Istat/Activity_Places_TUS_count2.csv",sep=";",dtype={"lg":str})

    TSTable=pd.read_csv("../TUS_Istat/data_by_tslot/Activity_Places_TUS_TIME_SLOT.csv",sep=";",dtype={"lg":str})

    print("Inizialize: DescrActivity,DescrGP2Activity_map,DescrOSM2tus_place_map,DescrLG,DescrGP2TusPlace_map, FreqTUS,TSTable... TABLES")
        