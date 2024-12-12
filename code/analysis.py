#!/usr/bin/env python
# coding: utf-8

# # Employee performance analysis with `Python`
# 
# ```
# @author: Aleksandras Urbonas
# @date  : 20241212 ALUR
# @email : aleksandras . urbonas (.) gmail . com
# ```
# 

# ---
# 
# # 0. Config
# 
# 

# In[ ]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# set chart size
sns.set_theme(rc={'figure.figsize':(3,3)})



# ---
# 
# # 1. Import data
# 
# 

# In[ ]:


raw_data_file_path = '../data/00_original/moondash_data.xlsx'

# Load the data
employee_data = pd.read_excel(raw_data_file_path, sheet_name='Employee Roster')
outcome_data = pd.read_excel(raw_data_file_path, sheet_name='Mid-Year Outcomes')



# In[ ]:


# Merge the data on employee_id
data_merged = pd.merge(employee_data, outcome_data, on='employee_id')
data_merged.set_index('employee_id', inplace=True)
# data.head(2)



# In[ ]:


# Display the first few rows to understand the structure
data_merged.head(2)



# In[ ]:


# Check the columns and data types
print(data_merged.info(), end='\n\n\n')



# In[ ]:


# Check for any missing values
print(data_merged.isnull().sum()) 



# ---
# 
# # 2. Data Prep
# 
# 

# In[ ]:


data_proc = data_merged



#     Some 2000 records are missing data in column `Perf_rating` and were excluded.
#     We continue with ~8000 records.
#     
#     

# In[ ]:


# remove null data
data_proc.dropna(subset=['perf_rating'], inplace=True)
data_proc.shape



# In[ ]:


### Clean `Age`
data_proc['age'] = np.round(data_proc['age'], 1)



# In[ ]:


### Calc: `is_promo`: 1 = Ready, 0 = no value
data_proc.loc[data_proc['promo_decision'].isna(), 'is_promo'] = 0
data_proc.loc[~data_proc['promo_decision'].isna(), 'is_promo'] = 1
data_proc['is_promo'] = data_proc['is_promo'].astype(int)
data_proc.drop(columns='promo_decision', inplace=True)



# In[ ]:


### `Job`: separate `Role` and `Level`
data_proc['job_role'] = data_proc['job_level'].str[0]
data_proc['job_rank'] = data_proc['job_level'].str[1].astype(int)
# data_proc[['job_level', 'job_role', 'job_rank']].head(2)



# In[ ]:


### Recode `gender` to `is_men` for statistics
data_proc.loc[data_proc['gender']=='men', 'is_men'] = 1
data_proc.loc[data_proc['gender']!='men', 'is_men'] = 0
data_proc['is_men'] = data_proc['is_men'].astype(int)
data_proc.drop(columns='gender', inplace=True)



# In[ ]:


### Recode `perf_rating` to perf_rank: only a rating, no text
data_proc['perf_rank'] = data_proc['perf_rating'].str[0].astype(int)




# In[ ]:


### Exclude non-performers, i.e. perf_rank = 1 or 2
data_proc.drop(data_proc[data_proc['perf_rank'].isin([1,2])].index, inplace=True)
print(f'''min: {min(data_proc['perf_rank'])}''')



# In[ ]:


data_proc.drop(columns='perf_rating', inplace=True)



# ### Inclusion/Exclusion Criteria
# 
# New promotion this cycle effective dated 2023-09-30.
# To be eligible for promotion, employees must have a tenure of at least 1.50 years by the 2023-09-30 effective date.
# 
#     We include employees that have worked longer than 1.5 year

# In[ ]:


### Transform `hire_date` into `tenure` 

# Convert hire_date to datetime
print(f'''* hire_date: from {str(min(data_proc['hire_date']))[:10]} to {str(max(data_proc['hire_date']))[:10]}''')
data_proc['hire_date'] = pd.to_datetime(data_proc['hire_date'])

# Calculate tenure in years
next_promotion_date = '2023-09-30'
data_proc['tenure'] = np.round((pd.to_datetime(next_promotion_date) - data_proc['hire_date']).dt.days / 365.25, 1)



# In[ ]:


data_proc.head(2)



# In[ ]:


# Filter employees eligible for promotion
data_proc = data_proc[data_proc['tenure'] >= 1]
# if 'hire_date' in data_proc.columns: data_proc.drop(columns='hire_date', inplace=True)



# ### QC before proceeding
# 
# 

# In[ ]:


# Drop rows with missing values in key columns, if any
data_clean = data_proc.dropna(subset=['perf_rank', 'is_men', 'is_promo'])

# Drop duplicates (if any)
data_clean = data_clean.drop_duplicates()

# Status: notify about number of removed duplicates
print(f'duplicates removed: {data_proc.shape[0] - data_clean.shape[0]} records.', "\n\n *** \n\n")

# Check the cleaned data
print(data_clean.isnull().sum())



