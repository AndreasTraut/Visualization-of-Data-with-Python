# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 18:46:07 2020

In this example I downloaded my complete history of played songs since 2016 
from www.last.fm (66'955 songs in total) and re-built some of these nice 
statistics and figues, which last.fm provides. This are for example a bar-plot 
with monthly aggregates of total played songs. Or top 10 songs of the week and
so on. Having the same plots at the end as last.fm has prooves, that my
results are correct. :-)

@author: Andreas Traut
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot

#%%
df = pd.read_csv('lastfm_data.csv', 
                 names=['artist', 'album','song', 'timestamp'], 
                 converters={'timestamp':pd.to_datetime})
#%% Extracting year/month/... from timestamp and adding as new columns
dates = pd.DatetimeIndex(df['timestamp'])
df['year'] = dates.year
df['month'] = dates.month
df['weekofyear'] = dates.weekofyear
df['hour']= dates.hour
df['weekday'] = dates.weekday   #Monday=0

#%% Overall statistics
# Next I wanted to have the overall statistics as for example # "played songs 
# per year" or "scrobbels per day".
print("\nPlayed songs per year:\n{}".format(df['year'].value_counts(sort=False)))
print("\nScrobbels per day:\n{}".format(df['year'].value_counts(sort=False)/365.))

# Now lets examine the "top artist", "top album", "top songs":
print("\nTop artists:\n{}".format(df['artist'].value_counts().head()))
print("\nTop album:\n{}".format(df['album'].value_counts().head()))
print("\nTop songs:\n{}".format(df['song'].value_counts().head(10)))

#%% Defining a year/mont/weekofyear for examination
myYear = 2017
myMonth = 5
myWeekofYear = 21

#%% Examine selected year 
print("\nAll songs in year %s:\n"%(myYear), df.loc[df['year'] == myYear, ['artist', 'album', 'song']])
selection = df.loc[df['year'] == myYear, ['artist', 'album', 'song', 'month']]
selectionPrev = df.loc[df['year'] == myYear-1, ['artist', 'album', 'song', 'month']]
print("\nTop artists:\n{}".format(selection['artist'].value_counts().head()))
print("\nTop songs:\n{}".format(selection['song'].value_counts().head(10)))

perMonth = selection['month'].value_counts().sort_index()
perMonthPrev = selectionPrev['month'].value_counts().sort_index()
print("\nScrobbels per month in {}:\n{}".format(myYear, perMonth))
print("\nScrobbels per month in {}:\n{}".format(myYear-1, perMonthPrev))

index = np.arange(12)
pltperMonth = pyplot.bar(index, perMonth, width=0.3, label=myYear, color='red')
pltperMonthPrev = pyplot.bar(index - 0.3, perMonthPrev, width=0.3, label=myYear-1, color='peachpuff')
pyplot.title('Year {}. Scrobbels per month.'.format(myYear))
pyplot.xticks(index, ('Jan', 'Feb', 'Mär', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez'))
pyplot.legend()
pyplot.show()

isyear = (df['year'] == myYear)
ismonth =  (df['month'] == myMonth)
selection = df.loc[isyear & ismonth, ['artist', 'album', 'song', 'timestamp']]
print ("\nOnly month {} in {}:\n{}".format(myMonth, myYear, selection))
print("\nTop Artists in {}/{}:\n{}".format(myMonth, myYear, selection['artist'].value_counts().head()))
print("\nTop Songs in {}/{}:\n{}".format(myMonth, myYear, selection['song'].value_counts().head(10)))

# isweekofyear= (df['weekofyear'] == myWeekofYear)
# selection = df.loc[isyear & isweekofyear, ['hour']]

#%% All songs afterDateX and beforeDateY
X = '2018-12-20' 
Y = '2018-12-31'
print("\nSongs played between %s and %s:" %(X, Y))
afterDateX = df['timestamp'] >= X 
beforeDateY = df['timestamp'] <= Y 
print(df.loc[afterDateX & beforeDateY, ['artist', 'album', 'song']])

#%% Listening clock
isweekofyear= (df['weekofyear'] == myWeekofYear)
selection = df.loc[isyear & isweekofyear, ['hour']]
#selection = df.loc[df['year'] == myYear, ['artist', 'album', 'song', 'month', 'hour', 'year']]
index = np.arange(24)
perHour = myselection['hour'].value_counts().sort_index()
pltperHour = pyplot.subplot(111)#, projection='polar')
# pltperHour.set_theta_zero_location("N")
pltperHour.bar(perHour.index, perHour, width=0.3, color='blue', alpha=0.5)
#pltperHour.set_xticklabels(['00', '', '18', '', '12', '', '06', ''])
pltperHour.set_xticks(index)
pyplot.title('Year {}, Week-of-Year {}. Scrobbels per hour.'.format(myYear, myWeekofYear))
pyplot.show()

