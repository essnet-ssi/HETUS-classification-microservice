import pandas as pd


def STOP_timeslots(day_start,day_end):
    TUS_timeslots={
     0:pd.Interval(pd.Timestamp(day_start+' 08:00:00'),pd.Timestamp(day_end+' 12:30:00'),closed='left'),
    10:pd.Interval(pd.Timestamp(day_start+' 12:30:00'),pd.Timestamp(day_end+' 14:30:00'),closed='left'),
    11:pd.Interval(pd.Timestamp(day_start+' 19:30:00'),pd.Timestamp(day_end+' 21:30:00'),closed='left'),
    2:pd.Interval(pd.Timestamp(day_start+' 14:30:00'),pd.Timestamp(day_end+' 19:30:00'),closed='left'),
    3:pd.Interval(pd.Timestamp(day_start+' 21:30:00'),pd.Timestamp(day_end+' 23:59:59'),closed='left'),
    4:pd.Interval(pd.Timestamp(day_start+' 00:00:00'),pd.Timestamp(day_end+' 08:00:00'),closed='left')
                  }
    return TUS_timeslots


def getTimeSlotFromStop(stop):
    # Dalla data di inizio e di fine dello stop, restituisce la fascia oraria relativa alle tabelle TUS
    # Se l'inizio e la fine di uno stop si sovrappone tra due fasce viene scelta la fascia con piu sovrapposizione
    #print("INFO STOP")
    #display(ADS_in["stop"])
    #print("----------")
    time_start=stop['time_start'].split(" ")[1]
    day_start=stop['time_start'].split(" ")[0]
    time_end=stop['time_end'].split(" ")[1]
    day_end=stop['time_end'].split(" ")[0]
    

    
    print("STOP start & end ",pd.to_datetime(day_start+' '+time_start) ,pd.to_datetime(day_end+' '+time_end) )
    print("\n"*4)
    
    stopInt=pd.Interval(  pd.to_datetime(day_start+' '+time_start) ,pd.to_datetime(day_end+' '+time_end) ,closed='left')
    TUS_timeslots=STOP_timeslots(day_start,day_end)
    DD={}
    for i in [0,10,11,2,3,4]:
        if TUS_timeslots[i].overlaps(stopInt):
            # Calcola i limiti della sovrapposizione
            inizio_sovrapposizione = max(TUS_timeslots[i].left, stopInt.left)
            fine_sovrapposizione = min(TUS_timeslots[i].right, stopInt.right)
            # Calcola l'ampiezza della sovrapposizione
            ampiezza_sovrapposizione = fine_sovrapposizione - inizio_sovrapposizione
            DD[i]=ampiezza_sovrapposizione
        else:
            DD[i]=pd.Timedelta('00:00:00')
            
    DD[1]=DD[10]+DD[11]
    del DD[10]
    del DD[11]
    
    chiave_massimo = max(DD, key=lambda k: DD[k].total_seconds())
    return chiave_massimo
