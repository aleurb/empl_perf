# To check for gender gaps in our multivariate dataset, we can conduct an analysis that includes summary statistics and visualizations.
# Here is a step-by-step recipe in python

# Import Necessary Libraries:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load Your Dataset: Ensure your dataset is loaded into a DataFrame. For this example, let's assume your dataset is stored in a CSV file named employee_performance.csv:
df = pd.read_csv('employee_performance.csv')



# Check Basic Statistics: Start by checking basic statistics to get an overview of the gender distribution and performance metrics.
print(df['is_men'].value_counts())
print(df.groupby('is_men')['performance_rank'].describe())



# Visualize Gender Distribution: Plot the distribution of genders to see if there is any noticeable imbalance.

sns.countplot(data=df, x='is_men')
plt.title('Gender Distribution')
plt.show()


# Analyze Performance Rank by Gender: Use box plots to compare the performance rank across genders.

sns.boxplot(data=df, x='is_men', y='performance_rank')
plt.title('Performance Rank by Gender')
plt.show()



# Analyze Promotion Rate by Gender: Calculate the promotion rate for each gender.

promotion_rate = df.groupby('is_men')['is_promo'].mean().reset_index()
print(promotion_rate)
sns.barplot(data=promotion_rate, x='is_men', y='is_promo')
plt.title('Promotion Rate by Gender')
plt.show()



# Cross-tabulation for Detailed Analysis: Use cross-tabulation to analyze the relationship between gender and other categorical variables like region, job group, and job level.

pd.crosstab(df['is_men'], df['region'])
pd.crosstab(df['is_men'], df['job_cat'])
pd.crosstab(df['is_men'], df['job_rank'])



# Advanced Visualization: Create more complex visualizations, such as comparing performance rank and promotion rates across multiple variables.

sns.catplot(data=df, x='job_rank', y='perf_rank', hue='is_men', kind='box')
plt.title('Performance Rank by Job Level and Gender')
plt.show()

sns.catplot(data=df, x='job_cat', y='is_promo', hue='is_men', kind='bar')
plt.title('Promotion Rate by Job Group and Gender')
plt.show()


# Example Data Insights:
# After performing these steps, you should have a clearer picture of whether there are significant gender gaps in performance, promotions, and other job-related metrics.
# You can further refine the analysis based on specific findings or delve deeper into areas showing disparities.


