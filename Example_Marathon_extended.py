# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:33:27 2020
Adapted example based on Book: Van der Plas, see EBook PDF Chapter 4
@author: Andreas Traut
"""
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#%% 1 Read the data. The function "convert" will split the Data after ":"
def convert(s):
    h, m, s = map(int, s.split(':'))
    return pd.Timedelta(hours=h, minutes=m, seconds=s)  #EBook PDF page 350: return pd.datetools.timedelta(...) does not work

data=pd.read_csv('marathon-data_extended.csv', converters={'split':convert, 'final':convert})
print(data.dtypes)

#%% 2 Apply the converter "convert" to transform the hh:mm:ss. 
data['split_sec'] = data['split'] / np.timedelta64(1, 's') #EBook PDF page 351: data['split_sec'] = data['split'].astype(int) / 1E9  does not work
data['final_sec'] = data['final'] / np.timedelta64(1, 's')

#%% 3 Add more colums. 
data['size_to_weight'] = data['size'] / data['weight']
print(data.head())

#%% 4 Doppel-Abbildung (Punktewolke mit Histogramm) mit x=size und y=weight
with sns.axes_style('white'):
    g = sns.jointplot("size", "weight", data, kind='hex')
    g.ax_joint.plot(np.linspace(min(data['size']), max(data['size'])), 
                    np.linspace(min(data['weight']), max(data['weight'])), ':k')

#%% 5 Histogram for 'size' and 'weight' (distplot=Distribution Plot) 
sns.distplot(data['size'], kde=False);
plt.show()
sns.distplot(data['weight'], kde=False)

#%% 6 PairGrids with variables 'nationality', 'size', 'final_sec', 'weight'
#   colors for gender (hue) is GreenBlue (GnBu)
g = sns.PairGrid(data, vars=['nationality', 'size', 'final_sec', 'weight'],
                  hue='gender', palette='GnBu_r')
g.map(plt.scatter, alpha=0.8)
g.add_legend();

#%% 7 KernelDensity (kde) for column "size_to_weight" 
sns.kdeplot(data.size_to_weight[data.nationality=='DE'], label='Deutschland', shade=True)
sns.kdeplot(data.size_to_weight[data.nationality=='AU'], label='Österreich', shade=True)
plt.xlabel('size_to_weight');
plt.show()

#%% 8 KernelDensity (kde) for column "weight" 
sns.kdeplot(data.weight[data.nationality=='DE'], label='Deutschland', shade=True)
sns.kdeplot(data.weight[data.nationality=='AU'], label='Österreich', shade=True)
plt.xlabel('size');

#%% 9 Regression Plot for "weight" and "size"
h = sns.lmplot('weight', 'size', hue='nationality', data=data[data.gender=="M"], markers=".")              
h = sns.lmplot('weight', 'size', hue='nationality', data=data[data.gender=="W"], markers=".")              

#%% 10 Violinplot using "size" and "nationality"
men = (data.gender == 'M')
women = (data.gender == 'W')
with sns.axes_style(style=None):
    sns.violinplot("size", "nationality", hue="gender", data=data,
                    split=True, inner="quartile",
                    palette=["lightblue", "lightpink"]);
plt.show()
#%% 11 Violinplot using "weight" and "nationality"
with sns.axes_style(style=None):
    sns.violinplot("weight", "nationality", hue="gender", data=data,
                    split=True, inner="quartile",
                    palette=["lightblue", "lightpink"]);
    
    
