# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 09:43:19 2020

In this example I downloaded the consumer price index from the official 
website (www.statistikdaten.bayern.de) and worked on these data. I needed to 
convert months (e.g. "January") to a valid date. Because of my 
German-Switzerland locale setting I needed to convert and numbers to float 
(which is replacing comma by point). 

Import csv file from the following link and delete first rows (which contain descriptions): 
https://www.statistikdaten.bayern.de/genesis/online?sequenz=statistikTabellen&selectionname=61111
     Code: 61111-202z	
     Inhalt: "Verbraucherpreisindex (2015=100): Bayern, Verbraucherpreise, Monate, Jahre"

@author: Andreas Traut
"""

import pandas as pd
from matplotlib import pyplot, dates
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as mtick
import seaborn as sns
from time import strptime
import locale
locale.setlocale(locale.LC_ALL, '')

#%%
# I have a 'German-Switzerland.1252' locale setting which requires to replace comma by point. 
def myMonthConverter(s): 
    return strptime(s,'%B').tm_mon

def myValueConverter(s):
    return s.replace(',', '.')

def fake_dates(x, pos):
    """ Custom formater to turn floats into e.g., 2016-05-08"""
    return dates.num2date(x).strftime('%Y-%m-%d')

#%%
# Read the csv. Semikolon separated. Encoding=latin-1
# Convert 'month' to numbers and 'value' to floats. 
# Without the encoding="latin-1" would lead to the error message
# UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe4 
df=pd.read_csv('61111-202z-bearbeitet.csv', sep=";", 
                 encoding="latin-1", names=['year', 'month', 'value'],
                 converters={'month':myMonthConverter, 'value': myValueConverter})
#%%
# Convert column 'value' into numerics
df['value'] = df['value'].apply(pd.to_numeric, errors='coerce')
# There is no need to downcast the year to integer, but here is how it would work: 
# df['year'] = df['year'].apply(pd.to_numeric, downcast='integer', errors='coerce')

#%%
# As a next step I created new columns "datenum" and  "date", which I need for the 
# graphics (the regression plot). The column "datenum" is a step, which I needed 
# because of the Seaborn regression plot function "sns.regplot". First the real 
# date (e.g. "1970-01-01") need to be converted to a number (e.g. 719163.0), which 
# is used in the x-Axis of the plot. Then the description of the x-Axis is 
# transformed from 719163.0 back to the real date in a string-format.  
# Create new column 'date' based on 'year' and 'month' and convert to date 
# Create new column 'datenum' as float for being used in the plot
df['date'] = df['year'].astype(str) + "-" + df['month'].astype(str) + "-1"
df['datenum'] = dates.datestr2num(df['date'])
df['date'] = df['date'].apply(pd.to_datetime, errors='coerce')

print(df.dtypes)

#%%
# Color settings
sns.set(color_codes=True)

# Plot 'datenum' (=float) and 'value' (=float)
fig, ax = pyplot.subplots()
sns.regplot('datenum', 'value', data=df, ax=ax)

# Create the x-axis which is 'datenum' converted to %Y-%m-%d
ax.xaxis.set_major_formatter(FuncFormatter(fake_dates))
ax.tick_params(labelrotation=90)
fig.tight_layout()

#%%
#Examine increments (absolute and relative)
df['increment_abs'] = df['value']-df['value'].shift(+1)
df['increment_rel'] = (1-df['value'].shift(+1)/df['value'])*100

#Replace "NaN" by 0
df['increment_abs'].fillna(0, inplace=True)
df['increment_rel'].fillna(0, inplace=True)

figin, axin = pyplot.subplots(2)
axin[0].plot(df['date'], df['increment_abs'])
axin[1].plot(df['date'], df['increment_rel'])

#Range of axis
axin[0].set_ylim([-1.1, +1.1])
axin[1].set_ylim([-1.1, +1.7])

#Title of axis
axin[0].set_title('absolute increment')
axin[1].set_title('relative increment')
for ax in figin.get_axes(): 
    ax.label_outer()

#Format y axis in percent
axin[1].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))


