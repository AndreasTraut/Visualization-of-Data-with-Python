# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:37:32 2021

@author: andre
"""


import streamlit as st
from numpy import array as vector
import matplotlib.pyplot as plot
#from annotated_text import annotated_text


st.title("SEIR Modell")
st.write("Autor: Andreas Traut, Datum: 18.02.2021")
st.write("Siehe: https://de.wikipedia.org/wiki/SEIR-Modell")
"""
Als SEIR-Modell bezeichnet man in der mathematischen Epidemiologie einen Ansatz zur Beschreibung der Ausbreitung von ansteckenden Krankheiten. Die Beschreibung ist näher am realen Verlauf als die des SIR-Modells, da hier berücksichtigt wird, dass ein Individuum nach seiner Infektion nicht sofort selbst infektiös ist. Im Gegensatz zu einem Individuum-basierten Modell ist die Beschreibung makroskopisch, d. h. die Population wird als Gesamtheit betrachtet. 

"""
# Explizites Euler-Verfahren
def euler_method(f,t0,x0,t1,h):
    t = t0; x = x0
    a = [[t,x]]
    for k in range(0,1+int((t1-t0)/h)):
        t = t0 + k*h
        x = x + h*f(t,x)
        a.append([t,x])
    return a

def SEIR_model(beta,gamma,a):
    def f(t,x):
        S,E,I,R = x
        return vector([
            -beta*S*I,
            beta*S*I - a*E,
            a*E - gamma*I,
            gamma*I
        ])
    return f

def SEIR_simulation(beta,gamma,a,E0,I0,days,step=0.1):
    x0 = vector([1.0-E0-I0,E0,I0,0.0])
    return euler_method(SEIR_model(beta,gamma,a),0,x0,days,step)

def diagram(simulation):
    
    plot.style.use('fivethirtyeight')
    figure,axes = plot.subplots()
    figure.subplots_adjust(bottom = 0.15)
    axes.grid(linestyle = ':', linewidth = 2.0, color = "#808080")
    t,x = zip(*simulation())
    S,E,I,R = zip(*x)
    axes.plot(t,S, color = "#0000cc")
    axes.plot(t,E, color = "#ffb000", linestyle = '--')
    axes.plot(t,I, color = "#a00060")
    axes.plot(t,R, color = "#008000", linestyle = '--')
    #plot.show()
    st.pyplot(figure)
  
    

def simulation1():
    N = 83200000 # Einwohnerzahl von Deutschland 2019/2020
    R0 = st.slider('R0 = Basisreproduktionszahl', min_value=0.8, max_value=3.0, value=2.4, step=0.1, format='%f')
    gamma = st.slider('gamma = Gesundungsrate. Der Kehrwert ist die mittlere infektiöse Zeit. ', min_value=0.2, max_value=0.5, value=0.33, step=0.01, format='%f')
    a = st.slider('a = Die mittlere Latenzzeit.', min_value=0.05, max_value=0.3, value=0.18, step=0.01, format='%f')
    days = st.slider('Tage', min_value=100, max_value=200, value=140, step=10, format='%d')
    beta = R0*gamma
    E0 = 40000.0/N
    I0 = 10000.0/N
    return SEIR_simulation(beta, gamma, a, E0, I0, days)

diagram(simulation1)
"""
(Blau) S=Anteil der Anfälligen, engl. susceptible. Noch nicht infiziert
(Gelb) E=Anteil der Exponierten, engl. exposed. Infiziert, aber noch nicht infektiös.
(Magenta) I=Anteil der Infektiösen, engl. infectious.
(Rot) R=Anteil der Erholten, engl. recovered oder resistant. Bzw. verstorben oder nach Symptomen in Quarantäne.
"""
# annotated_text(    
#     ("S", "", "#0000cc"),"S= Anteil der Anfälligen, engl. susceptible. Noch nicht infiziert", 
#     ("E", "", "#ffb000"),"E=Anteil der Exponierten, engl. exposed. Infiziert, aber noch nicht infektiös.", 
#     ("I", "", "#a00060"),"I=Anteil der Infektiösen, engl. infectious.", 
#     ("R", "", "#008000"),"R=Anteil der Erholten, engl. recovered oder resistant. Bzw. verstorben oder nach Symptomen in Quarantäne. ",
# )