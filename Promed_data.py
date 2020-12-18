# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 11:45:50 2020

@author: Promed Team
"""

import os
import pandas as pd
import numpy as np
from glob import glob
from os.path import join
import collections
from googletrans import Translator
import datetime
from forex_python.converter import CurrencyRates
os.chdir(".\\DATA IMPORTACIONES")

def count_col(country):
    '''
    count number of columns for csv file
    input: country--country name(file name)
    output: print(number of columns, number of csv file)
    return number of columns
    For example: for country URUGUAY, 21 csv files contain 59 columns, 4 csv files contain 9 columns
    the function would print [(59, 21), (9, 4)], and return [59, 9]
    '''
    file_name = glob(join(country,'*.csv'))
    ncol = []
    for f in file_name:
        data = pd.read_csv(f,encoding = "ISO-8859-1",low_memory=False)
        ncol.append(data.shape[1])
    cnt = collections.Counter(ncol)
    col_num = sorted(cnt, key = cnt.get, reverse = True)
    print(cnt.most_common())
    return(col_num)

def check_col(country,ncol):
    '''
    check whether columns are aligned
    input: country--country name(file name)
           ncol--number of columns
    output:True for aligned column name
           False for unaligned column name
    For example: for country ECUADOR with 71 columns, the function would return True, since all csv 
    files' columns names are aligned
    '''
    file_name = glob(join(country,'*.csv'))
    col_name = []
    for f in file_name:
        data = pd.read_csv(f,encoding = "ISO-8859-1",low_memory=False)
        if data.shape[1] == ncol:
            col_name.append(list(data.columns))
    equal = all(ele == col_name[0] for ele in col_name)
    if len(col_name) == 0:
        print("Something wrong with number of columns!")
    return(equal)

def load_data(country,ncol):
    '''
    aggregate data for each country
    input: country--country name(file name)
           ncol--number of columns
    output: aggregated data for the input country with input ncol
    '''
    file_name = glob(join(country,'*.csv'))
    #check col name
    if check_col(country, ncol):
        df = pd.DataFrame()
        for f in file_name:
            data = pd.read_csv(f,encoding = "ISO-8859-1",low_memory=False)
            if len(list(data.columns)) == ncol:
                df = pd.concat([df,data])
        df = df.drop_duplicates()
        return(df)
    else: print("files' columns name do not align")

#aggragte data for each country
country = ['ARGENTINA','BOLIVIA','BRASIL','CHILE','COLOMBIA','COSTA RICA','ECUADOR',
           'GUATEMALA','HONDURAS','MEXICO','PANAMA','PERU','REP. DOMINICANA','URUGUAY']

for c in country:
    print(c)
    ncol = count_col(c)[0]
    df = load_data(c,ncol)
    print(df.shape)
    df.to_csv(c+'.csv', index=False)
    
def bolivia_curreny(year, currency):
    '''
    Average exchange rate in 2013: 6.9459 BOB.
    Average exchange rate in 2014: 6.9111 BOB.
    Average exchange rate in 2015: 6.9048 BOB.
    source:https://www.exchangerates.org.uk/USD-BOB-spot-exchange-rates-history-2015.html
    '''
    if year == 2013:
       return currency / 6.9459
    if year == 2014:
       return  currency / 6.9111
    if year == 2015:
       return  currency / 6.9048
   
def chile_port(data):
    port = pd.DataFrame(data['PUERTO DE EMBARQUE'].unique())
    port.rename(columns={0:"Port"},inplace=True)
    split = port['Port'].str.split(",",expand=True)
    port = pd.concat([port,split],axis=1)
    translator = Translator()
    port['trans 0'] = port[0].apply(lambda x:translator.translate(str(x)).text)
    port['country'] = port[port['trans 0'].str.find("NORTH AMERICA")==0]['trans 0'].apply(lambda x:x[14:].strip())
    port[port['country']=='CANADA?'] = 'CANADA'
    port.loc[port['trans 0'].str.find("ASIA")==0,'country']=port[port['trans 0'].str.find("ASIA")==0]['trans 0'].apply(lambda x:x[5:].strip())
    port.loc[port['trans 0'].str.find("EUROPE")==0,'country']=port[port['trans 0'].str.find("EUROPE")==0]['trans 0'].apply(lambda x:x[7:].strip())
    port[port['country']=='B? LGICA'] = 'BELGIUM'
    port.loc[port['trans 0'].str.find("LATIN AMERICA")==0,'country']=port[port['trans 0'].str.find("LATIN AMERICA")==0]['trans 0'].apply(lambda x:x[14:].strip())
    port.loc[port['trans 0'].str.endswith("EUROPE"),'country']=port[port['trans 0'].str.endswith("EUROPE")]['trans 0'].apply(lambda x:x[:-7].strip())
    port.loc[port['trans 0'].str.find("CHILE")==0,'country']='CHILE'
    port.loc[port['trans 0'].str.find("AMERICA LATINA")==0,'country']=port[port['trans 0'].str.find("AMERICA LATINA")==0]['trans 0'].apply(lambda x:x[15:].strip())
    port.loc[port['trans 0'].str.find("AM?RICA LATINA")==0,'country']=port[port['trans 0'].str.find("AM?RICA LATINA")==0]['trans 0'].apply(lambda x:x[15:].strip())
    port.loc[port['trans 0']=="OCEANIA AUSTRALIA",'country']='AUSTRALIA'
    port.loc[port['trans 0']=="OCEAN?A AUSTRALIA",'country']='AUSTRALIA'
    port.loc[port['trans 0']=="AFRICA SOUTH AFRICA",'country']='SOUTH AFRICA'
    port.loc[port['trans 0']=="SOUTH AFRICA AFRICA",'country']='SOUTH AFRICA'
    port[port['country']=='PER?'] = 'PERU'
    port.loc[port['trans 0']=="Am? Richa Latin drink?",'country']='PANAMA'
    port.loc[port['country'].isnull(),'country'] = port[port['country'].isnull()]['trans 0']
    port = port.drop(58)
    return(port)

def ex_rate(cur,year):
    """
    calculate the avg ex rate for a certain year
    """
    c = CurrencyRates()
    temp_rate = []
    if cur == 'GRD':
        return(0.004)
    elif cur == 'CLP':
        if year == 2010:
            return(0.001962)
        elif year == 2013:
            return(0.002)
        elif year == 2014:
            return(0.001753)
        else:
            return(0.001529)
    elif cur =='COP':
        return(0.0003277)
    else:
        for m in range(12):
            date_obj = datetime.datetime(year,m+1,1)
            temp_rate.append(c.get_rate(cur,'USD',date_obj))
        return np.mean(temp_rate)
    
def chile_currency(data):
    data['year'] = data['FECHA DOCUMENTO TRANSPORTE'].apply(lambda x:str(x[:4]))
    data['year'] = data['year'].astype('int')
    temp = data[['year','MONEDA']]
    temp = temp.drop_duplicates(keep='first')
    currency_abb = {'MONEDA':['Dolar ee.uu.','Euro','Peso','Franco suiza','Otras no especi','Cruzeiro real',
                          'Dolar canada','Corona dinamarc','Yen','Libra esterlina','Corona suecia',
                          'Dolar australia','Corona noruega','Rand','Peso mexico','Rupia','Dracma',
                          'Dolar nva.zelan','Peso colombia','Ecu','Corona suecia','Dolar singapur'],
                'ABB':['USD','EUR','CLP','CHF','USD','BRL','CAD','DKK','JPY','GBP','SEK','AUD','NOK',
                       'ZAR','MXN','IDR','GRD','NZD','COP','EUR','SGD','SGD']}
    currency_abb_df = pd.DataFrame(currency_abb)
    temp = pd.merge(temp,currency_abb_df,how='left',left_on='MONEDA',right_on='MONEDA')
    temp['ex_rate'] = temp.apply(lambda row: ex_rate(row['ABB'],row['year']),axis=1)
    return(temp)

def transform(data, country):
    '''
    input: data df of country
           country: country name
    output: dataframe 
    '''
    if 'PAIS ORIGEN' in data.columns:
        data.rename(columns = {'PAIS ORIGEN':'PAIS DE ORIGEN'}, inplace = True)
    if 'PAIS PROCEDENCIA' in data.columns:
        data.rename(columns={'PAIS PROCEDENCIA':'PAIS DE PROCEDENCIA'}, inplace=True)
    if 'FECHA DESPACHO' in data.columns:
        data.rename(columns={'FECHA DESPACHO':'FECHA'}, inplace=True)
    if country == 'ARGENTINA':
        data.rename(columns = {'FOB DOLARS ITEM':'FOB','CIF DOLARS ITEM':'CIF',
                               'CANTIDAD ITEM':'CANTIDAD'}, inplace = True)
        data = data.dropna(subset = ['CIF', 'FOB', 'CANTIDAD'])
    if country == 'BOLIVIA':
        data['FECHA'] = pd.to_datetime(data['FECHA'], format='%Y/%m/%d')
        data['year'] = data['FECHA'].dt.year
        data['CIFBEFORE'] = data['CIF TOT Bs. ULTIMA'].str.replace(',','').astype(float)
        data['CIF'] = data.apply(lambda x: bolivia_curreny(x.year,x.CIFBEFORE), axis = 1)
        data.rename(columns = {'FOB TOT $US PRIMERA':'FOB'}, inplace = True)
        data.rename(columns = {'DESCRIPCION':'DESCRIPCION POSICION'}, inplace = True)
        #data.rename(columns =  {'ITEM':'CANTIDAD'}, inplace = True)
    if country == 'BRASIL':
        data.rename(columns={'DESCRIPCION':'DESCRIPCION POSICION','VALOR FOB':'FOB'}, inplace = True)
    if country == 'CHILE':
        data.rename(columns={'GLOSA':'POSICION ARANCELARIA','DESCRIPCION GLOSA':'DESCRIPCION POSICION',
                             'CANTIDAD DE BULTOS':'CANTIDAD','FECHA DEL DESPACHO':'FECHA'}, inplace = True)
        port = chile_port(data)
        data = pd.merge(data,port,how='left',left_on='PUERTO DE EMBARQUE',right_on='Port')
        data.rename(columns={'country':'PAIS DE PROCEDENCIA'},inplace=True)
        currency = chile_currency(data)
        data = pd.merge(data,currency,how='left',on=['MONEDA','year'])
        data['CIFVALUE'] = data['VALOR CIF'].str.replace(',','').astype(float)
        data['CIF'] = data['CIFVALUE']*data['ex_rate']
        data['FOBVALUE'] = data['VALOR FOB'].str.replace(',','').astype(float)
        data['FOB'] = data['FOBVALUE']*data['ex_rate']
    if country == 'COLOMBIA':
        data.rename(columns={'CIF U$S':'CIF','FOB U$S':'FOB','DESCRIPCION DE LA POSICION':'DESCRIPCION POSICION'}, inplace=True)
    if country == 'COSTA RICA':
        data.rename(columns={"DESCRIPCION":"DESCRIPCION POSICION","UNIDADES":"CANTIDAD","CIF US$":"CIF",'IMPORTADOR':'RAZON SOCIAL'}, inplace=True)
    if country == 'ECUADOR':
        data.rename(columns={'CIF U$S':'CIF','FOB U$S':'FOB'}, inplace=True)
        data.rename(columns={'ITEM':'CANTIDAD'}, inplace=True)
    if country == 'GUATEMALA':
        pass
    if country == 'HONDURAS':
        pass
    if country == 'MEXICO':
        data.rename(columns={'VALOR CIF U$S':'CIF'}, inplace=True)
    if country == 'PANAMA':
        data.rename(columns={'CIF U$S':'CIF','FOB U$S':'FOB','CANTIDAD COMERCIAL':'CANTIDAD'}, inplace=True)
    if country == 'PERU':
        peru_port = pd.read_csv('peru_port.csv',encoding = "ISO-8859-1",low_memory=False)
        data = pd.merge(data, peru_port, on = 'PUERTO DE EMBARQUE')
        data.rename(columns={'CIF U':'CIF','FOB U':'FOB','country_english':'PAIS DE PROCEDENCIA'}, inplace=True)
    if country == 'REP. DOMINICANA':
        pass
    if country == 'URUGUAY':
        data.rename(columns={'TOTAL CIF U$S':'CIF'}, inplace=True)
    return(data)

def diff(list1, list2): 
    '''
    find elements that exist in list1 but do not exist in list2
    input: lists
    output: list
    '''
    return (list(set(list1) - set(list2)))

def aggregate_data(country, select_var):
    '''
    aggregate all data of selected variables
    input: country list
           selected variables list
    output: dataframe of aggregated data
    '''
    df = pd.DataFrame()
    complete_country = []
    for c in country:
        print(c)
        data = pd.read_csv(c+'.csv',encoding = "ISO-8859-1",low_memory=False)
        data['PAIS'] = c
        data = transform(data, c)
        var_list = list(data.columns)
        common_var = list(set(var_list).intersection(select_var))
        select_data = data[common_var]
        #fill nan
        missing_var = diff(select_var,common_var)
        for m in missing_var:
            select_data[m] = float("nan")
        #convert number
        if select_data.shape[1] == len(select_var):
            select_data = select_data.sort_index(axis=1)
            df = pd.concat([df,select_data])
            complete_country.append(c)
    df['CIF'] = df['CIF'].astype(str).str.replace(',','').astype(float)
    df['FOB'] = df['FOB'].astype(str).str.replace(',','').astype(float)
    df['CANTIDAD'] = df['CANTIDAD'].astype(str).str.replace(',','').astype(float)
    df['FECHA'] = pd.to_datetime(df['FECHA'])
    if len(complete_country) == len(country):
        print("Aggregation Complete!")
    else:
        missing_country = diff(country, complete_country)
        for m in missing_country:
            print(m, "doesn't aggregate!")
    return(df)
    
country = ['ARGENTINA','BOLIVIA','BRASIL','CHILE','COLOMBIA','COSTA RICA','ECUADOR',
           'GUATEMALA','HONDURAS','MEXICO','PANAMA','PERU','REP. DOMINICANA','URUGUAY']
select_var = ['PAIS','PAIS DE ORIGEN','PAIS DE PROCEDENCIA','POSICION ARANCELARIA',
              'DESCRIPCION POSICION','CIF', 'FOB', 'CANTIDAD','FECHA','RAZON SOCIAL'] #PAIS(country) 
Promed_data = aggregate_data(country, select_var)

#HS_4
hs_code = list(Promed_data['POSICION ARANCELARIA'])
Promed_data['HS_4'] = [hs_code[i][0:4] for i in range(0,len(hs_code))]
#HS_6
Promed_data['HS_6'] = [hs_code[i][0:7] for i in range(0,len(hs_code))]

#add keyword
hs_keyword = pd.read_csv('HS code.csv', dtype=object)
Promed_data = pd.merge(Promed_data,hs_keyword,how='left',on='HS_6')

#merge country
PERU = Promed_data[Promed_data['PAIS'] == 'PERU']
len(PERU)

Promed_data = Promed_data[Promed_data['PAIS'] != 'PERU']
new_country = pd.read_csv('ctry_new.csv',encoding = "ISO-8859-1",low_memory=False)
location = new_country[['country_english','latitude','longitude']]  
new_country = new_country[['country name (Spanish)','country_english']]
new_country = new_country.drop(new_country.index[[513,657,709]]) 
new_country = new_country.drop_duplicates()
location = location.drop(location.index[[513,657,709]])  
location = location.drop_duplicates()

Promed_data = pd.merge(Promed_data,new_country,how='left',left_on='PAIS DE ORIGEN',right_on='country name (Spanish)')
Promed_data = Promed_data.drop(columns=['country name (Spanish)','PAIS DE ORIGEN'])
Promed_data.rename(columns={'country_english':'PAIS DE ORIGEN'}, inplace=True)
Promed_data = pd.merge(Promed_data,new_country[['country name (Spanish)','country_english']],how='left',left_on='PAIS DE PROCEDENCIA',right_on='country name (Spanish)')
Promed_data = Promed_data.drop(columns=['country name (Spanish)','PAIS DE PROCEDENCIA'])
Promed_data.rename(columns={'country_english':'PAIS DE PROCEDENCIA'}, inplace=True)
Promed_data = pd.concat([Promed_data,PERU],sort=True)
Promed_data['PAIS DE ORIGEN'] = Promed_data['PAIS DE ORIGEN'].astype(str).apply(lambda x: x.upper())  
Promed_data['PAIS DE PROCEDENCIA'] = Promed_data['PAIS DE PROCEDENCIA'].astype(str).apply(lambda x: x.upper())  

## add longitude and latitude 
Promed_data.loc[Promed_data['PAIS DE ORIGEN']=='KOREA, REPUBLIC OF','PAIS DE ORIGEN'] = 'SOUTH KOREA'
Promed_data.loc[Promed_data['PAIS DE ORIGEN']=='VIET NAM','PAIS DE ORIGEN'] = 'VIETNAM'
Promed_data.loc[Promed_data['PAIS DE ORIGEN']=='UNITED STATES MINOR OUTLYING ISLANDS','PAIS DE ORIGEN'] = 'UNITED STATES'
Promed_data.loc[Promed_data['PAIS DE ORIGEN']=='RUSSIAN FEDERATION','PAIS DE ORIGEN'] = 'RUSSIA'
Promed_data.loc[Promed_data['PAIS DE ORIGEN']=='IRAN (ISLAMIC REPUBLIC OF)','PAIS DE ORIGEN'] = 'IRAN'
Promed_data.loc[Promed_data['PAIS DE ORIGEN']=='VATICAN CITY STATE (HOLY SEE)','PAIS DE ORIGEN'] = 'VATICAN CITY'
Promed_data.loc[Promed_data['PAIS DE PROCEDENCIA']=='SÃÂÃÂ£O TOMÃÂÃÂ© AND PRÃÂÃÂ­NCIPE','PAIS DE PROCEDENCIA'] = 'SAO TOME AND PRINCIPE'
Promed_data.loc[Promed_data['PAIS']=='BRASIL','PAIS'] = 'BRAZIL'
Promed_data.loc[Promed_data['PAIS']=='REP. DOMINICANA','PAIS'] = 'DOMINICAN REPUBLIC'

temp = pd.merge(Promed_data,location,how='left',left_on='PAIS DE ORIGEN',right_on='country_english')

temp = pd.merge(temp,location,how='left',left_on='PAIS DE PROCEDENCIA',right_on='country_english')
temp.rename(columns={'latitude_x':'latitude_ori','latitude_y':'latitude_pro','longitude_x':'longitude_ori','longitude_y':'longitude_pro'},inplace=True)
del temp['country_english_x']
del temp['country_english_y']
temp = pd.merge(temp,location,how='left',left_on='PAIS',right_on='country_english')
temp.rename(columns={'latitude':'latitude_pais','longitude':'longitude_pais'},inplace=True)
del temp['country_english']



#write csv
temp.to_csv('Promed_data_whole_version1.csv', index=False)
