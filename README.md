# Data-Scientist-Assignment
The data source for this assignment consists of two tables. We assume that the size of fish is normal distributed. The first table gives 61 normal distributions with different average weights and standard deviations. In table 2, gives the number of fish and total biomass in the cage each month.
The overview of these two tables is shown as

<img src="https://user-images.githubusercontent.com/97944674/184493064-a6abca56-532d-4ed9-9bfc-7db931372b58.png" width="700" height="230">

## Q1: Calculating total harvestable (fish over 4kg) biomass each month
This question was solved by integrating the normal distribution function times the weight of fish from 4 kg to inf. `result = integrate.quad(lambda x: x * n/(std * sqrt(2*pi)) * exp(-0.5*((x-avg_weight)/std)**2), 4, inf)` where x represents weight, n represents total number of individuals in a cage. Result of this question is shown below

<img src="https://user-images.githubusercontent.com/97944674/184493158-46c9d98b-3969-40ca-af0b-e845bde8ceac.png" width="400" height="260">

## Q2: Calculating average weight of harvestable fish each month
First, calculate number of harvestable individuals by finding the percentile of 4kg, `cdf = norm(loc=avg_weight, scale=std).cdf(4)`, then, get the average weight by `total biomass / number of individuals`.
The average weight is plotted as 

<img src="https://user-images.githubusercontent.com/97944674/184493372-aa0fde81-c7fb-4d3f-8a2c-6f49ce428184.png" width="400" height="260">

## Q3: Simulation Calculation
**Assuming you only know the biomass and number of individuals at the start of the first month (from table 2). Assume a growth rate of 11,2%. How much will be harvested during the next 12 months, if we assume that all fish over 4kg will be harvested at the end of each month?**

The average weight of fish grows by 11.2% each month. Number of individuals start from 150677, harvestable fish will be subtracted from this. Multiplying remaining number of individuals by average weight, we can get total biomass this month. Then, 
applying the same method in Q1 and Q2 to get harvestbale biomass and average weight of harvestable fish. The result is shown below, with the total biomass within the 12 months to be 749850 kg

<img src="https://user-images.githubusercontent.com/97944674/184493548-279db325-d9ff-4ecb-97cc-94a1678cff10.png" width="400" height="260">


