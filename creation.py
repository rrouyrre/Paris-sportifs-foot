#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 23:01:10 2020

@author: rouyrrerodolphe
"""


import urllib
import bs4
import pandas as pd
import os
import fonctionsCreation
import fonctionsCotes
import glob


path = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/WIKIPEDIA'
path2 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/SCORES'
path3 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/RESULTATS'
path4 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/COTES'
url_ligue_1 = []

# On recupere les urls des pages des championnats des années 2000
for i in range(20):
    if i < 9 :
        url_ligue_1.append("https://fr.wikipedia.org/wiki/Championnat_de_France_de_football_200{0}-200{1}"
                  .format(i, i+1))
    elif i == 9 :
        url_ligue_1.append("https://fr.wikipedia.org/wiki/Championnat_de_France_de_football_200{0}-20{1}"
                  .format(i, i+1))
    else:
        url_ligue_1.append("https://fr.wikipedia.org/wiki/Championnat_de_France_de_football_20{0}-20{1}"
                  .format(i, i+1))

for i in range(len(url_ligue_1)):
    request_text = urllib.request.urlopen(url_ligue_1[i]).read()

    page = bs4.BeautifulSoup(request_text, "lxml")
 
    # On selectionne le tableau des resultats
    if i == 0 :        
        html = str(page.findAll('table')[5])
    elif i==1 :
        html = str(page.findAll('table')[6])
    elif i < 5 :
        html = str(page.findAll('table')[7])
    elif i<7 :
        html = str(page.findAll('table')[8])
    elif i<8 :
        html = str(page.findAll('table')[6])
    elif i<9 :
        html = str(page.findAll('table')[7])
    elif i<10 :
        html = str(page.findAll('table')[11])
    elif i<11 :
        html = str(page.findAll('table')[10])
    elif i<16 :
        html = str(page.findAll('table')[7])
    else :
        html = str(page.findAll('table')[8])
    soup = bs4.BeautifulSoup(html, "html.parser")
    rows = []
    
    # On traite le tableau html pour pouvoir inserer son contenu dans un dataframe
    for tr in soup.find_all('tr'):
        cols = []
        for td in tr.find_all(['td', 'th']):
            td_text = td.get_text(strip=True)
            if len(td_text):
                cols.append(td_text)
        rows.append(cols) 
    
    # On ne garde que les scores
    del rows[-1]
    del rows[0]
    df = pd.DataFrame(rows)

    # On enregistre les dataframes dans des fichiers excel
    os.chdir(path)
    if i < 9 :
        df.to_excel('Ligue1_200{0}-200{1}.xlsx' .format(i,i+1))
    elif i == 9 :
        df.to_excel('Ligue1_200{0}-20{1}.xlsx' .format(i,i+1))
    else :
        df.to_excel('Ligue1_20{0}-20{1}.xlsx' .format(i,i+1))
     
        
    # 2eme etape :
    # On sépare les resultats pour avoir les scores 
    df2 = fonctionsCreation.score(df)
 
    # On enregistre les dataframes
    os.chdir(path2)
    if i < 9 :
        df2.to_excel('Scores_Ligue1_200{0}-200{1}.xlsx' .format(i,i+1))
    elif i == 9 :
        df2.to_excel('Scores_Ligue1_200{0}-20{1}.xlsx' .format(i,i+1))
    else :
        df2.to_excel('Scores_Ligue1_20{0}-20{1}.xlsx' .format(i,i+1))
        
        
    # 3eme etape
    # On retranscrit le score en resultat
    df3 = fonctionsCreation.resultat(df2)

    # On enregistre les dataframes        
    os.chdir(path3)
    if i < 9 :
        df3.to_excel('Resultats_Ligue1_200{0}-200{1}.xlsx' .format(i,i+1))
    elif i == 9 :
        df3.to_excel('Resultats_Ligue1_200{0}-20{1}.xlsx' .format(i,i+1))
    else :
        df3.to_excel('Resultats_Ligue1_20{0}-20{1}.xlsx' .format(i,i+1))
        
        
    os.chdir(path4)
    path5 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/BETEXPLORER/'
    for i in range(len(glob.glob('{0}/*' .format(path5)))):
        if i > 1 :
            if i < 9 :
                path6 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/BETEXPLORER/Ligue1_200{0}-200{1}' .format(i,i+1)
                df, df2 = fonctionsCotes.dfFic(path6)
                df.to_excel('Cotes_Ligue1_200{0}-200{1}.xlsx' .format(i,i+1))
            elif i == 9 :
                path6 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/BETEXPLORER/Ligue1_200{0}-20{1}' .format(i,i+1)
                df, df2 = fonctionsCotes.dfFic(path6)
                df.to_excel('Cotes_Ligue1_200{0}-20{1}.xlsx' .format(i,i+1))
            else :
                path6 = '/home/rouyrrerodolphe/Bureau/PROJET PS/LIGUE1/BETEXPLORER/Ligue1_20{0}-20{1}' .format(i,i+1)
                df, df2 = fonctionsCotes.dfFic(path6)
                df.to_excel('Cotes_Ligue1_20{0}-20{1}.xlsx' .format(i,i+1))
            
