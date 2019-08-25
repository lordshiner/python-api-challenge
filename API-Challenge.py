#!/usr/bin/env python
# coding: utf-8

# # Observable trends:
#     1. The data supports that temperatures closer to the equator are higher.
#     2. There is no observable pattern in relation to wind speed and distance from the equator.
#     3. There is also no observable pattern in relation to humidity and distance from the equator.

# In[25]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import json

# Import API key
from OpenWeatherconfig import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)


# In[47]:


# Check API and preview data
url = "http://api.openweathermap.org/data/2.5/weather?"
params = {"appid" : api_key,"q" : cities[0], "units" : "imperial"}
response = requests.get(url, params=params).json()

print(json.dumps(response, indent=4))


# In[72]:


# Check target measures
lon_test= response["coord"]["lon"]
lat_test = response["coord"]["lat"]
temp_test = response["main"]["temp_max"]
humidity_test = response["main"]["humidity"]
clouds_test = response["clouds"]["all"]
wind_test = response["wind"]["speed"]
country_test = response["sys"]["country"]
date_test = response["dt"]

print(lon_test,lat_test,temp_test,humidity_test, clouds_test, wind_test,country_test,date_test)


# In[111]:


#Perform a weather check on each city using a series of successive API calls.
#Include a print log of each city as it's being processed (with the city number and city name).
lon = []
lat = []
temp = []
humidity = []
clouds = []
wind = []
country = []
date = []
error_counter = 0
error_city = []
missed_records = 0
cityCNT = len(cities)
captured_cities = cityCNT-missed_records

print("Beginning Data Retrieval")

for place in cities:
    list_size = str(len(temp)+1)
    params["q"] = place
    c = params["q"]
    response2 = requests.get(url, params=params).json()
    time.sleep(1)
    error_counter = 0
    error_city = []
    try:
        print(f"Attempting record {list_size}, for city {c}.")
        lon2 = response2["coord"]["lon"]
        lat2 = response2["coord"]["lat"]
        temp2 = response2["main"]["temp_max"]
        hum2 = response2["main"]["humidity"]
        cld2 = response2["clouds"]["all"]
        spd2 = response2["wind"]["speed"]
        cntry2 = response2["sys"]["country"]
        date2 = response2["dt"]
                
    except:
        error_city.append(place)
        for attempt in range (0,4):
            error_counter = error_counter + 1
            params["q"] = error_city[0]
            c2 = params["q"]
            if error_counter <= 3:
                time.sleep(3)
                params["q"] = error_city[0]
                print(f"  Update attempt failed, attempt number {str(error_counter)}.")
                try:
                    lon3 = response2["coord"]["lon"]
                    lat3 = response2["coord"]["lat"]
                    temp3 = response2["main"]["temp_max"]
                    hum3 = response2["main"]["humidity"]
                    cld3 = response2["clouds"]["all"]
                    spd3 = response2["wind"]["speed"]
                    cntry3 = response2["sys"]["country"]
                    date3 = response2["dt"]
                except:
                    continue
                else:
                    print(f" Updating {c2}, record {list_size} item 1.")
                    temp.append(temp3)
                    print(f" Updating {c2}, record {list_size} item 2.")      
                    humidity.append(hum3)
                    print(f" Updating {c2}, record {list_size} item 3.")
                    clouds.append(cld3)
                    print(f" Updating {c2}, record {list_size} item 4.")
                    wind.append(spd3) 
                    print(f" Updating {c2}, record {list_size} item 5.")
                    country.append(cntry3)
                    print(f" Updating {c2}, record {list_size} item 6.")
                    date.append(date3)
                    print(f" Updating {c2}, record {list_size} item 7.")
                    lon.append(lon3)
                    print(f" Updating {c2}, record {list_size} item 8.")
                    lat.append(lat3)
                    error_counter = 10
            elif error_counter < 9:
                print(f"     Max attempts reached. {c2}, record {list_size} item 1 - 8 is NaN.")
                temp.append("NaN")
                humidity.append("NaN")
                clouds.append("NaN")
                wind.append("NaN")
                country.append("NaN")
                date.append("NaN")
                lon.append("NaN")
                lat.append("NaN")
                error_counter = 10
                missed_records = missed_records + 1
    else:
        print(f" Updating {c}, record {list_size} item 1.")
        temp.append(temp2)
        print(f" Updating {c}, record {list_size} item 2.")      
        humidity.append(hum2)
        print(f" Updating {c}, record {list_size} item 3.")
        clouds.append(cld2)
        print(f" Updating {c}, record {list_size} item 4.")
        wind.append(spd2)
        print(f" Updating {c}, record {list_size} item 5.")
        country.append(cntry2)
        print(f" Updating {c}, record {list_size} item 6.")
        date.append(date2)
        print(f" Updating {c}, record {list_size} item 7.")
        lon.append(lon2)
        print(f" Updating {c}, record {list_size} item 8.")
        lat.append(lat2)
                    
