import pandas as pd
import numpy as np
from ggplot import *

#do the same things from the r analysis file in this folder,
#but adding vlines to different panels as here:
#http://docs.ggplot2.org/0.9.3.1/geom_vline.html

#Poverty rates by state from source in readme
df_poverty = pd.read_csv('data/state2yrpovrate1993-2010reshaped.csv',
                         na_values = 'NA')

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
def min_wage_change_years(data = df_minwage, state = 'Alabama'):
    sample = data[data['State or other jurisdiction'] == state]
    return sample['Year'][sample['Minimum Wage'].diff() > 0]

print min_wage_change_years()
print df_minwage[df_minwage['State or other jurisdiction'] == 'Alabama']

"""pl = ggplot(df_poverty, aes('Year','2 Yr Moving Average Poverty Rate')) + \
            geom_point() + \
            geom_line() + \
            facet_wrap('State', scales = 'fixed') + \
            theme(axis_text_x = element_text(angle = 90)) + \
            xlab('Year') + \
            ylab('Poverty Rate') + \
            ggtitle('Poverty Rates by State\nVertical Lines Indicate Changes in Minimum Wage')

ggsave(pl,'plots/minwage_small.png')
ggsave(pl,'plots/minwage_vs_poverty.png',height = 30, width = 40,
       limitsize = False)"""
