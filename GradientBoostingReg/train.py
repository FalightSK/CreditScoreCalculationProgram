import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
import joblib

dir = os.getcwd()
path = os.path.join(dir, 'GradientBoostingReg\\dataset.csv')
doc = pd.read_csv(path)


# Data preparation
train_data = []
target = []
for data in doc.iloc():
    train_data.append((data['FICO Score'], data['Avg Order Size'], data['Number of Orders']))
    target.append((data['Credit Budget'], data['Credit Terms (Days)']))

# Create pandas DataFrame for input data
df = pd.DataFrame(train_data, columns=['fico_score', 'avg_order_size', 'num_orders'])

# Create pandas DataFrame for target data
target_df = pd.DataFrame(target, columns=['credit_budget', 'credit_terms'])

# Ensure credit terms are within the range of 7 to 30
target_df['credit_terms'] = target_df['credit_terms'].clip(7, 30)

# Combine the dataframes for input features and target variables
df = pd.concat([df, target_df], axis=1)

# Split the dataset into training and testing sets
X = df[['fico_score', 'avg_order_size', 'num_orders']]  # Features
y_budget = df['credit_budget']  # Target 1: Credit Budget
y_terms = df['credit_terms']  # Target 2: Credit Terms

# Splitting the data for credit_budget prediction
X_train_budget, X_test_budget, y_train_budget, y_test_budget = train_test_split(X, y_budget, test_size=0.2, random_state=42)

# Splitting the data for credit_terms prediction
X_train_terms, X_test_terms, y_train_terms, y_test_terms = train_test_split(X, y_terms, test_size=0.2, random_state=42)

# Initialize Gradient Boosting Regressors
gbr_budget = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
gbr_terms = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Train the model 
gbr_budget.fit(X_train_budget, y_train_budget)
gbr_terms.fit(X_train_terms, y_train_terms)

# Make predictions for the test set

joblib.dump(gbr_budget, os.path.join(dir, 'GradientBoostingReg\\credit_budget_model.pkl'))
joblib.dump(gbr_terms, os.path.join(dir, 'GradientBoostingReg\\credit_terms_model.pkl'))
