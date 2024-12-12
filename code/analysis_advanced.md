People analytics is a super hot field right now, and tackling gender inequalities in the workplace is both important and timely.

Now, for your home assignment, let’s break it down into manageable pieces to make sure you’re approaching it in the most impactful way.


1. Understanding the Problem: Gender Inequalities in Performance and Promotion
    * Data Insight: First, understand the scope of the data.
        We are working with promotion history. Performance reviews are not included.
        Variables available for assessment of these areas are: gender, hire date, position, performance rank
   
   * Problem Framing: The main challenge here is identifying if and where gender disparities exist.
        The goal is to answer questions like: 
            * Do men and women have equal performance ratings?
            * Are promotions distributed equally?
            * Is there a gap in the number of promotions based on gender, even if performance is equal?
            * Do men and women get the same opportunities for career growth based on the same performance?


2. SQL Work and Analysis:
    * Data Aggregation:
        Start by aggregating the data you have. You'll likely need to group it by gender and then look at key metrics such as: 
            * Average performance scores by gender.
            * Promotion rates by gender.
            * Time to promotion for each gender.
            * Distribution of performance ratings by gender—are men and women getting the same ratings, or is there a noticeable difference in scores?
    * Data Cleaning:
        Make sure to clean any missing or inconsistent data. This will ensure your analysis isn’t skewed by incomplete data sets.
    * Statistical Analysis:
        Use simple statistical methods like averages, medians, and standard deviations to compare the performance and promotion rates.
        If possible, run tests like the T-test or Chi-square test to assess if the differences are statistically significant. This will give you more weight in your findings.


3. Key Metrics to Focus On:
    * Performance vs. Gender:
        Are there differences in performance scores by gender, even after controlling for factors like tenure, job level, or experience?
    * Promotion Ratio:
        Compare the number of promotions by gender.
        Is there a higher promotion rate for one gender over the other?
        Are men promoted more quickly than women, despite similar performance?
    * Time to Promotion:
        If performance is equal, does gender play a role in how quickly employees get promoted?
        Are women taking longer to be promoted, or are they held to a higher standard?
    * Leadership Representation:
        How does gender distribution look at the leadership level?
        Are women underrepresented in senior roles compared to the rest of the organization?



4. Visualizing Your Findings:
    Create clear, easy-to-read visualizations of your data to help tell the story.
    Some key visualizations could be: 
        * Bar charts comparing average performance ratings by gender.
        * Line charts or scatter plots showing promotion rates over time.
        * Histograms for comparing performance score distributions.
        * Visualizations will help make your findings clearer and will show how you analyzed the data, which is key in a home assignment.



5. Analyzing Bias in the Data:
    When examining gender inequalities, it's also important to assess if there might be any biases in the system.
    For instance: 
        * Are there performance review biases? Some studies show that women are often rated more harshly on leadership traits, while men are seen as more assertive.
        * Is there unconscious bias in the promotion process? Even if performance is similar, do people from certain demographics get more opportunities to advance?
        * You might not have all the data to fully assess these biases, but it's worth noting in your analysis.



6. Actionable Insights & Recommendations:
    * Once you've done the analysis, your next step is interpretation. What do the data show about gender inequalities in performance and promotion?
    * Propose solutions based on your findings: 
    * If there is a gap in promotions despite equal performance, suggest a more transparent promotion process.
    * If there's bias in performance reviews, recommend bias training for managers.
    * If there’s a lag in time to promotion for one gender, suggest a more equitable pathway for career advancement, with clear timelines and expectations for both genders.



7. Final Thoughts for the Assignment:
    * Be Transparent: If there are gaps in the data or areas where you couldn't make a solid conclusion, be honest about it. Transparency will always be appreciated.
    * Communicate Clearly: When you present your findings, make sure to keep it simple and focused. They want to know the key issues and what to do about them.
    * Contextualize Your Findings: If relevant, refer to external studies or best practices to back up your recommendations, showing that you’re not just talking numbers but also understanding the broader picture of workplace gender equity.



----------------------------- P2: Code

Now, let’s turn it into some actionable Python code. I’ll assume you have the necessary dataset (e.g., in a CSV file) and will help you with basic data processing and analysis in Python using pandas and matplotlib (for visualizations), as well as some statistical tests with scipy.

Here’s a basic code structure that follows the steps in the plan:

1. DONE: Data Loading and Initial Exploration:
    import pandas as pd
    # Load your dataset
    df = pd.read_csv("your_dataset.csv")
    # Display the first few rows to understand the structure
    print(df.head())

    # Check the columns and data types
    print(df.info())

    # Check for any missing values
    print(df.isnull().sum()) 


2. Data Cleaning (handle missing values, duplicate rows, etc.):
    # Drop rows with missing values in key columns, if any
    df_clean = df.dropna(subset=['perf_rank', 'is_promo', 'is_men'])

    # Optionally, you can fill missing values with a specific strategy if needed:
    df['perf_rank'].fillna(df['perf_rank'].mean(), inplace=True)

    # Drop duplicates (if any)
    df_clean = df_clean.drop_duplicates()
    # Check the cleaned data
    print(df_clean.isnull().sum()) 



