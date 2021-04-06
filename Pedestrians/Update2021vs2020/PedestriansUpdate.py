# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:46:07 2020

@author: andre
"""
import pandas as pd
from matplotlib import pyplot, dates
import seaborn as sns
import glob
import numpy as np

#%% read all files
all_files = glob.glob("*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, sep=';')
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

#%% convert and extract "date-times"
df['datenum'] = dates.datestr2num(df['time of measurement'])
df['date'] = df['time of measurement'].apply(pd.to_datetime, errors='coerce', utc=True)
df['weekofyear'] =  df['date'].dt.isocalendar().week
df['weekday'] = pd.DatetimeIndex(df['date']).weekday #Monday=0
df['weekdayname'] = pd.DatetimeIndex(df['date']).day_name()
df['year'] = pd.DatetimeIndex(df['date']).year
df['pedestrianscount'] = df['pedestrians count']

df = df[(df['weekofyear']>=8) & (df['weekofyear']<=13)]

#%% sum of pedestrians per weekday
print(df.groupby(['year', 'weekday','weekdayname'])['pedestrians count'].sum())


#%%
df_grouped=(df.groupby(['year', 'weekofyear', 'weekdayname'], as_index=False).pedestrianscount.
            agg({'pedestrianscount': lambda x: list(x), 'sum': 'sum'}))

#%%
myYear = 2020
g = sns.catplot(x='weekofyear', y='sum', hue='weekdayname', 
            hue_order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
            data=df_grouped[df_grouped['year']==myYear],
            height=6, kind='bar', palette='muted')

g.set(ylim=(0,35000))
g.fig.suptitle("Year {}".format(myYear))


#%%
myYear = 2021
g = sns.catplot(x='weekofyear', y='sum', hue='weekdayname', 
            hue_order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
            data=df_grouped[df_grouped['year']==myYear],
            height=6, kind='bar', palette='muted')

g.set(ylim=(0,35000))
g.fig.suptitle("Year {}".format(myYear))

#%%
myWeek = 12 
myYear = 2021
a = df_grouped[(df_grouped['year']==myYear) & (df_grouped['weekofyear']==myWeek)]['sum']
b = df_grouped[(df_grouped['year']==myYear-1) & (df_grouped['weekofyear']==myWeek)]['sum']

index = np.arange(7)
pltpera= pyplot.bar(index, a, width=0.3, label=myYear, color='red')
pltperb = pyplot.bar(index - 0.3, b, width=0.3, label=myYear-1, color='peachpuff')
pyplot.title('Week {}'.format(myWeek, myYear, myYear-1))
pyplot.xticks(index, ('Monday', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sunday'))
pyplot.legend()
pyplot.show()

#%%

