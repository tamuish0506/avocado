# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns  # visualization tool
from subprocess import check_output

avocado = pd.read_csv("desktop/DataExploration/Avocado/avocado.csv")

avocado.info() 
# data type and no missing values in each column
avocado.head(20)
avocado.tail(20)
avocado.describe()
avocado.shape

regiondict = {}
for reg in avocado['region']:
    regiondict[reg] = pd.DataFrame()
##    following code is same as above
##    regiondict = {reg : pd.DataFrame for reg in regions}

for key in regiondict.keys():
    regiondict[key] = avocado[:][avocado.region == key]

regiondict['NewYork'].describe()
regiondict['DallasFtWorth'].describe()

avocado['region'].unique()

avocado['region'].value_counts()
# numbers of observations at each region are equal
print("Nunique regions:", avocado['region'].nunique())

# Assign cities to states
dictionary={"Albany":"New York","Atlanta":"Georgia",
            "BaltimoreWashington":"Maryland","Boise":"Idaho",
            "Boston":"Massachusetts","BuffaloRochester":"Pennsylvania",
            "California":"California","Charlotte":"North Carolina",
            "Chicago":"Illinois","CincinnatiDayton":"Ohio","Columbus":"Ohio",
            "DallasFtWorth":"Texas","Denver":"Colorado", "Detroit":"Michigan",
            "GrandRapids":"Michigan",
            "HarrisburgScranton":"Pennsylvania",
            "HartfordSpringfield":"Massachusetts","Houston":"Texas",
            "Indianapolis":"Indiana","Jacksonville":"Florida",
            "LasVegas":"Nevada","LosAngeles":"California",
            "Louisville":"Kentucky","MiamiFtLauderdale":"Florida",
            "Midsouth":"Tennessee","Nashville":"Tennessee",
            "NewOrleansMobile":"Louisiana","NewYork":"New York",
            "NorthernNewEngland":"Massachusetts","Orlando":"Florida",
            "Philadelphia":"Pennsylvania","PhoenixTucson":"Arizona",
            "Pittsburgh":"Pennsylvania","Plains": "GreatPlains", 
            "RaleighGreensboro":"RaleighGreensboro",
            "Portland":"Oregon","RichmondNorfolk":"Virginia","Roanoke":"Virginia",
            "Sacramento":"California","SanDiego":"California","SanFrancisco":"California",
            "Seattle":"Washington","SouthCarolina":"South Carolina",
            "Spokane":"Washington","StLouis":"Missouri","Syracuse":"New York",
            "Tampa":"Florida","WestTexNewMexico":"New Mexico"}

# adding a column as State after region
avocado["State"]=avocado["region"].map(dictionary)
regions= avocado['region'].unique()
regions=pd.DataFrame(regions)
avocado['State'].value_counts(dropna=False)
#counted by State including null values

avocado.info()
# missing values in State are from GreatLakes,Midsouth, Northeast, Plains, SouthCentral,
# Southeast, TotalUS and West.

# correlation of features
avocado.corr()
f,ax = plt.subplots(figsize=(15, 15))
sns.heatmap(avocado.corr(), annot=True, linewidths=.4, fmt= '.2f',ax=ax)
plt.show()

# histogram of average price
avocado.AveragePrice.plot(kind = 'hist',bins = 50,figsize = (10,10))
plt.xlabel("Average Prices")
plt.ylabel("Counts")
plt.show()

# how is average price distributed by type and year?
avocado.boxplot(column='AveragePrice',by='type')
avocado.boxplot(column='AveragePrice',by='year')
avocado.boxplot(column='AveragePrice',by='region') #messy but evident!
avocado.boxplot(column='AveragePrice',by='State')

# average price, group by avocado type
avocado['type'].unique()
avocado.groupby(['type'])['AveragePrice'].mean()
# average price, group by region and State
avocado['region'].unique()
avocado.groupby(['region'])['AveragePrice'].mean()
# average price in different regions
plt.figure(figsize=(20,8))
plt.plot(avocado.groupby(['region'])['AveragePrice'].mean())
plt.xticks(rotation=90)
plt.show()

avocado['State'].unique()
avocado.groupby(['State'])['AveragePrice'].mean()

# average price vs region and year
avocado.groupby(['region','type', 'year'])['AveragePrice'].mean()
# Average price in 2018 is lower than that in 2017 because data in 2018 was not
# obtained from the whole year.

# Rank avocado price w/ different types in each region
avocado.groupby(['region','type'])['AveragePrice'].mean().unstack().sort_values(by='organic', ascending=False)
avocado.groupby(['region','type'])['AveragePrice'].mean().unstack().sort_values(by='conventional', ascending=False)

avocadoorg= avocado[avocado.type == 'organic']
avocadocon= avocado[avocado.type == 'conventional']
mean_price_conv_dict={}
mean_price_org_dict={}
for yr in years:
    mean_price_org_dict[yr]= avocadoorg [ avocadoorg.year == yr ] .AveragePrice.mean()
    mean_price_conv_dict[yr]= avocadocon [ avocadocon.year == yr ] .AveragePrice.mean()

print("Organic: ", mean_price_org_dict)
print("Conventional: ",mean_price_conv_dict)

lists = sorted(mean_price_org_dict.items()) # sorted by key, return a list of tuples
x, y = zip(*lists) # unpack a list of pairs into two tuples
line1= plt.plot(x, y, label= 'organic')

lists2 = sorted(mean_price_conv_dict.items()) # sorted by key, return a list of tuples
x2, y2 = zip(*lists2) # unpack a list of pairs into two tuples
line2= plt.plot(x2, y2, label= 'conventional')

plt.xlabel('Years')
plt.ylabel('Mean Price')
plt.xticks(years)
plt.legend()
plt.title('Comparision between mean price of organic and conventional avocados')
plt.show()

# average prices in different bag sizes
avocado.plot.scatter(x='Small Bags', y='AveragePrice',c='Green')
avocado.plot.scatter(x='Large Bags', y='AveragePrice',c='Blue')
avocado.plot.scatter(x='XLarge Bags', y='AveragePrice',c='Red')    
# The prices tends to be a little bit higher when the quantity is small and as 
# the number of bags increases they tends to foloow a line/trend

avocado.groupby('region')['Total Volume'].mean().sort_values()

# amount distribution in each year
avocado.plot(kind='scatter', x='year', y='Total Volume', alpha=0.5, color='r')
plt.xlabel('YEAR')
plt.ylabel('VOLUME')
plt.title("YEARLY VOLUME SCATTER")

# total volume changes in each year
years= avocado.year.unique()
plt.plot( avocado.groupby('year')['Total Volume'].sum())
plt.title('Yearly Volume')
plt.xlabel('Year', fontsize=14)
plt.xticks(years)
plt.ylabel('Total Volume', fontsize=14)
plt.show()