# In[ ]:


print(data_clean.dtypes, "\n\n *** \n\n")


# statistics for numeric values
data_clean.describe()



# ---
# 
# # 3: Analysis
# 
#     Let's analyze the performance ratings and promotion decisions by gender.
# 
# 
data_clean[['perf_rank', 'is_men', 'is_promo']].head(4)


# In[ ]:


# Performance ratings by gender
data_clean.groupby(['job_role', 'is_men'])['is_promo'].count()
# ALUR: no clear difference



# In[ ]:


# Performance ratings by gender
perf_by_gender = data_clean.groupby('is_men')['perf_rank'].mean()
perf_by_gender



# In[ ]:


# Promotion decisions by gender
promo_by_gender = eligible_for_promo.groupby('is_men')['is_promo'].value_counts(normalize=True).unstack()
promo_by_gender



# ### Total Average Promotion Rate 
# 
# 

# In[ ]:


avg__is_promo = data_clean.groupby('is_promo')['is_promo'].count() / data_clean['is_promo'].count()
print(f'Average Promotion Rate: {np.round(avg__is_promo[1] * 100, 2)}%')



#     Question: what is the average by Role or Level?
# 
# 

# In[ ]:


avg_promo__by__job_level = np.round(data_clean.groupby('job_level')['is_promo'].mean()*100, 1)
avg_promo__by__job_level



#     > ALUR: difference by job level.
# 

# In[ ]:


print(f'The difference by job level: from {min(avg_promo__by__job_level)}% up to {max(avg_promo__by__job_level)}%')



# ---
# 
# ### Differences by `job_role`: not significant
# 
# 

# In[ ]:


avg__is_promo__by__job_role = np.round(data_clean.groupby('job_role')['is_promo'].mean()*100, 1)
print(avg__is_promo__by__job_role)



# ### Differences by `job_rank`: not significant
# 
# 

# In[ ]:


np.round(data_clean.groupby('job_rank')['is_promo'].mean()*100, 1)



# ## Plot results
# 
# 

# In[ ]:


data_clean.head(2)


# In[ ]:


# Performance ratings boxplot
plt.figure(figsize=(5, 3))
sns.boxplot(x='perf_rank', y='is_men', data=data_proc)
plt.title('Performance Ranks by Gender')
plt.show()



# In[ ]:


# Promotion decision bar plot
plt.figure(figsize=(10, 6))
promo_by_gender.plot(kind='bar', stacked=True)
plt.title('Promotion Decisions by Gender')
plt.xlabel('Gender')
plt.ylabel('Proportion')
plt.legend(title='Promotion Decision')
plt.show()



# # Boxplots

# In[ ]:


sns.boxplot(x='job_function', y='is_men', hue='is_promo', data=data_clean)
# sns.boxplot(x=['job_function', 'perf_rank'], y='is_promo', data=df)
plt.xlabel('Group (x)')
plt.ylabel('Value (y)')
plt.title('Boxplot of Variable y Grouped by Variable x')
plt.show()



# ## Promotion by Performance and Gender 
# 
# 

# In[ ]:


# calculate mean of `x` grouped by`y`:
mean_by_groups = pd.DataFrame(data_clean.groupby(['perf_rank', 'is_promo'])['is_men'].mean().reset_index())
#mean_by_groups = np.round(mean_by_groups, 2)
print(f'{mean_by_groups}')



plt.figure(figsize=(8,5))
sns.barplot(data=mean_by_groups, x='perf_rank', y='is_men', hue='is_promo')
plt.xlabel('perf_rank')
plt.ylabel('Mean of `is_men`')
plt.title('Mean of `is_men` by `perf_rank` and `is_promo`')
plt.legend(title='is_promo')
plt.show()



# In[ ]:


print(data_clean['is_men'].value_counts())
print(data_clean.groupby('is_men')['perf_rank'].describe())



# ## Some charts

# In[ ]:


sns.countplot(data=data_clean, x='is_men')
plt.title('Gender Distribution')
plt.show()



# In[ ]:


sns.barplot(data=data_clean, x='perf_rank', y='is_men')
plt.title('Performance Rank by Gender')
plt.show()



# ## Analyze Promotion Rate by Gender: Calculate the promotion rate for each gender
# 
# 

# In[ ]:


promotion_rate = data_clean.groupby('is_men')['is_promo'].mean().reset_index()
print(promotion_rate)

sns.barplot(data=promotion_rate, x='is_men', y='is_promo')
plt.title('Promotion Rate by Gender')
plt.show()



# ## Cross-tabulation for Detailed Analysis:
# 
#     We use cross-tabulation to analyze the relationship between gender and other categorical variables like region, job group, and job level.
# 
# 

# In[ ]:


pd.crosstab(data_clean['is_men'], data_clean['region'])



# In[ ]:


pd.crosstab(data_clean['is_men'], data_clean['job_role'])



