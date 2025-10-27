import joblib
import numpy as np
import json

class ModelLoader:
    def __init__(self):
        self.model = None
        self.feature_columns = None
        self.is_loaded = False
    
    def load_model(self, model_path='models/phishing_model.pkl', features_path='models/model_features.json'):
        """Load the trained model and feature columns"""
        try:
            # Load model
            self.model = joblib.load(model_path)
            
            # Load feature columns
            with open(features_path, 'r') as f:
                self.feature_columns = json.load(f)
            
            self.is_loaded = True
            print(f"✅ Model loaded successfully with {len(self.feature_columns)} features")
            print(f"📊 Features: {self.feature_columns}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.is_loaded = False
            return False
    
    def predict(self, features):
        """Make prediction with proper feature alignment"""
        if not self.is_loaded:
            return None
        
        try:
            # Ensure features are in correct order
            feature_array = []
            missing_features = []
            
            for feature_name in self.feature_columns:
                if feature_name in features:
                    feature_array.append(features[feature_name])
                else:
                    print(f"⚠️ Missing feature: {feature_name}, using default value 0")
                    missing_features.append(feature_name)
                    feature_array.append(0)  # Default value for missing features
            
            if missing_features:
                print(f"❌ Missing {len(missing_features)} features: {missing_features}")
            
            features_array = np.array([feature_array])
            
            # Get probability prediction
            probability = self.model.predict_proba(features_array)[0]
            phishing_prob = probability[1]  # Probability of class 1 (phishing)
            
            # Use adjustable threshold
            threshold = 0.7  # Conservative threshold to reduce false positives
            
            # FIX: Convert numpy bool to Python bool for JSON serialization
            is_phishing = bool(phishing_prob > threshold)
            
            return {
                'is_phishing': is_phishing,  # Now it's a Python bool, not numpy bool
                'confidence': float(phishing_prob),  # Ensure it's Python float
                'threshold_used': threshold,
                'probabilities': {
                    'legitimate': float(probability[0]),
                    'phishing': float(probability[1])
                },
                'missing_features': missing_features
            }
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None

# Global instance
model_loader = ModelLoader()