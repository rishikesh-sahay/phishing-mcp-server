import joblib
import pandas as pd
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import os

print("🚀 Training and saving phishing detection model...")

# Load your dataset
df = pd.read_csv('phishing_research_dataset.csv')

# Prepare features
feature_columns = [col for col in df.columns if col not in ['url', 'label']]
X = df[feature_columns]
y = df['label']

print(f"📊 Dataset: {df.shape[0]} samples, {len(feature_columns)} features")

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Create models directory
os.makedirs('models', exist_ok=True)

# Save model
joblib.dump(model, 'models/phishing_model.pkl')

# Save feature list
with open('models/model_features.json', 'w') as f:
    json.dump(feature_columns, f, indent=2)

# Test accuracy
accuracy = model.score(X_test, y_test)
print(f"✅ Model saved with accuracy: {accuracy:.4f}")
print("📁 Files created:")
print("   - models/phishing_model.pkl")
print("   - models/model_features.json")