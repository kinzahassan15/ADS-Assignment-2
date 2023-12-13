#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
def load_and_transform_data(filepath):
    # Loading the original DataFrame
    df_original = pd.read_csv(filepath, skiprows=4)
    #Transposing the DataFrame to get countries as columns
    df_transposed = df_original.set_index(['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']).transpose()
    #Resetting the index to make the years a column instead of an index
    df_transposed.reset_index(inplace=True)
    #Renaming the 'index' column to 'Year'
    df_transposed.rename(columns={'index': 'Year'}, inplace=True)
    #Converting 'Year' to numeric
    df_transposed['Year'] = pd.to_numeric(df_transposed['Year'], errors='coerce')
    return df_original, df_transposed
def extract_specific_data(df_original, countries, indicators, start_year, end_year):
    """
    Extracts and returns data for specific countries, indicators, and years.
    """
    # Filtering for the specified countries and indicators
    filtered_df = df_original[(df_original['Country Code'].isin(countries)) & 
                              (df_original['Indicator Code'].isin(indicators))]
    # Selecting the range of years
    years = [str(year) for year in range(int(start_year), int(end_year) + 1)]
    return filtered_df[['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'] + years]
file_path = 'C:\\Users\\LENOVO\\Downloads\\API_19_DS2_en_csv_v2_5998250.csv'
df_original, df_transposed = load_and_transform_data(file_path)
#Defining countries, indicators, and years
countries = ['AFG', 'ARB']
indicators = ['SP.POP.TOTL', 'AG.LND.AGRI.ZS']
start_year = '2018'
end_year = '2022'
#Extracting the specific data
specific_data = extract_specific_data(df_original, countries, indicators, start_year, end_year)
print(specific_data)


# In[4]:


total_population = specific_data[specific_data['Indicator Code'] == 'AG.LND.AGRI.ZS']
agri_land = specific_data[specific_data['Indicator Code'] == 'AG.LND.AGRI.ZS']
#Correcting the variable names
total_population_data = total_population.copy()
agri_land_data = agri_land.copy()
years = [str(year) for year in range(2018, 2022)]
#Converting data to numeric
total_population_data[years] = total_population_data[years].apply(pd.to_numeric, errors='coerce')
agri_land_data[years] = agri_land_data[years].apply(pd.to_numeric, errors='coerce')
#Plotting
plt.figure(figsize=(10, 6))
for country in ['AFG', 'ARB']:
    arable_land = total_population_data[total_population_data['Country Code'] == country][years].values[0]
    forest_area = agri_land_data[agri_land_data['Country Code'] == country][years].values[0]
    plt.plot(years, arable_land, label=f'{country} - Total Population')
    plt.plot(years, forest_area, label=f'{country} - Agricultural Land', linestyle='--')
plt.xlabel('Year')
plt.ylabel('Value')
plt.title('Population and Agricultural Land Over Time')
plt.legend()
plt.show()


# In[6]:


year = '2018'
agri_land_2018 = specific_data[(specific_data['Indicator Code'] == 'AG.LND.AGRI.ZS')]
#Extracting values for each country for the selected year
agri_land_values = agri_land_2018[year].apply(pd.to_numeric, errors='coerce').tolist()
country_labels = agri_land_2018['Country Name'].tolist()
#Plotting the pie chart
plt.figure(figsize=(8, 8))
plt.pie(agri_land_values, labels=country_labels, autopct='%1.1f%%')
plt.title(f'Agricultural Land Distribution in {year}')
plt.show()


# In[10]:


years = [str(year) for year in range(2018, 2023)]

# Create a pivot table
pivot_table = pd.pivot_table(specific_data, 
                             values=years, 
                             index=['Country Name', 'Indicator Name'],
                             aggfunc='first')

# Displaying the pivot table
print(pivot_table)