print("Data Retrieval Complete")
if len(temp) == len(humidity) and len(temp) == len(clouds) and len(temp) == len(wind) and len(temp) == len(cities):
    print("Data Check: PASS")
    print(f"Non-Responsive cities: {str(missed_records)}")
    print(f"Total captured cities: {str(captured_cities)}")
else:
    print("Data Check: FAIL")
    print("Fail Reason: Missing Data Elements")


# In[112]:


#Export the city data into a .csv.
city_data = pd.DataFrame({"City" : cities,
                          "Cloudiness" : clouds,
                          "Country" : country,
                          "Date" : date,
                          "Humidity" : humidity,
                          "Lat" : lat,
                          "Lng" : lon,
                          "Max Temp" : temp,
                          "Wind Speed" : wind})
city_data.to_csv(output_data_file, index=False, header=True)

#Display the DataFrame
city_data.head(5)


# In[169]:


# Clean & Sort data

df = city_data.replace("NaN", np.nan, inplace = True)
df = city_data.dropna(how='any', inplace=False)
df = df.apply(pd.to_numeric, errors='ignore')
df["Date"] = pd.to_datetime(df["Date"], unit = 's')
df["Date"] = df["Date"].dt.date
df = df.sort_values("Lat", ascending = False).reset_index(drop=True)
m_date = df['Date'].max()
max_date = m_date.strftime('%m/%d/%Y')

df.head()


# In[171]:


#Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
#Latitude vs. Temperature Plot

df1 = df[["Max Temp","Lat"]]
plt.xticks(np.arange(-80,80,20))
plt.yticks(np.arange(df1["Max Temp"].min()-5,df1["Max Temp"].max()+5, 10))
plt.scatter(df1["Lat"], df1["Max Temp"])
plt.grid()
plt.title(f"City Latitude vs. Max Temperature ({max_date})")
plt.xlabel("Latitude")
plt.ylabel("Max Temperature (F)")
plt.tight_layout()
plt.show()
#Save the plotted figures as .pngs.
plt.savefig("output_data/TempPlot.png")


# In[172]:


#Latitude vs. Humidity Plot
df2 = df[["Humidity","Lat"]]
plt.xticks(np.arange(-80,80,20))
plt.yticks(np.arange(df2["Humidity"].min()-5,df2["Humidity"].max()+5, 10))
plt.scatter(df2["Lat"], df2["Humidity"])
plt.grid()
plt.title(f"City Latitude vs. Humidity ({max_date})")
plt.xlabel("Latitude")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.show()
#Save the plotted figures as .pngs.
plt.savefig("output_data/HumidityPlot.png")


# In[173]:


#Latitude vs. Cloudiness Plot
df3 = df[["Cloudiness","Lat"]]
plt.xticks(np.arange(-80,80,20))
plt.yticks(np.arange(df3["Cloudiness"].min()-5,df3["Cloudiness"].max()+5, 10))
plt.scatter(df3["Lat"], df3["Cloudiness"])
plt.grid()
plt.title(f"City Latitude vs. Cloudiness ({max_date})")
plt.xlabel("Latitude")
plt.ylabel("Cloudiness (%)")
plt.tight_layout()
plt.show()
#Save the plotted figures as .pngs.
plt.savefig("output_data/CloudinessPlot.png")


# In[174]:


#Latitude vs. Wind Speed Plot
df4 = df[["Wind Speed","Lat"]]
plt.xticks(np.arange(-80,80,20))
plt.yticks(np.arange(df4["Wind Speed"].min()-5,df4["Wind Speed"].max()+5, 10))
plt.scatter(df4["Lat"], df4["Wind Speed"])
plt.grid()
plt.title(f"City Latitude vs. Wind Speed ({max_date})")
plt.xlabel("Latitude")
plt.ylabel("Wind Speed (mph)")
plt.tight_layout()
plt.show()
#Save the plotted figures as .pngs.
plt.savefig("output_data/WindSpeedPlot.png")


# In[ ]:




