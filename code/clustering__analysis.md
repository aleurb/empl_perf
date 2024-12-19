# @title: clustering-analysis.md
# @date : 20241218 ALUR

To compare the properties of clusters in your original dataset after performing hierarchical clustering, you need to analyze and summarize the data for each cluster. This comparison can provide insights into how the clusters differ based on various attributes (e.g., age, tenure, gender, job function, performance ratings). 

Here are a few common techniques you can use to compare properties of clusters in your original dataset:

### **1. Descriptive Statistics by Cluster**
You can calculate basic descriptive statistics (mean, median, standard deviation, etc.) for each cluster to compare the properties of continuous variables such as age, tenure, and performance rating.

```python
# Group by cluster and calculate descriptive statistics
cluster_stats = df.groupby('cluster').agg({
    'age': ['mean', 'std', 'min', 'max'],
    'tenure': ['mean', 'std', 'min', 'max'],
    'perf_rating': ['mean', 'std', 'min', 'max']
})

print(cluster_stats)
```

This will give you a table that shows the mean, standard deviation, minimum, and maximum values for the `age`, `tenure`, and `perf_rating` variables in each cluster.

### **2. Count the Frequency of Categorical Variables in Each Cluster**
For categorical variables like `gender`, `job_function`, you can use a **cross-tabulation** or **group-by operation** to see how each category is distributed across clusters.

```python
# Count the occurrences of categorical variables by cluster
categorical_comparison = pd.crosstab(df['cluster'], df['gender'])
print(categorical_comparison)

categorical_comparison_function = pd.crosstab(df['cluster'], df['job_function'])
print(categorical_comparison_function)
```

This will give you a count of how many males, females, and non-binary employees belong to each cluster. Similarly, you can look at the distribution of different `job_function` categories in each cluster.

### **3. Compare Cluster Distribution Using Visualization**
You can use visualizations to better understand how the clusters differ. Common visualization methods include box plots, violin plots, and bar charts.

#### **a. Box Plot for Continuous Variables**

Box plots are useful to compare the distributions of continuous variables (like `age`, `tenure`, `perf_rating`) across clusters.

```python
import seaborn as sns
import matplotlib.pyplot as plt

# Boxplot for 'age' by cluster
sns.boxplot(x='cluster', y='age', data=df)
plt.title("Age Distribution by Cluster")
plt.show()

# Boxplot for 'tenure' by cluster
sns.boxplot(x='cluster', y='tenure', data=df)
plt.title("Tenure Distribution by Cluster")
plt.show()

# Boxplot for 'perf_rating' by cluster
sns.boxplot(x='cluster', y='perf_rating', data=df)
plt.title("Performance Rating Distribution by Cluster")
plt.show()
```

#### **b. Bar Plot for Categorical Variables**

Bar plots are effective for showing how categorical variables like `gender` or `job_function` are distributed across clusters.

```python
# Bar plot for gender distribution by cluster
sns.countplot(x='cluster', hue='gender', data=df)
plt.title("Gender Distribution by Cluster")
plt.show()

# Bar plot for job_function distribution by cluster
sns.countplot(x='cluster', hue='job_function', data=df)
plt.title("Job Function Distribution by Cluster")
plt.show()
```

### **4. Compare Clusters Using Pivot Tables**
You can use pivot tables to summarize and compare different properties by cluster. This approach is especially useful for quick comparisons between clusters.

```python
# Pivot table for summary statistics of continuous variables
pivot_stats = pd.pivot_table(df, values=['age', 'tenure', 'perf_rating'], 
                             index='cluster', 
                             aggfunc={'age': ['mean', 'std'], 'tenure': ['mean', 'std'], 'perf_rating': ['mean', 'std']})

print(pivot_stats)
```

This will give you a detailed summary of `age`, `tenure`, and `perf_rating` across different clusters.

### **5. Statistical Tests Between Clusters**
If you're interested in testing whether the differences between clusters are statistically significant, you can perform **ANOVA** (for continuous variables) or **Chi-squared tests** (for categorical variables).

#### **a. ANOVA for Continuous Variables**

ANOVA can help determine if there are significant differences between clusters for continuous variables like `age`, `tenure`, and `perf_rating`.

```python
from scipy.stats import f_oneway

# ANOVA for 'age'
f_stat, p_val = f_oneway(df[df['cluster'] == 1]['age'], 
                          df[df['cluster'] == 2]['age'], 
                          df[df['cluster'] == 3]['age'])
print(f"ANOVA for Age - F-statistic: {f_stat}, p-value: {p_val}")

# If p-value < 0.05, the differences between clusters in terms of 'age' are statistically significant
```

#### **b. Chi-Squared Test for Categorical Variables**

If you want to compare categorical variables, you can perform a **Chi-squared test** to see if the distribution of categories differs significantly across clusters.

```python
from scipy.stats import chi2_contingency

# Chi-squared test for 'gender' vs. 'cluster'
contingency_table = pd.crosstab(df['cluster'], df['gender'])
chi2_stat, p_val, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-squared Test for Gender - p-value: {p_val}")
```

If the `p-value` is less than 0.05, it indicates that the distribution of `gender` across clusters is significantly different.

### **6. Cluster Profiling Summary**

Once you've completed the analysis using the above techniques, you can create a summary of the clusters' characteristics. For example:

- **Cluster 1** might have a younger average age, higher performance ratings, and a more balanced gender distribution.
- **Cluster 2** might have employees with higher tenure and predominantly male employees, with lower performance ratings.
- **Cluster 3** might have a mix of younger and older employees, but more females and a higher rate of promotion readiness.

### **Final Thoughts**

By comparing properties of the clusters using the steps above, you'll be able to understand the characteristics of each cluster and identify key differences in employee profiles, which could inform management decisions such as resource allocation, promotions, or performance improvement strategies. Visualizations are especially useful for presenting this information to non-technical audiences, while statistical tests provide more formal evidence for your findings.
