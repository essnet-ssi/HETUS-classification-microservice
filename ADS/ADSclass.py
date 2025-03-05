import pandas as pd
import importlib
import folium
import numpy as np
import json
from geopy.distance import geodesic,great_circle
from matplotlib import pyplot as plt
from scipy.stats import norm,lognorm
from kneed import KneeLocator
import os

# custom libs
import scorePOI_X

import TimeSlotFromStop
import FilterPOI
import TablesMapping 
import Parameters
import json_in

from datetime import timedelta

importlib.reload(scorePOI_X)

importlib.reload(TimeSlotFromStop)
importlib.reload(FilterPOI)
importlib.reload(TablesMapping)
importlib.reload(Parameters)
importlib.reload(json_in)

#pd.set_option('display.max_colwidth', None)
np.seterr(all='ignore')
import warnings  
warnings.filterwarnings('ignore')#, category=pd.core.common.SettingWithCopyWarning)

class ADS:

    Parameters.Load()
    TablesMapping.Init()


    UseTUSdata= Parameters.UseTUSdata # if True use probabilistic aprroach
    DURATION_MODE=Parameters.DURATION_MODE
    TIMESLOT=Parameters.TIMESLOT

    poi_nActivitiesPredicted = 10 # number of activities predicted for each poi    

    if Parameters.UseUserProfileInfo==True:
        profileVar="ageclass-condiction-place"
    else :
        profileVar="place"

    if UseTUSdata==True:
        #def createStaticTable(self,profileVar): 
        df_eta=TablesMapping.FreqTUS
        #df_eta=self.df_eta
        ###########################################################
        P_Ai=df_eta[["catpri18","COUNT"]].groupby("catpri18").sum()
        P_Ai=P_Ai/P_Ai.sum()
        #self.P_Ai=P_Ai
        ############################################################
        
        def statsDuration(x): 
            tot=(x.COUNT).sum()    
            DURM=x["DURM"]
            SD=x["SD"]
            m=(pd.to_timedelta(DURM)).dt.total_seconds()
            sd=(pd.to_timedelta(SD)).dt.total_seconds()            
            P=x.COUNT/tot    
            mu=(m * P).sum()
            C=(x.COUNT).sum()
            var=( sd**2 * P ).sum() + ( P * (m-mu)**2 ).sum()
            mu =str(pd.to_timedelta(mu,unit='s')).split("days ")[-1]
            sd =(str(pd.to_timedelta(var**0.5,unit='s')).split("days ")[-1])            
            return pd.DataFrame({"COUNT":[C],"DURM":[mu],"SD":[sd]})
    
        if profileVar=="ageclass-condiction-place":            
            df_eta=df_eta
        if profileVar=="ageclass-place":            
            df_eta=df_eta.groupby(["etac","lg","catpri18"])[["COUNT","DURM","SD"]].apply(statsDuration).reset_index()
        if profileVar=="cond-place": 
            df_eta=df_eta.groupby(["cond","lg","catpri18"])[["COUNT","DURM","SD"]].apply(statsDuration).reset_index()
            df_eta=df_eta.drop("level_2",axis=1)
        if profileVar=="place": 
            df_eta=df_eta.groupby(["lg","catpri18"])[["COUNT","DURM","SD"]].apply(statsDuration).reset_index()
            df_eta=df_eta.drop("level_2",axis=1)
    
        
        df_Ai_list=[]
        for Ai in df_eta.catpri18.unique():
            
            if profileVar=="ageclass-condiction-place":
                df_Ai=df_eta[df_eta.catpri18==Ai].copy()
                df_Ai["P_X"]=(df_Ai.COUNT/df_Ai.COUNT.sum())
                df_Ai_list.append(df_Ai[["cond","etac","lg","catpri18","P_X"]])
    
            if profileVar=="condiction-place":
                df_Ai=df_eta[df_eta.catpri18==Ai].copy()
                df_Ai=df_Ai.groupby(["cond","lg","catpri18"])[["COUNT"]].sum().reset_index()               
                df_Ai["P_X"]=(df_Ai.COUNT/df_Ai.COUNT.sum())
                df_Ai_list.append(df_Ai[["cond","lg","catpri18","P_X"]])            
            
            if profileVar=="ageclass-place":
                df_Ai=df_eta[df_eta.catpri18==Ai].copy()
                df_Ai=df_Ai.groupby(["etac","lg","catpri18"])[["COUNT"]].sum().reset_index()               
                df_Ai["P_X"]=(df_Ai.COUNT/df_Ai.COUNT.sum())
                df_Ai_list.append(df_Ai[["etac","lg","catpri18","P_X"]])
    
            if profileVar=="place":
                df_Ai=df_eta[df_eta.catpri18==Ai].copy()
                df_Ai=df_Ai.groupby(["lg","catpri18"])[["COUNT"]].sum().reset_index()               
                df_Ai["P_X"]=(df_Ai.COUNT/df_Ai.COUNT.sum())
                df_Ai_list.append(df_Ai[["lg","catpri18","P_X"]])
                
                
        df_X_dato_Ai=pd.concat(df_Ai_list,axis=0)
        
        #self.df_X_dato_Ai=df_X_dato_Ai
        #self.profileVar=profileVar
        
        ############################################################




    #self.createStaticTable("ageclass-condiction-place")

    
    def predict(self, json_file):
        if ADS.UseTUSdata==True:
            df_X_dato_Ai=self.df_X_dato_Ai
            P_Ai=self.P_Ai        
            df_eta=self.df_eta
            profileVar=self.profileVar
        
        json_in.Read(json_file)
        gps=json_in.gps
        pois=json_in.pois
        stop=json_in.stop.loc[0]
        profile=json_in.profile
        codFascia=TimeSlotFromStop.getTimeSlotFromStop(stop)

        
        # Filter on user velocity GPS POINTS
        print("N points before gps filter:",len(gps))
        gps=(gps[gps.Speed<=Parameters.UserSpeedMax]).copy()
        gps=(gps[gps.Accuracy<=Parameters.AccuracyRadiusGPSMin]).copy() 
        print("N points after gps filter:",len(gps))
        
        if len(gps)==0:
            ActivityScore=pd.DataFrame(columns=["HETUS","ActivityScore","lg","Descr","StopRadius","MapServicePoisNumber","TAG_NOT_FOUND"])    
            print("NO GPS_POINTS AFTER SPEED & ACCURACY FILTER :")
            print("ACTIVITY SCORE EMPTY")
            return ActivityScore

        
        #######################################################
        # ASSIGN A TUS PLACE TO POINTS OF INTEREST
        # ASSIGN A DIRECT HETUS TO POINTS OF INTEREST
        def TagMatch(x):
            for key in DictTagMacth.keys():        
                if key.strip() in x:
                    return DictTagMacth[key]        
            return "not found"    
        if Parameters.mapService=="OSM":
            DictTagMacth=TablesMapping.DescrOSM2Activity_map
            pois["DIRECT_HETUS"]=pois.tag.apply(TagMatch) 
            DictTagMacth=TablesMapping.DescrOSM2TusPlace_map
            pois["TUS_PLACE"]=pois.tag.apply(TagMatch)            
        if Parameters.mapService=="GP":
            DictTagMacth=TablesMapping.DescrGP2Activity_map
            pois["DIRECT_HETUS"]=pois.tag.apply(TagMatch) 
            DictTagMacth=TablesMapping.DescrGP2TusPlace_map
            pois["TUS_PLACE"]=pois.tag.apply(TagMatch)      
        #######################################################
        
        #######################################################
        # SELECT ONLY POI WITH A TUS_PLACE FOUND 
        if ADS.UseTUSdata==True:
            pois=pois[pois.TUS_PLACE.str.contains("not found")==False]
            print("*** USEFUL POI FOUND ***",len(pois))    
            #display(pois)
        if ADS.UseTUSdata==False:
            
            pois=pois[pois.DIRECT_HETUS.str.contains("not found")==False]
            print("*** USEFUL POI FOUND ***",len(pois))    
        MapServicePoisNumber=len(pois)
        #pois.to_csv("OUTPUT_RUN_ADS/POIS_"+str(User)+"_"+str(day)+"_"+str(stopID)+".csv",index=False) 
        if len(pois)==0:
            print("EXIT")
            ActivityScore=pd.DataFrame(columns=["HETUS","ActivityScore","lg","Descr","StopRadius","MapServicePoisNumber","TAG_NOT_FOUND"])
            return ActivityScore
        #######################################################   


        
        ################## dinamic search by  incremental radius ####################    
        pois=FilterPOI.FilterPOI(gps,pois,Parameters.DinaminPOISearchRadiusStep) 
        print("*** DINAMIC SEARCH POIS ***",len(pois))  
        # ASSIGN A SCORE TO POINTS OF INTEREST BY MEDIAN DISTANCE (POI-GPS sample)
        result=scorePOI_X.scorePOI_X(gps,pois,Parameters.GpsSampleSizeMax)   
        if len(result)==0:
            print("EXIT")
            ActivityScore=pd.DataFrame(columns=["HETUS","ActivityScore","lg","Descr","StopRadius","MapServicePoisNumber","TAG_NOT_FOUND"])
            return ActivityScore
        #######################################################
        
        TSTable=TablesMapping.TSTable
        # ASSIGN A PROB(tusplace,timeslot) FOR EACH POI DEPENDING ON TUSPLACE AND TIMESLOT    
        result["T_slot"]=codFascia
        #display(TSTable)
        TSTable["lg"]=TSTable["lg"].astype("str")
        result["TUS_PLACE"]=result["TUS_PLACE"]
        result=result.merge(TSTable,right_on=["lg","T_slot"],left_on=["TUS_PLACE","T_slot"],how="inner")
        
        ######### UPDATE scorePoi WITH PROB(tusplace,timeslot) 
        result["scorePoiBefore"]=result["scorePoi"]
        
        if ADS.TIMESLOT==True:
            result["scorePoi"]=(result["scorePoi"])   * result["ProbTimeslot"]  
        else:
            result["scorePoi"]=(result["scorePoi"])  
            
        result=result.sort_values("scorePoi",ascending=False).reset_index(drop=True)
        #result.to_csv("OUTPUT_RUN_ADS/RESULTS"+str(User)+"_"+str(day)+"_"+str(stopID)+".csv",index=False)   

        
        
        ################### pois short list with elbow ####################################
        if len(result)>1:
            kneedle = KneeLocator(range(len(result)), result.scorePoi.values, curve="convex", direction="decreasing")
            NpoiSL=kneedle.elbow   
        else:
            NpoiSL=1
        if NpoiSL==0:
            print ("ELBOW DOES NOT FIND POINTS")
            NpoiSL=min(3,len(result))      
        print("ELBOW: Best number of pois is:", NpoiSL)    
        #print(result)
        resultSL=result.head(NpoiSL)
        
        #######################################################



        def P_t(t,X,Ai):
            #try:        
            if True:
                if profileVar=="ageclass-condiction-place":
                    cond,etac,lg=X        
                    appo=  df_eta[(df_eta.cond==cond)&(df_eta.etac==etac)&(df_eta.lg==lg)&(df_eta.catpri18==Ai)]
                if profileVar=="condiction-place":
                    cond,lg=X        
                    appo=  df_eta[(df_eta.cond==cond)&(df_eta.lg==lg)&(df_eta.catpri18==Ai)]

                if profileVar=="ageclass-place":
                    etac,lg=X        
                    appo=  df_eta[(df_eta.etac==etac)&(df_eta.lg==lg)&(df_eta.catpri18==Ai)]
                if profileVar=="place":
                    lg=X        
                    appo=  df_eta[(df_eta.lg==lg)&(df_eta.catpri18==Ai)]
                
                if len(appo)>0:
                    
                    mu,sd=(appo[["DURM","SD"]].values.tolist()[0])
                    
                    mu=pd.Timedelta(str(mu)).total_seconds()
                    sd=pd.Timedelta(str(sd)).total_seconds()
                    
                    if ADS.DURATION_MODE=="lognorm":
                        V = np.log(   1+(sd**2)/(mu**2)  )
                        B = np.sqrt( V )
                        A = np.log (mu)-(V/2)
                        density = lognorm.pdf(t, B, scale=np.exp(A))
                        return density
                                
                    if ADS.DURATION_MODE=="norm":
                        return (norm(loc=mu,scale=sd).pdf(t))
                    if ADS.DURATION_MODE=="uniform":
                        return 1
                else:
                    return np.nan                            
        
        def P(t,X,Ai): 
            
                     
            try:
                if profileVar=="ageclass-condiction-place":
                    cond,etac,lg=X   
                    V=(df_X_dato_Ai[(df_X_dato_Ai.catpri18==Ai)&(df_X_dato_Ai.cond==cond)&(df_X_dato_Ai.lg==lg)&(df_X_dato_Ai.etac==etac)]).P_X.values[0]
                if profileVar=="ageclass-place":
                    etac,lg=X   
                    V=(df_X_dato_Ai[(df_X_dato_Ai.catpri18==Ai)&(df_X_dato_Ai.lg==lg)&(df_X_dato_Ai.etac==etac)]).P_X.values[0]
                if profileVar=="condiction-place":
                    cond,lg=X   
                    V=(df_X_dato_Ai[(df_X_dato_Ai.catpri18==Ai)&(df_X_dato_Ai.cond==cond)&(df_X_dato_Ai.lg==lg)]).P_X.values[0]
                if profileVar=="place":
                    lg=X   
                    V=(df_X_dato_Ai[(df_X_dato_Ai.catpri18==Ai)&(df_X_dato_Ai.lg==lg)]).P_X.values[0]
                return(V)
            except:
                return np.nan
            
        def fP_Ai(Ai):
            return P_Ai.loc[Ai,:].values[0]
               
        
        DescrActivity=TablesMapping.DescrActivity
        def getDescrActivity(x):
            ap=DescrActivity.get(x)
            try:
                return x+" "+ap[:]
            except:
                return ""
        
        
        def Activity(t,X):
            lAi=[]
            for Ai in sorted(df_eta.catpri18.unique()):
                
                P1=P_t(t,X,Ai)
                P2=P(t,X,Ai) 
                P3=fP_Ai(Ai) 
                P123= P1 * P2 * P3
                
                prob=Ai,P123
                if np.isfinite(P123):
                    pass
                    
                lAi.append( prob)
        
            lAi=pd.DataFrame(lAi)    
            lAi=lAi[lAi[1].isna()==False]    
            lAi["Pout"]=lAi[1]/(lAi[1].sum())
            lAi["A"]=lAi[0].apply(getDescrActivity)
            
            return lAi.sort_values(1,ascending=False).head(ADS.poi_nActivitiesPredicted).reset_index()
        ###########################################################################################    

        
        
        ActFinal=[]
        for poi in resultSL.iterrows():
            tag=poi[1].tag
            score=poi[1].scorePoi
            lg=poi[1].TUS_PLACE
            eta=profile.AgeClass.values[0]
            cond=profile.Condition.values[0]    
            t=stop.duration
             
                        
            
            if ADS.UseTUSdata==True:

                if profileVar=="ageclass-condiction-place":
                    X=(cond,eta,lg)
                if profileVar=="condiction-place":
                    X=(cond,lg)
                if profileVar=="ageclass-place":
                    X=(eta,lg)
                if profileVar=="place":
                    X=(lg)

                dfAct=Activity(t,X) 
            if ADS.UseTUSdata==False:    
                DescrActivity=TablesMapping.DescrActivity
                def getDescrActivity(x):
                    ap=DescrActivity.get(x)
                    try:
                        return x+" "+ap[:]
                    except:
                        return ""    
                directAct=poi[1].DIRECT_HETUS
                Pout=1
                A=getDescrActivity(directAct)
                dfAct=pd.DataFrame({0:[directAct],"Pout":[Pout],"A":[A]})
                
            dfAct["lg"]=lg
                
            #### EACH ACTIVITY IS MULTIPLY TO THE POI score        
            dfAct["Pscore"]=dfAct.Pout*score
            dfAct["Poiscore"]=score

            ActFinal.append(dfAct)
            
        if len(ActFinal)==0:            
            ActivityScore=pd.DataFrame(columns=["HETUS","ActivityScore","lg","Descr"])
            print("ACTIVITY SCORE EMPTY (NO PROB ACTIVITY FOR PROFILE)")
            return ActivityScore    
        else:

            ActivityScore=pd.concat(ActFinal).sort_values("Pscore",ascending=False)

            ActivityScore=ActivityScore.groupby(0).agg({"Pscore":"sum","lg":"first"}).sort_values("Pscore",ascending=False)
            ActivityScore=ActivityScore.reset_index().rename({0:"HETUS"},axis=1)
            ActivityScore["Descr"]=ActivityScore.HETUS.apply(getDescrActivity)
            
            
            ActivityScore.columns=["HETUS","ActivityScore","lg","Descr"]
            
            ActivityScore["StopRadius"]=stop.at["radius"]    
            ActivityScore["MapServicePoisNumber"]=MapServicePoisNumber
        return ActivityScore