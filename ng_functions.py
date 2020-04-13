import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import scanpy as sc
import datetime
from itertools import product
import re


def fix_filename(string):
    return re.sub(r'\W', '', str(string).replace(' == ','_').replace(' & ','_').replace(' ', '_'))

def now():
    """spring current date and time as filename-friendly string"""
    return datetime.datetime.now().strftime('%y%m%d_%Hh%M')


def umap_plot(anndata_raw, color : list, vmax = 500, folder='figures', filt='', split_by_cats = '', palette_dictionary = None, dpi=500, norm='log', cmap='viridis', show_fig=True, save_fig=True, return_fig=True, **kwargs):
    
    
    cell_subset_cmap =  {'B cells': '#4666B0',
                         'Basophils': '#4c2e4d',
                         'DC1': '#ff0000',
                         'DC2': '#ff9900',
                         'DC3': '#990000',
                         'Mac1': '#FF9ACC',
                         'Mac2': '#66ffff',
                         'Mac3': '#9966ff',
                         'Mac4': '#33cccc',
                         'Mono1': '#e1e74b',
                         'Mono2': '#6d700f',
                         'Mono3': '#0099ff',
                         'MonoDC': '#00cc00',
                         'N1': '#0a5e75',
                         'N2': '#66ffcc',
                         'N3': '#008055',
                         'N4': '#12a9d3',
                         'N5': '#666699',
                         'N6': '#EE2C7C',
                         'NK cells': '#1F6935',
                         'Plasma_cells': '#c0ff36',
                         'pDC': '#a094ff',
                         'T1' : '#FFD900',
                         'T2' : '#BA0899',
                         'T3' : '#CC263C',
                         'T_CD4': '#0098ff',
                         'T_CD8': '#18ffdd',
                         'T_Calca_?': '#00bcff',
                         'T_Cd163l1_?': '#f50b00',
                         'T_doublet_B': '#6cff89',
                         'T_doublet_Neutro': '#32ffc3',
                         'T_reg': '#0000f5'}

    if palette_dictionary:
        subset_dict = palette_dictionary
    else:
        subset_dict = cell_subset_cmap
    


    
    if filt:
        anndata = anndata_raw[anndata_raw.obs.eval(filt)]
    else:
        anndata = anndata_raw
    
        
    if split_by_cats:
        if type(split_by_cats) == str:

            cat_a = split_by_cats
            queries = ['{} == "{}"'.format(cat_a, x) for x in anndata.obs[cat_a].cat.categories]

        if type(split_by_cats) == list:
            if len(split_by_cats) == 1:

                cat_a = split_by_cats[0]
                queries = ['{} == "{}"'.format(cat_a, x) for x in anndata.obs[cat_a].cat.categories]

            elif len(split_by_cats) == 2:

                cat_a, cat_b = split_by_cats
                queries = {'{} == "{}" & {} == "{}"'.format(cat_a, x, cat_b, y) for x,y in  list(product(anndata.obs[cat_a].cat.categories, anndata.obs[cat_b].cat.categories))}

            else:
                raise('Too many arguments.')
    else: queries = False
    
    
    
    qdict = {}
    
    
    if queries:
        for q in queries:
            qdict[q] = anndata[anndata.obs.eval(q)]

    if len(qdict) == 0:
        qdict[fix_filename(color)] = anndata
        
    qindex = 1
    fig_list = []
    
    
    for qtitle, qdata in qdict.items():
        
        qfig = sc.pl.umap(qdata, 
                   cmap = cmap, 
                   norm = matplotlib.colors.SymLogNorm(linthresh=0.25, base=2),
                   color = color,
                   palette = qdata.obs['minor_subset'].cat.categories.map(subset_dict).tolist(),
                   return_fig=True, **kwargs)


        plt.suptitle(qtitle)
        qfig.set_dpi(dpi)
        
        if save_fig:
            if qtitle != fix_filename(color):
                figtitle = fix_filename(filt) + '_'*(len(filt)!=0) + fix_filename(qtitle) + '_by_' + fix_filename(color)
            else:
                figtitle = fix_filename(filt) + '_'*(len(filt)!=0) + fix_filename(color)

            figname = '{}/{}_{}_{}.pdf'.format(folder, figtitle, now(), qindex)

            qfig.savefig(fname=figname, dpi=dpi, bbox_inches='tight')
            print('{} done!'.format(figname))
        
        
        if show_fig == False:
            plt.close()
        
        qindex += 1
        fig_list.append(qfig)
        
    return fig_list