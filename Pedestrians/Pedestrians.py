# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 11:46:07 2020

@author: andre
"""
import pandas as pd
from matplotlib import pyplot, dates
import seaborn as sns
from matplotlib.ticker import FuncFormatter
import glob

#%% read all files
all_files = glob.glob("*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0, sep=';')
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

#%% convert and extract "date-times"
df['datenum'] = dates.datestr2num(df['time_of_measurement'])
df['date'] = df['time_of_measurement'].apply(pd.to_datetime, errors='coerce', utc=True)
df['hour']= pd.DatetimeIndex(df['date']).hour
df['minute']= pd.DatetimeIndex(df['date']).minute
# df['weekofyear'] = pd.DatetimeIndex(df['date']).weekofyear
df['weekofyear'] =  df['date'].dt.isocalendar().week
df['weekday'] = pd.DatetimeIndex(df['date']).weekday #Monday=0
df['weekdayname'] = pd.DatetimeIndex(df['date']).day_name()

#%% define methods for printing images
sns.set(color_codes=True)
def fake_dates(x, pos):
    """ Custom formater to turn floats into e.g., 2016-05-08"""
    return dates.num2date(x).strftime('%Y-%m-%d')

def print_image(selection, title):
    fig, ax = pyplot.subplots()
    ax.set_title(title)
    sns.barplot(x=selection['datenum'], y=selection['counted_pedestrians'])
    
    #Create the x-axis which is 'datenum' converted to %Y-%m-%d
    ax.xaxis.set_major_formatter(FuncFormatter(fake_dates))
    ax.tick_params(labelrotation=90)
    fig.tight_layout()
    
#%% print image for the whole period
print_image(df, "all data")
#%% sum of pedestrians per weekday
print(df.groupby(['weekday','weekdayname'])['counted_pedestrians'].sum())

#%% sum of pedestrians per weekday and per week-of-year
print(df.groupby(['weekday','weekdayname','weekofyear']).
      agg( 
          sum_counted_pedestrians=('counted_pedestrians', sum)          
          )
      )
#%%
df_grouped=(df.groupby(['weekofyear', 'weekdayname'], as_index=False).counted_pedestrians.
            agg({'counted_pedestrians': lambda x: list(x), 'sum': 'sum'}))

sns.catplot(x='weekofyear', y='sum', hue='weekdayname', 
            hue_order=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 
            data=df_grouped,
            height=6, kind='bar', palette='muted')

#%% print images for each day
print_image(df.loc[df['weekdayname'] == 'Monday'], "Monday")
print_image(df.loc[df['weekdayname'] == 'Tuesday'], "Tuesday")
print_image(df.loc[df['weekdayname'] == 'Wednesday'], "Wednesday")
print_image(df.loc[df['weekdayname'] == 'Thursday'], "Thursday")
print_image(df.loc[df['weekdayname'] == 'Friday'], "Friday")
print_image(df.loc[df['weekdayname'] == 'Saturday'], "Saturday")
print_image(df.loc[df['weekdayname'] == 'Sunday'], "Sunday")

