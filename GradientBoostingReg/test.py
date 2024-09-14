import numpy as np
import pandas as pd
import os
from sklearn.metrics import mean_squared_error
import joblib

path_credit_budget_model = os.path.join(os.getcwd(), 'GradientBoostingReg\\credit_budget_model.pkl')
path_credit_terms_model = os.path.join(os.getcwd(), 'GradientBoostingReg\\credit_terms_model.pkl')


credit_budget_model = joblib.load(path_credit_budget_model)
credit_terms_model = joblib.load(path_credit_terms_model)

test_data = np.array([[700, 12000, 23]])

predicted_budget = credit_budget_model.predict(test_data)
predicted_terms = credit_terms_model.predict(test_data)

print(predicted_budget[0], predicted_terms[0])