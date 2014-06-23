import pandas as pd
import numpy as np
from ggplot import *

#Poverty rates by state from source in readme
df_poverty = pd.read_csv('data/state2yrpovrate1993-2010reshaped.csv',
                         na_values = 'NA')
#Fixes obnoxious state labeling where states end in periods for some idiotic reason
for a in df_poverty.index:
    if df_poverty.ix[a,'State'][-1:] == '.' and df_poverty.ix[a,'State'] != 'D.C.' and df_poverty.ix[a,'State'] != 'U.S.':
        df_poverty.ix[a,'State'] = df_poverty.ix[a,'State'][:-1]
df_poverty['Value'] = df_poverty['Value']/df_poverty['Value'].mean()

#Minwage dataframe from source in readme
#Use to get vlines dataframe showing when minwage changed by geographic locale
df_minwage = pd.read_csv('data/minwage.csv',
                         na_values = '...')

#replaces all NaNs with FLSA for that year
for year in pd.unique(df_minwage['Year'].ravel()):
    flsa = float(df_minwage['Value'][df_minwage['State or other jurisdiction'] == 'FLSA'][df_minwage['Year'] == year])
    df_minwage['Value'][df_minwage['Year'] == year] = df_minwage['Value'][df_minwage['Year'] == year].replace(np.nan,flsa)


#fixes geographic naming discrepancy between minwage and poverty datasets
df_minwage['State or other jurisdiction'][df_minwage['State or other jurisdiction'] == 'District of Columbia'] = 'D.C.'
df_minwage['State or other jurisdiction'][df_minwage['State or other jurisdiction'] == 'FLSA'] = 'U.S.'
df_minwage.columns = pd.Index(['State','Year','Value', 'Type'])
df_minwage['Value'] = df_minwage['Value']/df_minwage['Value'].mean()

#throws 'em into the same df. Which value a line is is indicated by df['Type']
df = pd.concat([df_poverty,df_minwage])

colors = ['#f43605','#0000FF', 'green'] #I have no idea why this has to be three values considering that there are only minimum wage and poverty rate in df['Type'] but whatever

#make the big ol' plot
pl = ggplot(df, aes('Year','Value', colour = 'factor(Type)')) + \
            scale_colour_manual(values = colors) + \
            geom_line() + \
            facet_wrap('State', scales = 'fixed') + \
            ggtitle('Poverty Rate and Minimum Wage by State') + \
            xlim(1993,2005) + \
            theme(axis_text_x = element_text(angle = 0,
                                             vjust = 0,
                                             hjust = 1,
                                             size = 6),
                         axis_text_y = element_text(size = 6)) + \
            ylab('')
#            xlab('Year') + \
#            ylab('Poverty Rate') + \



ggsave(pl,'plots/minwage_small.png')
ggsave(pl,'plots/minwage_vs_poverty.png',height = 30, width = 40,
       limitsize = False)
