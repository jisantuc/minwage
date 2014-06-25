import pandas as pd
import numpy as np
from ggplot import *
import datetime as dt

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'D.C.',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


df_u = pd.read_csv('data/state_u.csv')

#standardizes to mean
df_u['Value'] = df_u['Value']/df_u['Value'].mean()

df_minwage = pd.read_csv('data/minwage.csv',
                         na_values = '...')

#replaces missings with FLSA minwage
for year in pd.unique(df_minwage['Year'].ravel()):
    flsa = float(df_minwage['Value'][df_minwage['State or other jurisdiction'] == 'FLSA'][df_minwage['Year'] == year])
    df_minwage['Value'][df_minwage['Year'] == year] = df_minwage['Value'][df_minwage['Year'] == year].replace(np.nan,flsa)

#replaces bad naming convention for D.C., subs in 'U.S.' for 'FLSA', standardizes to mean
df_minwage['State or other jurisdiction'][df_minwage['State or other jurisdiction'] == 'District of Columbia'] = 'D.C.'
df_minwage['State or other jurisdiction'][df_minwage['State or other jurisdiction'] == 'FLSA'] = 'U.S.'
df_minwage.columns = pd.Index(['State','Date','Value', 'Type'])
df_minwage['Value'] = df_minwage['Value']/df_minwage['Value'].mean()

for a in df_u.index:
    df_u.ix[a,'Date'] = float(df_u.ix[a,'Date'][:4]) + ((float(df_u.ix[a,'Date'][5:7]) - 1)/12)
    df_u.ix[a,'State'] = states[df_u.ix[a,'State']]

#throws 'em into the same df. Which value a line is is indicated by df['Type']
#also converts to numeric or something? I think I added that when I was troubleshooting
#a problem that that doesn't even solve. Ho hum.
df = pd.concat([df_u,df_minwage]).convert_objects(convert_numeric = True)
df = df[df['State'] != 'U.S.']

#df.to_csv('check.csv')

colors = ['#f43605','#0000FF', 'green'] #I have no idea why this has to be three values considering that there are only minimum wage and poverty rate in df['Type'] but whatever

for col in df.columns:
    print type(df.ix[0,col])

pl = ggplot(df, aes('Date','Value', colour = 'factor(Type)')) + \
            scale_colour_manual(values = colors) + \
            geom_line() + \
            facet_wrap('State', scales = 'fixed') + \
            ggtitle('Unemployment Rate and Minimum Wage by State,\nStandardized') + \
            xlim(1988,2006) + \
            theme(axis_text_x = element_text(angle = 0,
                                             vjust = 0,
                                             hjust = 1,
                                             size = 6),
                         axis_text_y = element_text(size = 6)) + \
            ylab('')

ggsave(pl, 'plots/minwage_u_small.png')
ggsave(pl, 'plots/minwage_u.png',height = 30, width = 40,
       limitsize = False)
