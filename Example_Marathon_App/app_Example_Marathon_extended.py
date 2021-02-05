# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 09:33:27 2020
Adapted example based on Book: Van der Plas, see EBook PDF Chapter 4
@author: Andreas Traut
"""

import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.title("Example Marathon")
st.write("Author: Andreas Traut, Date: 19.11.2020")

#%% 1 Read the data. The function "convert" will split the Data after ":"
def convert(s):
    h, m, s = map(int, s.split(':'))
    return pd.Timedelta(hours=h, minutes=m, seconds=s)  #EBook PDF page 350: return pd.datetools.timedelta(...) does not work

data=pd.read_csv('marathon-data_extended.csv', converters={'split':convert, 'final':convert})
# print(data.dtypes)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # bytes_data = uploaded_file.read()    
    data=pd.read_csv(uploaded_file, converters={'split':convert, 'final':convert})


#%% 2 Apply the converter "convert" to transform the hh:mm:ss. 
data['split_sec'] = data['split'] / np.timedelta64(1, 's') #EBook PDF page 351: data['split_sec'] = data['split'].astype(int) / 1E9  does not work

data['final_sec'] = data['final'] / np.timedelta64(1, 's')

#%% 3 Add more colums. 
data['size_to_weight'] = data['size'] / data['weight']
# print(data.head())
st.write(data)

#%% 4 Doppel-Abbildung (Punktewolke mit Histogramm) mit x=size und y=weight
with sns.axes_style('white'):
    g = sns.jointplot("size", "weight", data, kind='hex')
    g.ax_joint.plot(np.linspace(min(data['size']), max(data['size'])), 
                    np.linspace(min(data['weight']), max(data['weight'])), ':k')
st.pyplot(g)

#%% 5 Histogram for 'size' and 'weight' (distplot=Distribution Plot) 
if st.checkbox('Show Histograms'):
    g = sns.displot(data['size'], kde=False);
    st.pyplot(g)
    # plt.show()
    g = sns.displot(data['weight'], kde=False)
    st.pyplot(g)

#%% 6 PairGrids with variables 'nationality', 'size', 'final_sec', 'weight'
#   colors for gender (hue) is GreenBlue (GnBu)
if st.checkbox('Show Pair Grids'):
    g = sns.PairGrid(data, vars=['nationality', 'size', 'final_sec', 'weight'],
                     hue='gender', palette='GnBu_r')
    g.map(plt.scatter, alpha=0.8)
    g.add_legend();
    st.pyplot(g)

#%% 7 KernelDensity (kde) for column "size_to_weight" 
if st.checkbox('Show Size-to-Weights Kernel Density'):
    fig, ax = plt.subplots() 
    ax1 = sns.kdeplot(data.size_to_weight[data.nationality=='DE'], label='Deutschland', shade=True)
    ax2 = sns.kdeplot(data.size_to_weight[data.nationality=='AU'], label='Österreich', shade=True)
    plt.xlabel('size_to_weight');
    # plt.show()
    st.pyplot(fig)

#%% 8 KernelDensity (kde) for column "weight" 
if st.checkbox('Show German/Austria Kernel Density'):
    fig, ax = plt.subplots() 
    ax1 = sns.kdeplot(data.weight[data.nationality=='DE'], label='Deutschland', shade=True)
    ax2 = sns.kdeplot(data.weight[data.nationality=='AU'], label='Österreich', shade=True)
    plt.xlabel('size');
    # plt.show()
    st.pyplot(fig)

#%% 9 Regression Plot for "weight" and "size"
if st.checkbox('Show Weight-Size Regression Plots'):
    m=sns.lmplot('weight', 'size', hue='nationality', data=data[data.gender=="M"], markers=".")              
    st.pyplot(m)
    w=sns.lmplot('weight', 'size', hue='nationality', data=data[data.gender=="W"], markers=".")              
    st.pyplot(w)
    
#%% 10 Violinplot using "size" and "nationality"
men = (data.gender == 'M')
women = (data.gender == 'W')
if st.checkbox('Show Size-Nationality Violinplot'):
    fig, ax = plt.subplots() 
    with sns.axes_style(style=None):
        ax=sns.violinplot("size", "nationality", hue="gender", data=data,
                          split=True, inner="quartile",
                          palette=["lightblue", "lightpink"]);
        # plt.show()
    st.pyplot(fig)

#%% 11 Violinplot using "weight" and "nationality"
if st.checkbox('Show Weight-Nationality Violinplot'):
    fig, ax = plt.subplots() 
    with sns.axes_style(style=None):
        ax=sns.violinplot("weight", "nationality", hue="gender", data=data,
                          split=True, inner="quartile",
                          palette=["lightblue", "lightpink"]);
    st.pyplot(fig)

