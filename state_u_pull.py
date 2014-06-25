import pandas as pd
import pandas.io.data as web
import datetime as dt

#oh you know just a dictionary of states and their abbreviations sorta dull
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

#Minwage dataframe from source in readme
df_minwage = pd.read_csv('data/minwage.csv',
                         na_values = '...')

#replaces all NaNs with FLSA for that year
for year in pd.unique(df_minwage['Year'].ravel()):
    flsa = float(df_minwage['Value'][df_minwage['State or other jurisdiction'] == 'FLSA'][df_minwage['Year'] == year])
    df_minwage['Value'][df_minwage['Year'] == year] = df_minwage['Value'][df_minwage['Year'] == year].replace(np.nan,flsa)

#sets start and end dates. because the data are there, Jan. 1 through Dec. 31, 2006
start_date = dt.datetime(1988,1,1)
end_date = dt.datetime(2006,12,31)
df_u = pd.concat([web.DataReader('{0}UR'.format(st), 'fred', start_date, end_date) for st in states.keys()])

df_u.to_csv('check.csv')
