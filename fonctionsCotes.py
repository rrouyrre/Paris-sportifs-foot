#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 17:14:43 2020

@author: rouyrrerodolphe
"""


import bs4
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


def dfFic(nomFic) :
    """ 
    Prend le nom d'un fichier en entree et retourne 2 dataframes en sortie.
    Fonction qui permet de recuperer les cotes contenues dans le code html d'un fichier.
    Le premier dataframe contient les cotes 1X2, le resultat et les cotes gagnantes.
    Le deuxieme dataframe contient les probas traduites par les cotes.
    """
    
    fic = open(nomFic, 'r')
    page2 = bs4.BeautifulSoup(fic, "lxml")
    
    html = str(page2.findAll('table')[0])
    
    soup = bs4.BeautifulSoup(html, "html.parser")
    
    results = soup.findAll("td", {"class" : ['table-main__odds']})
    liste = [[],[],[]]
    victoires = []
    cotes = []
    probas = [[],[],[]]
    for i in range(len(results)):
        j = i%3
        soup = bs4.BeautifulSoup(str(results[i]), "html.parser")
        if len(str(soup.span).split('"'))>1 :
            liste[j].append(str(soup.span).split('"')[1])
            victoires.append(j)
            cotes.append(str(soup.span).split('"')[1])
            #probas[j].append(round((1/(float(str(soup.span).split('"')[1]))),2))
            probas[j].append((1/(float(str(soup.span).split('"')[1]))))
        else :
            liste[j].append(results[i].attrs["data-odd"])
            #probas[j].append(round(1/(float(results[i].attrs["data-odd"])),2))
            probas[j].append((1/(float(results[i].attrs["data-odd"]))))
    
    liste[0] = liste[0][0:min(len(liste[0]),len(liste[1]),len(liste[2]), len(victoires))]
    liste[1] = liste[1][0:min(len(liste[0]),len(liste[1]),len(liste[2]),len(victoires))]
    liste[2] = liste[2][0:min(len(liste[0]),len(liste[1]),len(liste[2]),len(victoires))]
    
    victoires = victoires[0:min(len(liste[0]),len(liste[1]),len(liste[2]),len(victoires))]
    cotes = cotes[0:min(len(liste[0]),len(liste[1]),len(liste[2]))]    
    
    df = pd.DataFrame({'1' : liste[0], 'X' : liste[1], '2' : liste[2], 
                        'victoires' : victoires, 'cotes' : cotes})
    
    df = df.apply(pd.to_numeric, errors='coerce')
    df2 = pd.DataFrame(probas)
    df2 = df2.apply(pd.to_numeric, errors='coerce')
    
    return df, df2 


def dfTRJ(df1,df2) :
    """ Fonction qui permet de calculer le TRJ et les cotes telles qu'estimees 
        par le bookmaker.
    """
    
    # CA POURRAIT ETRE SIMPLIFIE
    df1['TRJ'] = round(1/df2.sum()*100,2)
    df1['somme'] = df2.sum()
    
    df1['proba 1'] = 1/df1['1']
    df1['proba X'] = 1/df1['X']
    df1['proba 2'] = 1/df1['2']
    df1['proba'] = 1/df1['cotes']
    
    df1['cote reelle'] = df1['cotes']*df1['somme']
    df1['cote reelle 1'] = df1['1']*df1['somme']
    df1['cote reelle X'] = df1['X']*df1['somme']
    df1['cote reelle 2'] = df1['2']*df1['somme']
    
    df1['proba reelle'] = 1/df1['cote reelle']
    df1['proba reelle 1'] = 1/df1['cote reelle 1']
    df1['proba reelle X'] = 1/df1['cote reelle X']
    df1['proba reelle 2'] = 1/df1['cote reelle 2']
    
    # On verifie que la somme des probabilites est bien egale a 1 :
    df1['somme proba'] = df1['proba reelle 1'] + df1['proba reelle X'] + df1['proba reelle 2']
    
    return df1


def dfProbaArr(df1) :
    """ Cette fonction permet de regrouper les cotes proches.
    """
    
    df3 = pd.DataFrame()
    df3['cotes2'] = np.zeros(len(df1)) + 0.01
    df3['12'] = np.zeros(len(df1)) + 0.01
    df3['X2'] = np.zeros(len(df1)) + 0.01
    df3['22'] = np.zeros(len(df1)) + 0.01
    k = 5
    h = k/100
    for i in range(int(100/k)) :
        proba = h*(i+1)
        df3['cotes2'] = np.where(df1['proba']>proba, (h*i+h*(i+1))/2, df3['cotes2'])
        df3['12'] = np.where(df1['proba 1']>proba, (h*i+h*(i+1))/2, df3['12'])
        df3['X2'] = np.where(df1['proba X']>proba, (h*i+h*(i+1))/2, df3['X2'])
        df3['22'] = np.where(df1['proba 2']>proba, (h*i+h*(i+1))/2, df3['22'])
    
    return df3


def dfProbaReellesArr(df1) :
    """ Cette fonction permet de regrouper les cotes reelles qui sont proches.
        Les colonnes crees contiennent les probas reelles arrondies a 2.5% pres.
    """
    
    df3 = pd.DataFrame()
    df3['cotes2'] = np.zeros(len(df1)) + 0.01 # Les 0.01 sont necessaires pr ne pas diviser par 0
    df3['12'] = np.zeros(len(df1)) + 0.01
    df3['X2'] = np.zeros(len(df1)) + 0.01
    df3['22'] = np.zeros(len(df1)) + 0.01
    k = 5 # Le pas choisi
    h = k/100 # Le pas en pourcentage
    for i in range(int(100/k)) : # On prend 100/k pr couvrir toutes les probas de 0 a 1
        proba = h*(i+1)
        df3['cotes2'] = np.where(df1['proba reelle']>proba, (h*i+h*(i+1))/2, df3['cotes2'])
        df3['12'] = np.where(df1['proba reelle 1']>proba, (h*i+h*(i+1))/2, df3['12'])
        df3['X2'] = np.where(df1['proba reelle X']>proba, (h*i+h*(i+1))/2, df3['X2'])
        df3['22'] = np.where(df1['proba reelle 2']>proba, (h*i+h*(i+1))/2, df3['22'])

    return df3
 

def listeCotes(df1) :
    """ Fonction qui renvoie un dataframe compose de toutes les probas reelles 
    arrondies du dataframe d'entree.
    """
    
    liste2 = df1['12']
    liste2 = liste2.append(df1['X2'])
    liste2 = liste2.append(df1['22'])
    df4 = pd.DataFrame(liste2)

    return df4


def favoris(df) :
    """ Fonction qui ajoutent des colonnes au dataframe d'entree en distinguant 
        les cotes des favoris, des outsiders et celles neutres.
    """
    
    df['favoris'] = df[['1','2','X']].min(axis=1)
    df['neutres'] = df[['1','2','X']].median(axis=1)
    df['outsiders'] = df[['1','2','X']].max(axis=1)
    
    df['cotes3'] = np.zeros(len(df))
    df['cotes3'] = np.where(df['cotes'] == df['favoris'], 'favoris', df['cotes3'])
    df['cotes3'] = np.where(df['cotes'] == df['neutres'], 'neutre', df['cotes3'])
    df['cotes3'] = np.where(df['cotes'] == df['outsiders'], 'outsider', df['cotes3'])
    
#    df.groupby('cotes3').size()
#    df[df['cotes3']=='outsider']['cotes'].mean()
    
    tab = np.zeros(3)
    tab[0] = df.groupby('cotes3').size()[0]*df[df['cotes3']=='favoris']['cotes'].mean()-len(df)
    tab[1] = df.groupby('cotes3').size()[1]*df[df['cotes3']=='neutre']['cotes'].mean()-len(df)
    tab[2] = df.groupby('cotes3').size()[2]*df[df['cotes3']=='outsider']['cotes'].mean()-len(df)

    return df, tab

def strategieDom(df) :
    
    tab = np.zeros(3)
    tab[0] = df[df['1']==df['cotes']]['cotes'].sum()-len(df)
    tab[1] = df[df['X']==df['cotes']]['cotes'].sum()-len(df)
    tab[2] = df[df['2']==df['cotes']]['cotes'].sum()-len(df)
    
    return tab 

def figures(df3,df4,df5,df6) :
    
    # Figures pour visualiser :
    df7 = pd.DataFrame({'frequence' : df3.groupby('cotes2').size()/df5.groupby(0).size()})
    df8 = pd.DataFrame({'frequence' : df4.groupby('cotes2').size()/df6.groupby(0).size()})
    
    fig, ax = plt.subplots()
    df7['frequence'].plot(kind='bar')
    fig.suptitle('cote book value', fontsize=16)
    plt.subplots_adjust(top=0.88)
    
    df7 = df7.rename_axis('cotes2').reset_index()
    #df7['index'] = df7['cotes2']
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
    
    
if __name__ == '__main__':
    
    os.chdir('/home/rouyrrerodolphe/Bureau/PROJET PS/SERIE A/BETEXPLORER')
    
    # Test de la fonction dfFic :
    dfCotes, dfProbas = dfFic('SerieA_2019-2020')
    print(dfCotes.describe())
    
    # Test de la fonction dfTRJ : 
    df1 = dfTRJ(dfCotes,dfProbas)
    print(df1.describe())

    # Test de la fonction dfProbaArr :
    df4 = dfProbaArr(df1)
    #print(df3.describe())
    
    # Test de la fonction dfProbaReelleArr :
    df3 = dfProbaReellesArr(df1)
    #print(df4.describe())

    # Test de la fonction listeCotes :
    df5 = listeCotes(df3)
    df6 = listeCotes(df4)
    
    # Test de la fonction favoris : 
    dfCotes, tab = favoris(dfCotes)

    # Test de la fonction figures : 
    figures(df3,df4,df5,df6)

    # Test de la fonction strategieDom :
    tab2 = strategieDom(df1)

