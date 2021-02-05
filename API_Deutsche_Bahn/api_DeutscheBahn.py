# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 09:50:56 2020

@author: Andreas Traut

"""

import requests
import json

# You need to put your tokens here. 
# myToken = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Sandbox   
myToken = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' #Produktion
myUrl = 'https://api.deutschebahn.com/fasta/v2'
head = {'Authorization': 'Bearer {}'.format(myToken)}
response = requests.get(myUrl, headers=head) 

#%%
myEquipmentnumber = myUrl + "/facilities/10500702"
response = requests.get(myEquipmentnumber, headers=head) 
# print("Response status code is: ", response.status_code)
result = response.content

result_Eq = response.content
data = json.loads(result_Eq)
print(data["stationnumber"]) 
print(data["equipmentnumber"]) 
# print(data["description"]) 
print (data["stateExplanation"])

#%%
# myStationnumber= myUrl + "/stations/6323" #Ulm
# myStationnumber= myUrl + "/stations/6030"
response = requests.get(myStationnumber, headers=head) 
# print("Response status code is: ", response.status_code)
result = response.content

result_Stat = response.content
data = json.loads(result_Stat)
print("Bahnhof Nummer: ", data["stationnumber"], "Name: ", data["name"]) 
print("Anzahl Aufzüge: ", len(data["facilities"]))
i=0 
while i<len(data["facilities"]):
    t =data["facilities"][i]
    print("Aufzug Nummer", t["equipmentnumber"], ": ", t["stateExplanation"]," -> " 
          "Koordinaten (X=", t["geocoordX"],", Y=", t["geocoordY"], ")")
    i=i+1
    
#%%
# install with: 
# pip intall geopy
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="http")
location = geolocator.reverse("48.39846, 9.98278")
print(location.address)