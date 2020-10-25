#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 11:57:58 2020

@author: rouyrrerodolphe
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import fonctionsCotes


#path = '/home/rouyrrerodolphe/Bureau/LIGUE1/BETEXPLORER'
def analyseChampionnat(championnat) :
    """ Prend le nom d'un championnat en entree, retourne 2 dataframes en 
    sortie
    """
    
    path = ('/home/rouyrrerodolphe/Bureau/{0}/BETEXPLORER'.format(championnat))
    
    listeDf = []
    listeDf2 = []
    grosDf = pd.DataFrame()
    grosDf2 = pd.DataFrame()
    grosDfTRJ = pd.DataFrame()
    tab = []
    tab2 = []
    for i in range(len(glob.glob('{0}/*' .format(path)))):
        df, df2 = fonctionsCotes.dfFic(glob.glob('{0}/*' .format(path))[i])
        df2 = df2.dropna(axis='columns')
        listeDf.append(df)
        listeDf2.append(df2)
        if i == 0 :
            grosDf = df
            grosDf2 = df2
            grosDfTRJ = fonctionsCotes.dfTRJ(df,df2)
            dfFav,tab1 = fonctionsCotes.favoris(df)
            tab.append(tab1)
        else :
            grosDf = grosDf.append(df)
            grosDf2 = grosDf2.append(df2)         
            grosDfTRJ = grosDfTRJ.append(fonctionsCotes.dfTRJ(df,df2))
            dfFav,tab1 = fonctionsCotes.favoris(grosDfTRJ)
            dfFav,tab1 = fonctionsCotes.favoris(df)
            tab.append(tab1)
            tab3 = fonctionsCotes.strategieDom(df)
            tab2.append(tab3)
            
    return grosDf, grosDfTRJ, tab, tab2


def strategie(df) :
    """ Prend un dataframe en entree. 
        Trace les nuages de points pour les strategies a choix uniques.
    """
    
    fig, ax = plt.subplots()
    f = plt.scatter(df.index,df[0])
    n = plt.scatter(df.index,df[1])
    o = plt.scatter(df.index,df[2])

    plt.legend((f,n,o),('favoris','neutres','outsiders'))
    
def strategieDom(df) :

    fig, ax = plt.subplots()
    f = plt.scatter(df.index,df[0])
    n = plt.scatter(df.index,df[1])
    o = plt.scatter(df.index,df[2])

    plt.legend((f,n,o),('domicile','nul','exterieur'))
    
def comparaisonTRJ(grosDf, grosDfTRJ) :       
    # J'AI L'IMPRESSION QUE Y A UN GROS PB AVEC DF3
    df3 = fonctionsCotes.dfProbaArr(grosDf)
    print(df3.describe())
    df4 = fonctionsCotes.dfProbaReellesArr(grosDfTRJ)
    print(df4.describe())
    
    df5 = fonctionsCotes.listeCotes(df3)
    df6 = fonctionsCotes.listeCotes(df4)
    
    df7 = pd.DataFrame({'frequence' : df3.groupby('cotes2').size()/df5.groupby(0).size()})
    df8 = pd.DataFrame({'frequence' : df4.groupby('cotes2').size()/df6.groupby(0).size()})
    
    fig, ax = plt.subplots()
    df7['frequence'].plot(kind='bar')
    fig.suptitle('cote book value', fontsize=16)
    plt.subplots_adjust(top=0.88)
    
    df7 = df7.rename_axis('cotes2').reset_index()
    #df7['diff'] = (df7['cotes2']-df7['frequence'])
    df7['diff'] = (df7['cotes2']-df7['frequence'])
    
    fig, ax = plt.subplots()
    df7['diff'].plot(kind='bar')
    fig.suptitle('cote book diff', fontsize=16)
    plt.subplots_adjust(top=0.88)
    
    
    fig, ax = plt.subplots()
    df8['frequence'].plot(kind='bar')
    fig.suptitle('cote reelle value', fontsize=16)
    plt.subplots_adjust(top=0.88)
    
    df8 = df8.rename_axis('cotes2').reset_index()
    df8['diff'] = (df8['cotes2']-df8['frequence'])
    
    fig, ax = plt.subplots()
    df8['diff'].plot(kind='bar')
    fig.suptitle('cote reelle diff', fontsize=16)
    plt.subplots_adjust(top=0.88)
    
    
    fig, ax = plt.subplots()
    x = np.array([0,1])
    y = x
    plt.plot(x,y)

    plt.scatter(df7['cotes2'],df7['frequence'])
    plt.scatter(df8['cotes2'],df8['frequence'])
    
    
    grosDfTRJ = grosDfTRJ.reset_index()


if __name__ == '__main__':
    
    championnats = ['LIGUE1', 'PREMIER LEAGUE', 'BUNDESLIGA', 
                    'LIGA', 'SERIE A']
    
    for j in range(len(championnats)):
    
        # Test de la fonction analyse championnat :
        grosDf, grosDfTRJ, tab, tab2 = analyseChampionnat(championnats[j])
        
        # Test de la fonction strategie :
        df = pd.DataFrame(tab)
        
        strategie(df)
        
       # tab2 = fonctionsCotes.strategieDom(grosDfTRJ)
        df2 = pd.DataFrame(tab2)
        
        strategieDom(df2)
        
        # Test de la fonction comparaison :
        comparaisonTRJ(grosDf, grosDfTRJ)
    
        df1,tab2 = fonctionsCotes.favoris(grosDfTRJ)
    # LE BON DATAFRAME EST GROSDFTRJ







