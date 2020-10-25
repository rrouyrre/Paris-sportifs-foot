#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 11:57:18 2020

@author: rouyrrerodolphe
"""


from pylatex import Document, Section, Figure, Command
from pylatex import Subsection, Tabular 
from pylatex import Math, TikZ, Axis, Plot, Matrix, Alignat 

from pylatex.utils import NoEscape
from pylatex.utils import italic

import os
import pandas as pd
import statsLigue1
import matplotlib.pyplot as plt


def rapport(df,nbMatchs,annee):
    """ La función hace un informe para analizar un curso.
    """
    
    if True:  
        geometry_options = {"tmargin": "1cm", "lmargin": "1cm"} 
        doc = Document(geometry_options=geometry_options)
        
        doc.preamble.append(Command('title', 'Rapport {}' .format(annee)))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(
                r"""\maketitle"""))
        with doc.create(Section('Presentation')): 
            doc.append('Nombre de matchs: {0} \n' .format(nbMatchs))

    os.chdir('/home/rouyrrerodolphe/Bureau/LIGUE1')  
    doc.generate_pdf('Rapport', clean_tex=False, compiler='pdflatex') 
    
    
def rappChamp(championnat):
    
    if True :
        geometry_options = {"tmargin": "1cm", "lmargin": "1cm"} 
        doc = Document(geometry_options=geometry_options)
        
        doc.preamble.append(Command('title', 'Rapport {}' .format(championnat)))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(
                r"""\maketitle"""))
        
        with doc.create(Section('Presentation')): 
            doc.append('Nous allons analyser le championnat de {0} \n' .format(championnat))
        
        with doc.create(Figure(position='h!')) as kitten_pic: 
            kitten_pic.add_image('PorcDom_{0}.png' .format(championnat), width='120px')
           
        with doc.create(Figure(position='h!')) as kitten_pic: 
            kitten_pic.add_image('Buts_par_match_{0}.png' .format(championnat), width='120px')
           
        
    os.chdir('/home/rouyrrerodolphe/Bureau/PROJET PS/{0}' .format(championnat))  
    doc.generate_pdf('Rapport_{0}' .format(championnat), clean_tex=False, compiler='pdflatex') 
        
    
    
    
    
if __name__ == '__main__':
    
    path = '/home/rouyrrerodolphe/Bureau/LIGUE1/SCORES/Scores_Ligue1_2002-2003.xlsx'
    path2 = '/home/rouyrrerodolphe/Bureau/LIGUE1/RESULTATS/Resultats_Ligue1_2002-2003.xlsx'
   
    #df = pd.read_excel(path)
      
    porcDom, porcNul, porcExt, porcAutres = statsLigue1.porc(path2)
    diffDomExt = porcDom - porcExt

    df = pd.DataFrame({'Domicile':porcDom,'Nul':porcNul,'Exterieur':porcExt,
                       'difference dom-ext':diffDomExt}, 
                        index=['pourcentage de victoires'])
    
    fig, ax = plt.subplots()
    df.plot(kind='bar', rot=0)

    
    
    nbBMDom, nbBMExt, nbBMTot, nbMatchs = statsLigue1.nbButs(path)
    diffDE = nbBMDom - nbBMExt
   
    dfButs = pd.DataFrame({'butsDom' : nbBMDom, 'butsTot' : nbBMTot, 
                           'butsExt' : nbBMExt, 
                           'diff' : diffDE}, index=['nombre de buts par match'])
    
    fig, ax = plt.subplots()
    dfButs.plot(kind='bar', rot=0)
    
    
    
    rapport(df,nbMatchs,'2002')

    # Test de la fonction rappChamp :
    
    championnats = ['LIGUE1', 'PREMIER LEAGUE', 'BUNDESLIGA', 
                    'LIGA', 'SERIE A']
    
    for j in range(len(championnats)):
        rappChamp(championnats[j])
        
    
        
    
    
    
    
    
    
    
    