# -*- coding: utf-8 -*-


import pandas as pd
from itertools import product


def expand_grid(dictionary):
   return pd.DataFrame([row for row in product(*dictionary.values())], 
                       columns=dictionary.keys())

#------------------------
def color_brutes(sommets,k):
    coloration_aux = pd.DataFrame()
    couleurs = range(k)
    for i in range(len(sommets)) :
        coloration_aux[sommets[i]] = couleurs
    coloration_aux = coloration_aux.to_dict('dict')
    coloration = expand_grid(coloration_aux)
    
    return coloration

#------------------------

def acceptable(coloration,g):
    ''' on suppose que coloration est une liste avec des noms de colonnes identiques identiques aux sommets de g '''
    E = g.edges()
    l = True
    for e in E:
        var0 = e[0]
        var1 = e[1]
        x = (coloration[var0]!=coloration[var1])
        l = (l & x)
    return(l)

#------------------------

def color_acc(g,k):
    sommets = g.vertices()
    coloration = color_brutes(sommets,k)
    accumulateur = []
    for i in range(len(coloration)):
        if acceptable(coloration.iloc[i],g):
            accumulateur.append(i)
    coloration = coloration.iloc[accumulateur]
    
    return coloration

#------------------------

def fusion(A,B):
    C = A.merge(B,how='inner')
    C = C.drop_duplicates()
    
    return C

#-----------------------

def graph_color(g,w):
    #décomposition arborescente
    T = g.treewidth(k=w,certificate=True)
    
    parcours = T.lex_DFS()
    
    sub = g.subgraph(parcours[0])
    coloration = color_acc(sub,w)
    accumulateur = coloration
    
    for t in parcours:
        sub = g.subgraph(t)
        coloration = color_acc(sub,w)
        accumulateur = fusion(accumulateur,coloration)
    
    return accumulateur 

#--------------------------------

def coloration_finale(g,w):
    admissibles = graph_color(g,w)
    admissibles['nb_couleurs'] = admissibles.nunique(1)
    approx_nbchroma = min(admissibles.nb_couleurs)
    admissibles = admissibles[admissibles.nb_couleurs == approx_nbchroma]
    
    return approx_nbchroma, admissibles

#---------------------------------

def coloration_finale2(g,w):
    admissibles = graph_color(g,w)
    admissibles['nb_couleurs'] = admissibles.nunique(1)
    approx_nbchroma = min(admissibles.nb_couleurs)
    val = admissibles.nb_couleurs == approx_nbchroma
    admissibles = admissibles[val]
    
    return approx_nbchroma, admissibles

