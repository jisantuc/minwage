import pandas as pd
import numpy as np
from ggplot import *

#do the same things from the r analysis file in this folder,
#but adding vlines to different panels as here:
#http://docs.ggplot2.org/0.9.3.1/geom_vline.html

df_poverty = pd.read_csv('data/state2yrpovrate1993-2010reshaped.csv',
                         na_values = 'NA')

pl = ggplot(df_poverty, aes('Year','2 Yr Moving Average Poverty Rate')) + \
            geom_point() + \
            geom_line() + \
            facet_wrap('State')

print pl
