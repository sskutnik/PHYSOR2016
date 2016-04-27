import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#sns.set(style="ticks",font_scale=1.5)

# Global plot config options
IMAGE_DEST='./images/'
GLOB_COL_WRAP = 2 # number of columns per line for small multiples
OUTPUT_FORMAT = 'pdf'
SHOW_PLOTS = False
#DEFAULT_YLIM = [0.8,1.1] # General y-axis limits for all plots

# Isotope function for one or more dataframes
def plotDeltaKeff(df, labels, seriesInfo, pltTitle, filename, legendLoc="best"):
   
    for idx in range(0,len(labels)):
       plt.plot(df["Burnup (MWd/MTU)"], df[labels[idx]].values,**seriesInfo[idx])
    
    #plt.xticks(df_iso.index,df_iso["Isotope"])
    #plt.xlim(min(df_iso.index)-1,max(df_iso.index)+1)
    plt.title(pltTitle)
    plt.ylabel(r'$\Delta k_{eff}$ (pcm)')
    plt.xlabel(r'Burnup $\left(\mathrm{\frac{MWd}{MTU}}\right)$')
    # plt.ylim(yLim)
    #plt.ylim(bottom=0.8)
    sns.despine(top=True)
    plt.legend(loc=legendLoc)
    plt.tight_layout()
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.savefig(IMAGE_DEST + filename + '.' + OUTPUT_FORMAT)
        plt.close()

# NEED TO ADD A POWER COLUMN => BURNUP COLUMN => PLOT BY BURNUP
df_keff = pd.read_csv('TMI-1_k-eff.csv')

df_kDelta = df_keff
df_kDelta["ModEu"] = (df_keff["ModEu"]-df_keff["Nominal"])*1E5
df_kDelta["ModEu+Sm"] = (df_keff["ModEu+Sm"]-df_keff["Nominal"])*1E5
df_kDelta["E7.1 ModEu"] = (df_keff["E7.1 ModEu"]-df_keff["E7.1 Nominal"])*1E5
df_kDelta["E7.1 ModEu+Sm"] = (df_keff["E7.1 ModEu+Sm"]-df_keff["E7.1 Nominal"])*1E5

#print(df_keff["E7.1 Nominal"])
# General column labels for all plots (i.e., series to plot)
labels = ["ModEu", "E7.1 ModEu", "ModEu+Sm", "E7.1 ModEu+Sm"]

# Default series meta-info
defaultSeriesInfo = [ { 'markersize':8,'marker':'^','label':'ENDF/VII.0 + mod. Eu-154' },
                      { 'markersize':8,'marker':'^','label':'ENDF/VII.1 + mod. Eu-154' },
                     { 'markersize':8,'marker':'v','label':'ENDF/VII.0 + mod. Eu-154 & Sm-154' },
                     { 'markersize':8,'marker':'v','label':'ENDF/VII.1 + mod. Eu-154 & Sm-154' },
                     ]
plotDeltaKeff(df_kDelta, labels, defaultSeriesInfo, "TMI-NJ05YU Sample C2D1: Effective reactivity change", "C2D1_deltaK")
