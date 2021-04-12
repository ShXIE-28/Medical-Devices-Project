# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 17:38:20 2020

"""

import os
import pandas as pd

os.chdir(".\\DATA IMPORTACIONES")
Promed_data = pd.read_csv('Promed_data_whole_version1.csv',encoding = "ISO-8859-1",low_memory=False)

def unit_price_cal(Promed_data):
    '''
    calculate unit price from Promed data
    input: Promed_data
    output: Promed_data_MEAN, df of unit price
    '''
    Promed_data = Promed_data.drop(['DESCRIPCION POSICION', 'FECHA', 'PAIS DE ORIGEN', 'PAIS DE PROCEDENCIA', 
                                'HS_4', 'HS_6', 'keyword','RAZON SOCIAL','latitude_ori','latitude_pro','latitude_pais',
                                'longitude_ori','longitude_pro','longitude_pais'], axis=1)
    Promed_data = Promed_data[Promed_data['CANTIDAD'] > 0]
    Promed_data['unit_cif'] = Promed_data['CIF'] / Promed_data['CANTIDAD']
    Promed_data['unit_fob'] = Promed_data['FOB'] / Promed_data['CANTIDAD']
    Promed_data['diff_unit_cif_fob'] = Promed_data['unit_cif'] - Promed_data['unit_fob']
    Promed_data = Promed_data.drop(columns=['CIF','FOB'])
    Promed_data_MEAN = Promed_data.groupby(by = ['POSICION ARANCELARIA','PAIS']).mean()
    Promed_data_MEAN = Promed_data_MEAN.drop(columns = ['CANTIDAD'])
    Promed_data_SUM = Promed_data.groupby(['POSICION ARANCELARIA','PAIS']).sum()
    Promed_data_MEAN = pd.merge(Promed_data_MEAN, Promed_data_SUM[['CANTIDAD']], on = ['PAIS','POSICION ARANCELARIA'])
    return(Promed_data_MEAN)

def add_hs_code(Promed_data):
    '''
    add HS code and keyword
    input: Promed_data
    output: Promed_data with HS_4, HS_6 and keyword
    '''
    #HS_4
    hs_code = list(Promed_data['POSICION ARANCELARIA'])
    Promed_data['HS_4'] = [hs_code[i][0:4] for i in range(0,len(hs_code))]
    #HS_6
    Promed_data['HS_6'] = [hs_code[i][0:7] for i in range(0,len(hs_code))]
    #add keyword
    hs_keyword = pd.read_csv('HS code.csv', dtype=object)
    Promed_data = pd.merge(Promed_data,hs_keyword,how='left',on='HS_6')
    return(Promed_data)
    
    
Promed_data_MEAN = unit_price_cal(Promed_data)   
Promed_data_MEAN = Promed_data_MEAN.reset_index()
Promed_data_MEAN = add_hs_code(Promed_data_MEAN)
Promed_data_MEAN.to_csv('Promed_unit_price.csv', index = False)
