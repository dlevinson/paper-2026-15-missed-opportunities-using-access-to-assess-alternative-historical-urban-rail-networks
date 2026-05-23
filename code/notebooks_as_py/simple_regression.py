# Exported from Simple Regression.ipynb. Outputs removed; execution order preserved where present.


# %% Cell 1
import pandas as pd
csv_path1 = 'C:/Users/m1llz/Downloads/Merged Costs (1.4) - Sheet1.csv'
csv_rail_data1 = pd.read_csv(csv_path1)
csv_rail_data1

# %% Cell 2
print(csv_rail_data1.dtypes)

# %% Cell 3
csv_rail_data1 = csv_rail_data1[csv_rail_data1['TunnelPer'] == '1']
csv_rail_data1

# %% Cell 4
print(csv_rail_data1['City'].unique())

# %% Cell 5
csv_rail_data1 = csv_rail_data1[
    (csv_rail_data1['City'] == 'Istanbul') |
    (csv_rail_data1['City'] == 'Toronto') | 
    (csv_rail_data1['City'] == 'Montreal') | 
    (csv_rail_data1['City'] == 'Seattle') | 
    (csv_rail_data1['City'] == 'Los Angeles') | 
    (csv_rail_data1['City'] == 'San Francisco') | 
    (csv_rail_data1['City'] == 'Sofia') | 
    (csv_rail_data1['City'] == 'Warsaw') | 
    (csv_rail_data1['City'] == 'Bucharest') | 
    (csv_rail_data1['City'] == 'Moscow') | 
    (csv_rail_data1['City'] == 'Nizhniy Novgorod') | 
    (csv_rail_data1['City'] == 'Saint Petersburg') | 
    (csv_rail_data1['City'] == 'Budapest') | 
    (csv_rail_data1['City'] == 'Turin') | 
    (csv_rail_data1['City'] == 'Helsinki') | 
    (csv_rail_data1['City'] == 'Stockholm') | 
    (csv_rail_data1['City'] == 'Milan') | 
    (csv_rail_data1['City'] == 'Leipzig') | 
    (csv_rail_data1['City'] == 'Rome') | 
    (csv_rail_data1['City'] == 'Berlin') | 
    (csv_rail_data1['City'] == 'Copenhagen') | 
    (csv_rail_data1['City'] == 'Oslo') | 
    (csv_rail_data1['City'] == 'Istanbul') | 
    (csv_rail_data1['City'] == 'Melbourne') | 
    (csv_rail_data1['City'] == 'Athens') | 
    (csv_rail_data1['City'] == 'Thessaloniki') | 
    (csv_rail_data1['City'] == 'Busan') | 
    (csv_rail_data1['City'] == 'Paris') |
    (csv_rail_data1['City'] == 'Vienna') |
    (csv_rail_data1['City'] == 'Lisbon') |
    (csv_rail_data1['City'] == 'Madrid') |
    (csv_rail_data1['City'] == 'Karlsruhe') |
    (csv_rail_data1['City'] == 'Dusseldorf') |
    (csv_rail_data1['City'] == 'New York') |
    (csv_rail_data1['City'] == 'Auckland') |
    (csv_rail_data1['City'] == 'Hamburg') |
    (csv_rail_data1['City'] == 'Barcelona') |
    (csv_rail_data1['City'] == 'Lyon') |
    (csv_rail_data1['City'] == 'Osaka') |
    (csv_rail_data1['City'] == 'Tokyo') |
    (csv_rail_data1['City'] == 'Fukuoka') |
    (csv_rail_data1['City'] == 'Kyiv') |
    (csv_rail_data1['City'] == 'Taipei') |
    (csv_rail_data1['City'] == 'Perth') |
    (csv_rail_data1['City'] == 'Nuremberg') |
    (csv_rail_data1['City'] == 'Cologne') |
    (csv_rail_data1['City'] == 'Ankara') |
    (csv_rail_data1['City'] == 'Hong Kong') |
    (csv_rail_data1['City'] == 'Naples') |
    (csv_rail_data1['City'] == 'Belgrade') |
    (csv_rail_data1['City'] == 'Munich') |
    (csv_rail_data1['City'] == 'Łódź') |
    (csv_rail_data1['City'] == 'Prague') |
    (csv_rail_data1['City'] == 'Genova') |
    (csv_rail_data1['City'] == 'Cluj-Napoca')
] 


csv_rail_data1

# %% Cell 6
average_cost = csv_rail_data1['Cost/km (2023 dollars)'].mean()
print(average_cost)

# %% Cell 7
import matplotlib.pyplot as plt

# Histogram
plt.hist(df['cost_per_km'], bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Cost per km (Millions $)')
plt.ylabel('Frequency')
plt.title('Distribution of Rail Construction Costs per km')
plt.show()

# %% Cell 8
Q1 = cost_data.quantile(0.25)
Q3 = cost_data.quantile(0.75)
IQR = Q3 - Q1

# Filter for outliers
outliers = df[(cost_data < (Q1 - 1.5 * IQR)) | (cost_data > (Q3 + 1.5 * IQR))]
print(outliers)

# %% Cell 9


# %% Cell 10
import numpy as np
csv_rail_data1['Cost/km (2023 A$)'] = csv_rail_data1['Cost/km (2023 dollars)'] * 1.52

# %% Cell 11
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming your data is in a DataFrame and the column is named 'cost_per_km'
# Basic box plot using Matplotlib
plt.figure(figsize=(8, 4))
sns.boxplot(x=csv_rail_data1['Cost/km (2023 A$)'], color='grey', flierprops={'marker': ''})
plt.xlabel("Cost per km (Millions A$)")
#plt.title("Box and Whisker Plot of Rail Construction Costs per km")
plt.xlim(0, 2000)

plt.xticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Adding annotations for quartiles and median
Q1 = csv_rail_data1['Cost/km (2023 A$)'].quantile(0.25)
median = csv_rail_data1['Cost/km (2023 A$)'].median()
Q3 = csv_rail_data1['Cost/km (2023 A$)'].quantile(0.75)

# Add annotation for Q1, Median, and Q3
#plt.text(Q1, 0.1, f"Q1: ${Q1:.2f}M", ha='center', va='center', color='blue', fontsize=12)
#plt.text(median, 0.1, f"Median: ${median:.2f}M", ha='center', va='center', color='green', fontsize=12)
#plt.text(Q3, 0.1, f"Q3: ${Q3:.2f}M", ha='center', va='center', color='blue', fontsize=12)
plt.savefig("C:/Users/m1llz/Downloads/box_plot_cost_per_km.png", dpi=300, bbox_inches='tight')
plt.show()

# %% Cell 12
print(csv_rail_data1['Cost/km (2023 dollars)'].max())

# %% Cell 13
cost_data = csv_rail_data1['Cost/km (2023 A$)']  # Assuming 'cost_per_km' is your column name
summary_stats = cost_data.describe()
print(summary_stats)

# %% Cell 14

