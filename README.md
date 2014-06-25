minwage
=======

State-level minwage data work

Historical minimum wage data by state taken from [Department of Labor](http://www.dol.gov/whd/state/stateMinWageHis.htm), with FLSA value substituted for all state NAs

State poverty rates are two year moving averages from [Current Population Survey] (https://www.census.gov/hhes/www/poverty/publications/pubs-cps.html) Annual Social and Economic Supplement poverty tables

State unemployment rates from FRED St. Louis Fed queried with pandas.io.data. Series names were of form \[XX\]UR, where XX is a state abbreviation