# In[ ]:


pd.crosstab(data_clean['is_men'], data_clean['job_rank'])



# ## Advanced Visualization:
# 
# Create more complex visualizations, such as comparing performance rank and promotion rates across multiple variables.
# 
# 

# In[ ]:


data_clean.describe()



# In[ ]:


sns.catplot(data=data_clean, x='perf_rank', y='job_rank', hue='is_men', kind='box')
plt.title('Performance Rank by Job Level and Gender')
plt.show()



# In[ ]:


sns.catplot(data=data_clean, x='job_function', y='is_promo', hue='is_men', kind='bar')
plt.title('Promotion Rate by Job Function and Gender')
plt.show()



# In[ ]:


sns.catplot(data=data_clean, x='job_level', y='is_promo', hue='is_men', kind='bar')
plt.title('Promotion Rate by Job Level and Gender')
plt.show()



# In[ ]:


sns.catplot(data=data_clean, x='region', y='is_promo', hue='is_men', kind='bar')
plt.title('Promotion Rate by Job Function and Gender')
plt.show()



# In[ ]:


sns.catplot(data=data_clean, x='is_promo', y='is_men', hue='job_role', kind='bar')
plt.title('Promotion Rate by Job Group and Gender')
plt.show()



# # Data Insights:
# 
#     After data analysis, we have a clearer picture of possible gender gaps in performance, promotions, and other job-related metrics.
# 
#     We can further refine the analysis based on specific findings or delve deeper into areas showing disparities.
# 
# 

# # 4. Statistical Testing:
# 
# Now, let’s run a t-test to check if there’s a significant difference in performance scores based on gender.
# We’ll also check promotion rates.
# 
# 

# In[ ]:


data_clean.head(2)



# In[ ]:


from scipy import stats

# Separate performance scores by gender
male_performance = data_clean[data_clean['is_men'] == 1]['perf_rank']
female_performance = data_clean[data_clean['is_men'] == 0]['perf_rank']

# Perform a t-test for performance scores by gender 
t_stat_performance, p_val_performance = stats.ttest_ind(male_performance, female_performance)
print("\nT-test for performance scores by gender:")
print(f"T-statistic: {np.round(t_stat_performance, 3)}, p-value: {np.round(p_val_performance, 3)}")

# Check if the p-value is less than 0.05 for significance
if p_val_performance < 0.05: print("There is a significant difference in performance scores by gender.")
else: print("No significant difference in performance scores by gender.")



# In[ ]:


# Check promotion rates by gender using a Chi-Square test 
promotion_male = data_clean[data_clean['is_men'] == 1]['is_promo'].value_counts()
promotion_female = data_clean[data_clean['is_men'] == 0]['is_promo'].value_counts()

# Perform a Chi-Square test for promotion rates
chi2_stat, p_val_promotion, dof, expected = stats.chi2_contingency([promotion_male, promotion_female])
print("\nChi-Square test for promotion rates by gender:") 
print(f"Chi2 statistic: {np.round(chi2_stat, 3)}, p-value: {np.round(p_val_promotion, 3)}") 
# Check if the p-value is less than 0.05 for significance
if p_val_promotion < 0.05: print("There is a significant difference in promotion rates by gender.")
else: print("No significant difference in promotion rates by gender.") 



# ---
# 
# # 6. Actionable Insights & Recommendations:
# 
#     * The data does not show inequalities in performance and promotion about gender.
# 
#     * Propose solutions based on your findings: 
#         * If there is a gap in promotions despite equal performance, suggest a more transparent promotion process.
#         * If there's bias in performance reviews, recommend bias training for managers.
#         * If there’s a lag in time to promotion for one gender, suggest a more equitable pathway for career advancement, with clear timelines and expectations for both genders.
# 
# 

# ---
# 
# # 7. Final Thoughts for the Assignment:
# 
# 
#     * Be Transparent:
#         If there are gaps in the data or areas where you couldn't make a solid conclusion, be honest about it.
#         Transparency will always be appreciated.
# 
#     * Communicate Clearly:
#         When you present your findings, make sure to keep it simple and focused.
#         They want to know the key issues and what to do about them.
# 
#     * Contextualize Your Findings:
#         If relevant, refer to external studies or best practices to back up your recommendations, showing that you’re not just talking numbers but also understanding the broader picture of workplace gender equity.
# 
# 

# # Next Steps:
# 
#     * Use these insights to make recommendations for addressing any gender inequalities you find.
# 
#     * If any biases or disparities were found, we could consider introducing more transparent criteria for performance evaluations, or promoting unconscious bias training.
# 
# 

# # Conclusion:
# 
#     With these steps, we have an in-depth, data-driven approach to assess gender inequalities in our dataset.
# 
#     We did not find significant differences in performance, promotions, or time to promotion, which leaves little room to recommend ways to make the workplace even more equitable for everyone.
# 
# 
