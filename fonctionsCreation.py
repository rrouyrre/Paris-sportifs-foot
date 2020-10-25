#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:46:30 2020

@author: rouyrrerodolphe
"""


import pandas as pd
import numpy as np
import glob


""" Fichier contenant les fonctions necessaires a la creation des fichiers de 
    donnees.
"""


def score(df):
    """Fonction qui retourne un dataframe contenant les scores séparés en 2 colonnes,
    à partir d'un fichier du dossier WIKIPEDIA contenant les scores en 1 colonne.
    """
    
    df2 = pd.DataFrame()
    for j in range(len(df)):
        if j == 0 :
            df2[j] = df[j] # La première colonne comporte le nom des clubs et ne change pas
            df2[j+1] = np.zeros(len(df)) # On remplit la deuxième colonne de zéros
        else :
            new = df[j].str.split('-', expand=True) # On sépare les scores avec split
            # new est un tableau à 2 colonnes
            new = new.apply(pd.to_numeric, errors='coerce')  
            new = new.dropna()
            # Permet de ne pas traiter les cas particuliers 
            df2[2*j] = new[0]
            df2[2*j+1] = new[1]   
    
    return df2


def resultat(df2):
    """Fonction qui retourne un dataframe contenant les resultats des matchs 
    (domicile/nul/exterieur) à partir d'un dataframe contenant les scores 
    separes en 2 colonnes.     
    """
    
    df3 = pd.DataFrame()
    for k in range(len(df2)):
        if k == 0 :
            df3[k] = df2[k] # La première colonne reste le nom des clubs
        else :
            # On traduit les scores en résultats
            # La deuxième colonne n'est jamais prise en compte
            df3[k] = np.zeros(len(df2))
            df3[k] = np.where(df2[2*k]>df2[2*k+1], 'Domicile', df3[k])
            df3[k] = np.where(df2[2*k]==df2[2*k+1], 'Nul', df3[k])
            df3[k] = np.where(df2[2*k]<df2[2*k+1], 'Extérieur', df3[k])
           
    return df3

def grosDataFrame(path):

    df4 = pd.DataFrame() 
    for i in range(len(glob.glob('{0}/*' .format(path)))):
        df5 = pd.read_excel(glob.glob('{0}/*' .format(path))[i])
        df4 = df4.append(df5)
    df4.to_excel('Gros_DataFrame.xlsx')
    
    
if __name__ == '__main__':
    
    df = pd.read_excel('/home/rouyrrerodolphe/Bureau/LIGUE1/WIKIPEDIA/Ligue1_2000-2001.xlsx')
    
    # Test de la fonction score :
    df2 = score(df)
    
    # Test de la fonction resultat :
    df3 = resultat(df2)
    
    # Test de la fonction grosDataFrame :
    path = '/home/rouyrrerodolphe/Bureau/LIGUE1/RESULTATS/'
    grosDataFrame(path)
        
    
    
    
    
    
