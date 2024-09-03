import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import joblib


file_path = r'C:\Users\Admin\OneDrive\Desktop\dev\myenv\first\first\Crop_Yield_Prediction_main.csv'
data = pd.read_csv(file_path)


label_encoder = LabelEncoder()
data['Crop'] = label_encoder.fit_transform(data['Crop'])

X = data.drop(columns='Yield')
y = data['Yield']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = RandomForestRegressor(random_state=42)


param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}


grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)


grid_search.fit(X_train, y_train)


best_params = grid_search.best_params_

best_model = RandomForestRegressor(**best_params, random_state=42)
best_model.fit(X_train, y_train)

y_pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Best Parameters:", best_params)
print("MAE:", mae)
print("MSE:", mse)
print("R2:", r2)


joblib.dump(best_model, 'crop_yield_predictor_model.pkl')


loaded_model = joblib.load('crop_yield_predictor_model.pkl')


# sample_data = X_test.head(10)
# sample_predictions = loaded_model.predict(sample_data)

# sample_results = pd.DataFrame({
#     'Actual Yield': y_test.head(10).values,
#     'Predicted Yield': sample_predictions
# })

# print("Sample Predictions:\n", sample_results)
