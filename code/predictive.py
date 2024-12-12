# ------------------------------------------------ Predictive
# We can build a predictive model to determine if an employee got promoted. Here’s a step-by-step guide to building a binary classification model using Python, with the popular libraries Pandas, Scikit-Learn, and optionally, Seaborn and Matplotlib for visualization.
# Step-by-Step Guide to Building a Predictive Model:

# Import Necessary Libraries:
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt


#Load Your Dataset:
df = pd.read_csv('data_model.csv')



#Preprocess the Data:
#    Handle missing values, encode categorical variables, and scale numerical features.

    # Handle missing values
    df.fillna(method='ffill', inplace=True)
    # Encode categorical variables
    df = pd.get_dummies(df, columns=['region', 'job_cat', 'is_men'], drop_first=True)
    # Extract features and target variable
    X = df.drop(columns=['is_promo'])
    y = df['is_promo']
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=8)

    # Scale the features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)



# Build and Train the Model:
#    We'll use a Random Forest Classifier for this example.

    # Initialize the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    # Train the model
    model.fit(X_train, y_train)


# Evaluate the Model:

    # Make predictions
    y_pred = model.predict(X_test)
    # Evaluate the performance
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

    # Plot confusion matrix
    sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.title('Confusion Matrix')
    plt.show()


# Explanation:
#    Data Preprocessing: Handling missing values, encoding categorical variables, and scaling numerical features are crucial steps in preparing your data for modeling.
#    Model Selection: A Random Forest Classifier is chosen for its robustness and ability to handle complex data structures.
#    Evaluation: Accuracy, classification report, and confusion matrix provide insights into the model's performance.


# Insights:
#   We have a predictive model that can determine if an employee is likely to be promoted based on the features provided. The classification report and confusion matrix will help you understand the model's performance and areas for improvement.
#   We can tune the model parameters or try different algorithms to see which one performs best on our dataset.
