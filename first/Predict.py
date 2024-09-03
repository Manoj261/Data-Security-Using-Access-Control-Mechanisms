import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib
import numpy as np
class Crop:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.label_encoder = LabelEncoder()
        self.rf_classifier = RandomForestClassifier(random_state=42)
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None

    def load_data(self):
        self.data = pd.read_csv(self.file_path)
        #print("data:",self.data.info())
        self.data['label'] = self.label_encoder.fit_transform(self.data['label'])

    def preprocess_data(self):
        X = self.data.drop(columns=['label'])
        y = self.data['label']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    def train_model(self):
        self.rf_classifier.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        y_pred = self.rf_classifier.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        report = classification_report(self.y_test, y_pred, target_names=self.label_encoder.classes_)
        print(f'Accuracy: {accuracy}')
        print('Classification Report:')
        print(report)

    def save_model(self, model_path, encoder_path):
        joblib.dump(self.rf_classifier, model_path)
        joblib.dump(self.label_encoder, encoder_path)

if __name__ == "__main__":
    file_path = r'C:\Users\Admin\OneDrive\Documents\Crop_recommendation.csv'
    model_path = 'rf_crop_model.pkl'
    encoder_path = 'label_encoder.pkl'

    crop_model = Crop(file_path)
    crop_model.load_data()
    crop_model.preprocess_data()
    crop_model.train_model()
    crop_model.evaluate_model()
    crop_model.save_model(model_path, encoder_path)



new_data = np.array([
    [90, 40, 40, 22.0, 80.0, 6.5, 200.0],
    [70, 50, 30, 25.0, 60.0, 7.0, 150.0],
    [50, 20, 10, 20.0, 70.0, 6.0, 100.0]
])


rf_classifier = joblib.load('rf_crop_model.pkl')
label_encoder = joblib.load('label_encoder.pkl')


feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
new_data_df = pd.DataFrame(new_data, columns=feature_names)


predictions = rf_classifier.predict(new_data_df)
predicted_labels = label_encoder.inverse_transform(predictions)

print('Predicted crop types:', predicted_labels)