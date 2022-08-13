# import libraries
import pandas as pd
from scipy.stats import norm
import scipy.integrate as integrate
from numpy import inf, sqrt, pi, exp
import matplotlib.pyplot as plt

# import data
distribution = pd.read_excel("Data_Scientist_assigment_Backround_data.xlsx", sheet_name = "Table 1")
monthly = pd.read_excel("Data_Scientist_assigment_Backround_data.xlsx", sheet_name = "Table 2")

# rename the unnamed column in monthly
monthly.rename(columns = {"Unnamed: 0": "month"}, inplace = True)

# Q1: How would you go about calculating the total harvestable biomass (fish larger than 4kg) for these months?
# First, calculate mean weight for each month and add as a new column
monthly['Average weight'] = round(monthly["Biomass"] / monthly["Number of individuals"], 1)

# turn the columns into the same number of decimal and data type
distribution['Average weight'] = round(distribution['Average weight'], 1).astype('float64')
monthly['Average weight'] = monthly['Average weight'].astype('float64')

# get the corresponding distribution as a new column
monthly_c = pd.merge(monthly, distribution, on = 'Average weight', how = 'left')

# calculate harvestable biomass for each month
# initialize output
harvest = []
# iterate over each month, and get the number of harvestable biomass
for i in range(len(monthly_c)):
    avg_weight = monthly_c.loc[i, 'Average weight']
    std = monthly_c.loc[i, "std (σ)"]
    bio = monthly_c.loc[i, "Biomass"]
    n = monthly_c.loc[i, "Number of individuals"]
    # integrate the function of normal distribution * x over 4 to inf
    result = integrate.quad(lambda x: x * n/(std * sqrt(2*pi)) * exp(-0.5*((x-avg_weight)/std)**2), 4, inf)
    harvest.append(result[0])

# append output list to dataframe
monthly_c["harvest"] = harvest

# visualization
plt.bar(monthly_c['month'], monthly_c['harvest'])

# Q2: What is the average weight of these (harvestable) fish?
# initialize output
harvest_n = []
# iterate over each month, get cumulative distribution function at 4.0kg
for i in range(len(monthly_c)):
    avg_weight = monthly_c.loc[i, 'Average weight']
    std = monthly_c.loc[i, "std (σ)"]
    n = monthly_c.loc[i, "Number of individuals"]
    cdf = norm(loc = avg_weight, scale = std).cdf(4)
    proportion = 1 - cdf
    hvst_n = n * proportion
    harvest_n.append(hvst_n)

# append output list to dataframe
monthly_c["harvest_n"] = harvest_n
monthly_c["harvest_avg"] = monthly_c["harvest"] / monthly_c["harvest_n"]

# visualization
plt.bar(monthly_c['month'], monthly_c['harvest_avg'])
plt.ylim(4, 5.5)

# Q3: Assuming you only know the biomass and number of individuals at the start of the first
# month (from table 2). Assume a growth rate of 11,2%. How much will be harvested during the next
# 12 months, if we assume that all fish over 4kg will be harvested at the end of each month?

monthly = pd.read_excel("Data_Scientist_assigment_Backround_data.xlsx", sheet_name = "Table 2")
monthly.rename(columns = {"Unnamed: 0": "month"}, inplace = True)
monthly_new = monthly

# start from Feb, each month the growth rate of average weight is 11.2%
monthly_new.loc[0, 'Average weight'] = round(monthly_new.loc[0, "Biomass"] / monthly_new.loc[0, "Number of individuals"], 1)
for i in range(1, len(monthly_new)):
    monthly_new.loc[i, 'Average weight'] = round(monthly_new.loc[i-1, 'Average weight'] * 1.112, 1)

# merge with distribution, get std
distribution['Average weight'] = round(distribution['Average weight'], 1).astype('float64')
monthly_new['Average weight'] = monthly_new['Average weight'].astype('float64')

# get the corresponding distribution as a new column
monthly_newc = pd.merge(monthly_new, distribution, on = 'Average weight', how = 'left')

# get the harvestable biomass and harvestable individuals for Jan
# initialize output
harvest = []
harvest_n = []
# harvestable biomass for Jan
avg_weight = monthly_newc.loc[0, 'Average weight']
std = monthly_newc.loc[0, "std (σ)"]
bio = monthly_newc.loc[0, "Biomass"]
n = monthly_newc.loc[0, "Number of individuals"]
result = integrate.quad(lambda x: x * n/(std * sqrt(2*pi)) * exp(-0.5*((x-avg_weight)/std)**2), 4, inf)
harvest.append(result[0])
# harvestable individuals for Jan
cdf = norm(loc = avg_weight, scale = std).cdf(4)
proportion = 1 - cdf
hvst_n = n * proportion
harvest_n.append(hvst_n)

# interate over Feb to Dec, get harvestable biomass and harvestable individuals for each month
for i in range(1, len(monthly_newc)):
    avg_weight = monthly_newc.loc[i, 'Average weight']
    std = monthly_newc.loc[i, "std (σ)"]
    # number of remaining individuals in the number of individuals minus the harvested individuals last month
    n = monthly_newc.loc[i - 1, "Number of individuals"] - harvest_n[i - 1]
    # multiply number of individuals with avg_weight to get total biomass
    bio = n * avg_weight
    monthly_newc.loc[i, "Number of individuals"] = n
    monthly_newc.loc[i, "Biomass"] = bio
    # get the biomass harvestable
    result = integrate.quad(lambda x: x * n / (std * sqrt(2 * pi)) * exp(-0.5 * ((x - avg_weight) / std) ** 2), 4, inf)
    harvest.append(result[0])

    # get the number of harvestable individuals
    cdf = norm(loc=avg_weight, scale=std).cdf(4)
    proportion = 1 - cdf
    hvst_n = n * proportion
    harvest_n.append(hvst_n)

monthly_newc["harvest_n"] = harvest_n
monthly_newc["harvest"] = harvest
monthly_newc["harvest_avg"] = monthly_newc["harvest"] / monthly_newc["harvest_n"]

# visualization
plt.bar(monthly_newc['month'], monthly_c['harvest'])

print("Total havestable biomass is ", int(monthly_newc['harvest'].sum()), 'kg')