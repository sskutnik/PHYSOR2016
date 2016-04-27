import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import re

sns.set(style="ticks",font_scale=1.5)

# Global plot config options
IMAGE_DEST='./images/'
GLOB_COL_WRAP = 2 # number of columns per line for small multiples
OUTPUT_FORMAT = 'pdf'
SHOW_PLOTS = False
DEFAULT_YLIM = [0.4,1.3] # General y-axis limits for all plots

# Isotope function for one or more dataframes
def plotIsos(df_iso, labels, seriesInfo, pltTitle, filename, yLim=DEFAULT_YLIM, legendLoc="best"):

    for idx in range(0,len(labels)):
        # Using .values attribute to handle cases where we exclude the first element (e.g., U-233), which plt.errorbar tries to access
        plt.errorbar(df_iso["Isotope"].index, df_iso[labels[idx]].values,df_iso["Sigma"].values,ls='',**seriesInfo[idx])

    plt.xticks(df_iso.index,df_iso["Isotope"])
    plt.xlim(min(df_iso.index)-1,max(df_iso.index)+1)
    plt.title(pltTitle)
    plt.ylabel("C/E")
    plt.ylim(yLim)
    #plt.ylim(bottom=0.8)
    sns.despine(top=True)
    plt.legend(loc=legendLoc)
    plt.tight_layout()
    if SHOW_PLOTS:
        plt.show()
    else:
        plt.savefig(IMAGE_DEST + filename + '.' + OUTPUT_FORMAT)
        plt.close()


# Isotope regular expression, e.g. "233U"
rxIso = re.compile(r"([0-9]+)([a-zA-Z]+)")
# Fetch out the element identifier
rxEle = re.compile(r"([a-zA-Z]+)-[0-9]+")
df_iso = pd.read_csv('AG536_C2D1.csv')

# Change isotope names to form U-233, etc.
isoNames = []
eleNames = []
for line in df_iso["Isotope"]:
	line = re.sub(rxIso,r'\2-\1',line)
	isoNames.append(line)
	element = re.sub(rxEle,r'\1',line)
	eleNames.append(element)

df_iso["Isotope"] = pd.Series(isoNames)
df_iso["Element"] = pd.Series(eleNames)

# Add an rolling element index (1... N_el for each element); used for plotting
numElements = df_iso.groupby('Element',sort=False).size()
#print(numElements)

#g = sns.factorplot(data=df_iso,col='Element',hue='Element',x='Isotope',y='ORNL C/E',size=4,col_wrap=4)
#g = sns.FacetGrid(data=df_iso,col='Element',hue='Element',size=4,col_wrap=4)
#g.map(plt.scatter,'IsoIndex',"ORNL C/E")

# General column labels for all plots (i.e., series to plot)
labels = ["ORNL C/E","Nominal C/E","E7.1 Nominal C/E","modEu C/E","modEu+Sm C/E", "E7.1 modEu+Sm C/E"]
# Default series meta-info
defaultSeriesInfo = [ { 'markersize':6,'marker':'s','color':'k','markeredgecolor':'k','label':'ORNL (2016)' },
                     { 'markersize':8,'marker':'o','label':'ENDF VII.0 (nominal)' },
                     { 'markersize':8,'marker':'o','label':'ENDF/VII.1 (nominal)' },
                     #                     { 'markersize':8,'marker':'o','markerfacecolor':'w','markeredgewidth':1,'color':'k','label':'ENDF/VII.1' },
                     { 'markersize':8,'marker':'^','label':'VII.0 + mod. Eu-154' },
                     { 'markersize':8,'marker':'v','label':'VII.0 + mod. Eu-154 & Sm-154' },
                     { 'markersize':8,'marker':'^','label':'VII.1 + mod. Eu-154 & Sm-154' },
                     #                     { 'markersize':8,'marker':'^','markerfacecolor':'w','color':'k','markeredgewidth':1,'label':'ENDF/VII.1 + mod. Eu-154 & Sm-154' },
                     ]

# Uranium series
isU = df_iso.loc[(df_iso["Element"] == "U") & ~(df_iso["Isotope"] == "U-233")]
uTitle = "TMI-NJ05YU C2D1: Uranium"
uFilename = "U_CE"

plotIsos(isU, labels, defaultSeriesInfo, uTitle, uFilename )


# Plutonium series
isPu = df_iso.loc[(df_iso["Element"] == "Pu")]
puTitle = "TMI-NJ05YU C2D1: Plutonium"
puFilename = "Pu_CE"

plotIsos(isPu, labels, defaultSeriesInfo, puTitle, puFilename )

	
# MA series
isMA = df_iso.loc[(df_iso["Element"] == "Am") | (df_iso["Element"] == "Np") | (df_iso["Element"] == "Cm")]
maTitle = "TMI-NJ05YU C2D1: Minor actniides"
maFilename = "MA_CE"

plotIsos(isMA, labels[0:4], defaultSeriesInfo[0:4], maTitle, maFilename)

# Cs series
isCs = df_iso.loc[(df_iso["Element"] == "Cs")]
csTitle = "TMI-NJ05YU C2D1: Cesium"
csFilename = "Cs_CE"

plotIsos(isCs, labels, defaultSeriesInfo, csTitle, csFilename, legendLoc="lower left" )

# Eu series
isEu = df_iso.loc[(df_iso["Element"] == "Eu") & (df_iso["Isotope"] != "Eu-152")]

euTitle = "TMI-NJ05YU C2D1: Europium"
euFilename = "Eu_CE"

# FIGURE OUT LINE COLOR of modEu and nominal => reassign back to E7.1 plots!
plotIsos(isEu, labels, defaultSeriesInfo, euTitle, euFilename )

# Zoom in for several Eu evaluations
yLimZoom = [0.9,1.2]
euFilename = "Eu_CE_zoom"
plotIsos(isEu, labels[1:], defaultSeriesInfo[1:], euTitle, euFilename, yLim=yLimZoom )

# Gd series
isGd = df_iso.loc[(df_iso["Element"] == "Gd")]
gdTitle = "TMI-NJ05YU C2D1: Gadolinium"
gdFilename = "Gd_CE"

plotIsos(isGd, labels, defaultSeriesInfo, gdTitle, gdFilename )
	
	
# Sm series
isSm = df_iso.loc[(df_iso["Element"] == "Sm")]
smTitle = "TMI-NJ05YU C2D1: Samarium"
smFilename = "Sm_CE"

plotIsos(isSm, labels, defaultSeriesInfo, smTitle, smFilename )

