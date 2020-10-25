#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 11:04:19 2020

@author: rouyrrerodolphe
"""


import pandas as pd
import numpy as np
import glob
import os
import matplotlib.pyplot as plt

   
def porc(nomfic):
    """
    Renvoie les pourcentages de victoires pour un fichier (et donc une annee)
    Necessite un fichier Resultat en entree
    """
    
    df4 = pd.read_excel(nomfic)
    
    nbNul = []
    nbDom = []
    nbExt = []
    nbAutres = []
    for i in range(len(df4.columns)):
        if i > 1 :
            nbNul.append(len(df4[df4[i].isin(['Nul'])]))
            nbDom.append(len(df4[df4[i].isin(['Domicile'])]))
            nbExt.append(len(df4[df4[i].isin(['Extérieur'])]))
            nbAutres.append(len(df4[~df4[i].isin(['Nul','Domicile','Extérieur'])]))
            
    totNul = 0
    totDom = 0
    totExt = 0
    totAutres = 0
    for i in range(len(nbNul)):
        totNul += nbNul[i]
        totDom += nbDom[i]
        totExt += nbExt[i]
        totAutres += nbAutres[i]
        
    tot = totNul + totDom + totExt
    
    porcDom = round((totDom/tot)*100,2)
    porcNul = round((totNul/tot)*100,2)
    porcExt = round((totExt/tot)*100,2)
    porcAutres = (totAutres/tot)*100
    
    return porcDom, porcNul, porcExt, porcAutres    
    
def figures(porcDom, porcNul, porcExt, porcAutres) :
    
    plt.hist()
    
def porcAnnee(path):
    """Renvoie les listes de pourcentages de victoires de chaque annee
    """
    
    porcDom = []
    porcNul = []
    porcExt = []
    porcAutres = []
    for i in range(len(glob.glob('{0}/*' .format(path)))):
        porcDom.append(['0'])
        porcNul.append(['0'])
        porcExt.append(['0'])
        porcAutres.append(['0'])
        porcDom[i], porcNul[i], porcExt[i], porcAutres[i] = porc(glob.glob('{0}/*' .format(path))[i])
    
def nbButs(nomfic) :
    """
    Necessite un fichier Score en entree.
    Retourne les nombres de buts par match (domicile/exterieur/totaux) et le nombre de matchs.
    """
    
    df = pd.read_excel(nomfic) # Prend un fichier du dossier score
    df = df.apply(pd.to_numeric, errors='coerce') # Normalement y a plus besoin

    nbButsDom = 0
    nbButsExt = 0
    nbButsTot = 0
    nbMatchs = 0
    for i in range(len(df.columns)):
        if i > 1 :
            nbButsTot += np.sum(df[i])
            # Numero de colonne pair : domicile, impair : exterieur
            if i%2 == 0 :
                nbButsDom += np.sum(df[i])
                nbMatchs += len(df[i].dropna())
            else :
                nbButsExt += np.sum(df[i])
    nbBMDom = nbButsDom/nbMatchs
    nbBMExt = nbButsExt/nbMatchs
    nbBMTot = nbButsTot/nbMatchs
    
    return nbBMDom, nbBMExt, nbBMTot, nbMatchs

def ecart(df) :
    """
    A partir d'un fichier scores.
    Trace un histogramme representant l'ecart de buts entre l'equipe a domicile et l'equipe a l'exterieur, sur une saison.
    """
    
    df2 = pd.DataFrame()
    df3 = pd.DataFrame()
    
    for i in range(len(df.columns)-1):
        if i > 1 :
            if i%2 == 0 :
                df2[i] = np.zeros(len(df))
                df2[i] = df[i]-df[i+1]
    
    liste = []
    for i in range(20) :
        liste.append(i-9)
        
    l2 = np.zeros(len(liste))
    df3 = pd.DataFrame({'l' : liste,'l2' : l2})
    
    df3 = df3.set_index('l')
    for j in df2.columns :
        for i in df2.groupby(j).size().index :
            df3.iloc[i+9] = df3.iloc[i+9] + df2.groupby(j).size()[i]
    
    df3.plot(kind='bar')
    
    return df2

def championnatResultats(championnat) :
    """ Trace un histogramme representant l'evolution du pourcentage de victoires a domicile.
        Utilise la fonction porc
    """
    
    indexAnn = ['00-01','01-02','02-03','03-04','04-05','05-06','06-07',
            '07-08','08-09','09-10','10-11','11-12','12-13','13-14',
            '14-15','15-16','16-17','17-18','18-19','19-20']

    
    path = '/home/rouyrrerodolphe/Bureau/{0}/RESULTATS/'.format(championnat)
    #grosDataFrame(path)
    path2 = '/home/rouyrrerodolphe/Bureau/{0}/'.format(championnat)
    os.chdir(path2)
        
    #porcDom, porcNul, porcExt, porcAutres = porc('Gros_DataFrame.xlsx')
    
    porcDom = []
    porcNul = []
    porcExt = []
    porcAutres = []
    fichiers = []
    diffDomExt = []
    for i in range(len(glob.glob('{0}/*' .format(path)))):
        porcDom.append(['0'])
        porcNul.append(['0'])
        porcExt.append(['0'])
        porcAutres.append(['0'])
        porcDom[i], porcNul[i], porcExt[i], porcAutres[i] = porc(glob.glob('{0}/*' .format(path))[i])
        fichiers.append(glob.glob('{0}/*' .format(path))[i])
        diffDomExt.append(porcDom[i] - porcExt[i])
    
    df = pd.DataFrame({'fichiers' : fichiers, 'porcDom' : porcDom,
                       'porcNul' : porcNul, 'porcExt' : porcExt, 
                       'diff' : diffDomExt})
    
    df = df.set_index('fichiers')
    df = df.sort_index()
    df = df.reset_index()
    df['indexAnn'] = indexAnn
    df = df.set_index('indexAnn')
    
    
    os.chdir('/home/rouyrrerodolphe/Bureau/PROJET PS/{0}/' .format(championnat))
    
    fig, ax = plt.subplots()
    df['diff'].plot(kind='bar')
    fig.suptitle('porcDom {0}' .format(championnat), fontsize=16)
    plt.subplots_adjust(top=0.88)
    fig.savefig('PorcDom_{0}.png' .format(championnat), dpi=fig.dpi, bbox_inches='tight')
    
    
def championnatScores(championnat) :
    """ Trace une courbe representant l'evolution du nombre de buts par match
        Utilise la fonction nbButs    
    """ 
    
    path3 = '/home/rouyrrerodolphe/Bureau/{0}/SCORES/'.format(championnat)
    
    nbButsDom = []
    nbButsExt = []
    nbButsTot = []
    nbMatchs = []
    fichiers = []
    diffDE = []
    for i in range(len(glob.glob('{0}/*' .format(path3)))):
        nbButsDom.append(['0'])
        nbButsExt.append(['0'])
        nbButsTot.append(['0'])
        nbMatchs.append(['0'])
        nbButsDom[i], nbButsExt[i], nbButsTot[i], nbMatchs[i] = nbButs(glob.glob('{0}/*' .format(path3))[i])
        fichiers.append(glob.glob('{0}/*' .format(path3))[i])
        diffDE.append(nbButsDom[i] - nbButsExt[i])
        
    dfButs = pd.DataFrame({'fichiers' : fichiers, 'butsDom' : nbButsDom,
                       'butsTot' : nbButsTot, 'butsExt' : nbButsExt, 
                       'nbMatchs' : nbMatchs, 'diff' : diffDE})
    
    
    os.chdir('/home/rouyrrerodolphe/Bureau/PROJET PS/{0}/' .format(championnat))
    
    fig, ax = plt.subplots()
    plt.plot(dfButs.index, dfButs['butsTot'])
    fig.savefig('Buts_par_match_{0}.png' .format(championnat), dpi=fig.dpi, bbox_inches='tight')
    
    
if __name__ == '__main__':
    
    # Test de la fonction porc :
    nomfic = '/home/rouyrrerodolphe/Bureau/LIGUE1/RESULTATS/Resultats_Ligue1_2002-2003.xlsx'
    porcDom, porcNul, porcExt, porcAutres = porc(nomfic)
    
    # Test de la fonction porcAnnnee :
    path = '/home/rouyrrerodolphe/Bureau/LIGUE1/RESULTATS/'
    porcAnnee(path)
    
    
    # Test de la fonction nbButs :
    nomfic = '/home/rouyrrerodolphe/Bureau/LIGUE1/SCORES/Scores_Ligue1_2003-2004.xlsx'
    
    nbBMDom, nbBMExt, nbBMTot, nbMatchs = nbButs(nomfic)
    
    # Test de la fonction ecart :
    df = pd.read_excel(nomfic)
    
    df2 = ecart(df)
    
    # Test des fonctions championnats :    
    championnats = ['LIGUE1', 'PREMIER LEAGUE', 'BUNDESLIGA', 'LIGA', 'SERIE A']
    
    for j in range(len(championnats)):
        championnatResultats(championnats[j])
        championnatScores(championnats[j])
        
    
        