import pandas as pd
import numpy as np
from ggplot import *

#do the same things from the r analysis file in this folder,
#but adding vlines to different panels as here:
#http://docs.ggplot2.org/0.9.3.1/geom_vline.html

#Poverty rates by state from source in readme
df_poverty = pd.read_csv('data/state2yrpovrate1993-2010reshaped.csv',
                         na_values = 'NA')
#Fixes obnoxious state labeling
for a in df_poverty.index:
    if df_poverty.ix[a,'State'][-1:] == '.' and df_poverty.ix[a,'State'] != 'D.C.':
        df_poverty.ix[a,'State'] = df_poverty.ix[a,'State'][:-1]

#Minwage dataframe from source in readme
#Use to get vlines dataframe showing when minwage changed by geographic locale
df_minwage = pd.read_csv('data/minwage.csv',
                         na_values = '...')

#replaces all NaNs with FLSA for that year
for year in pd.unique(df_minwage['Year'].ravel()):
    flsa = float(df_minwage['Minimum Wage'][df_minwage['State or other jurisdiction'] == 'FLSA'][df_minwage['Year'] == year])
    df_minwage['Minimum Wage'][df_minwage['Year'] == year] = df_minwage['Minimum Wage'][df_minwage['Year'] == year].replace(np.nan,flsa)


#fixes geographic naming discrepancy between minwage and poverty datasets
df_minwage['State or other jurisdiction'][df_minwage['State or other jurisdiction'] == 'District of Columbia'] = 'D.C.'
df_minwage['State or other jurisdiction'][df_minwage['State or other jurisdiction'] == 'FLSA'] = 'U.S.'


#method to get years in which minimum wage changes occurs for state
def min_wage_change_years(state, data = df_minwage):
    #print state
    sample = data[data['State or other jurisdiction'] == state]
    return list(sample['Year'][sample['Minimum Wage'].diff() > 0])

vlines_data = pd.DataFrame(index = pd.unique(df_poverty['State'].ravel()),
                           columns = ['vlines'])

#gets years in which minimum wage changes in each state
for state in vlines_data.index:
    vlines_data.ix[state,'vlines'] = min_wage_change_years(state = state)

#facet_wrap is going to alphabetize based on state, so reindexing vlines_data to alphabetical version of itself
sorting = list(vlines_data.index)
sorting.sort()
vlines_data = vlines_data.reindex(index = sorting)
vlines_data['vs'] = np.repeat(range(8),8)[:52]
vlines_data['am'] = np.tile(range(7),8)[:52]
vlines_data['z'] = np.tile([1993,1994,1995,1996],13)

#need to reshape vlines_data to one value per row. do that
#by passing an array to np.repeat(obj, [val for val in something or other])

#check that reindexing work
#it does
#print vlines_data

#make the big ol' plot
#to do: add vlines from vlines_data
pl = ggplot(df_poverty, aes('Year','2 Yr Moving Average Poverty Rate')) + \
            geom_line() + \
            facet_wrap('State', scales = 'fixed') + \
            theme(axis_text_x = element_text(angle = 90)) + \
            xlab('Year') + \
            ylab('Poverty Rate') + \
            ggtitle('Poverty Rates by State\nVertical Lines Indicate Changes in Minimum Wage') + \
            xlim(1993,2005) + \
            ylim(0,30)# + \
#            geom_vline(aes(xintercept = 'z', color = 'red',linetype = 'longdash'),vlines_data)
#            geom_point(aes(size = 0.5)) + \



ggsave(pl,'plots/minwage_small.png')
#ggsave(pl,'plots/minwage_vs_poverty.png',height = 30, width = 40,
#       limitsize = False)