3. Data Aggregation and Descriptive Statistics:
We'll calculate key metrics, such as the average performance score by gender, and promotion rates.

    # Calculate average performance by gender
    gender_performance = df_clean.groupby('is_men')['perf_rank'].mean()
    print("Average performance by gender:\n", gender_performance)

    # Calculate promotion rate by gender (e.g., 1 = promoted, 0 = not promoted)
    promotion_rate = df_clean.groupby('is_men')['is_promo'].mean()

    print("\nPromotion rate by gender:\n", promotion_rate)

    # Time to promotion - calculate the average time (if you have a column like 'time_in_current_role')
    # This assumes 'time_in_current_role' is a column in your dataset

    time_to_promotion = df_clean[df_clean['is_promo'] == 1].groupby('is_men')['time_in_current_role'].mean()
    print("\nTime to promotion by gender:\n", time_to_promotion) 



4. Statistical Testing:
Now, let’s run a t-test to check if there’s a significant difference in performance scores based on gender. We’ll also check promotion rates.

from scipy import stats
# Separate performance scores by gender
male_performance = df_clean[df_clean['is_men'] == 'Male']['perf_rank']
female_performance = df_clean[df_clean['is_men'] == 'Female']['perf_rank']

# Perform a t-test for performance scores by gender 
t_stat_performance, p_val_performance = stats.ttest_ind(male_performance, female_performance)
print("\nT-test for performance scores by gender:")
print(f"T-statistic: {t_stat_performance}, p-value: {p_val_performance}")

# Check if the p-value is less than 0.05 for significance
if p_val_performance < 0.05: print("There is a significant difference in performance scores by gender.") else: print("No significant difference in performance scores by gender.")

# Check promotion rates by gender using a Chi-Square test 
promotion_male = df_clean[df_clean['is_men'] == 'Male']['is_promo'].value_counts()
promotion_female = df_clean[df_clean['is_men'] == 'Female']['is_promo'].value_counts()

# Perform a Chi-Square test for promotion rates
chi2_stat, p_val_promotion, dof, expected = stats.chi2_contingency([promotion_male, promotion_female])
print("\nChi-Square test for promotion rates by gender:") 
print(f"Chi2 statistic: {chi2_stat}, p-value: {p_val_promotion}") 
# Check if the p-value is less than 0.05 for significance
if p_val_promotion < 0.05: print("There is a significant difference in promotion rates by gender.")
else: print("No significant difference in promotion rates by gender.") 



5. Data Visualization:
Visualizing the performance scores and promotion rates by gender:

    #import matplotlib.pyplot as plt
    
    # 1. Plot average performance by gender
    plt.figure(figsize=(8, 6))
    df_clean.groupby('is_men')['perf_rank'].mean().plot(kind='bar', color=['blue', 'orange'])
    plt.title('Average Performance Score by Gender')
    plt.xlabel('is_men')
    plt.ylabel('Average Performance Score')
    plt.show()

    # 2. Plot promotion rates by gender
    plt.figure(figsize=(8, 6)) 
    df_clean.groupby('is_men')['is_promo'].mean().plot(kind='bar', color=['blue', 'orange']) 
    plt.title('Promotion Rate by Gender') 
    plt.xlabel('is_men') 
    plt.ylabel('Promotion Rate') 
    plt.show()

    # 3. Distribution of performance scores by gender
    plt.figure(figsize=(8, 6)) 
    df_clean[df_clean['is_men'] == 'Male']['perf_rank'].plot(kind='hist', alpha=0.5, bins=20, color='blue', label='Male') 
    df_clean[df_clean['is_men'] == 'Female']['perf_rank'].plot(kind='hist', alpha=0.5, bins=20, color='orange', label='Female') 
    plt.title('Performance Score Distribution by Gender') plt.xlabel('Performance Score') 
    plt.legend() 
    plt.show() 




6. Final Actionable Insights:

    Summary of findings based on statistical results and visualizations:

    * Gender differences in performance:
        Do the means of the performance scores differ between men and women?
        Is there a significant difference based on your t-test result?

    * Promotion rates:
        Are men promoted more often than women, or is it the opposite?
        Is the difference statistically significant?

    * Time to promotion:
        Do men and women take the same amount of time to get promoted, or is there a noticeable gap?



Next Steps:
• Use these insights to make recommendations for addressing any gender inequalities you find.
• If you find any biases or disparities, suggest actionable steps such as introducing more transparent criteria for performance evaluations or promoting unconscious bias training.



# Conclusion:
With these steps, we have an in-depth, data-driven approach to assess gender inequalities in our dataset.
We did not find significant differences in performance, promotions, or time to promotion, you can recommend ways to make the workplace more equitable for everyone.
