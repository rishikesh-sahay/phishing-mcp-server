from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import os

from config import config
from utils.enhanced_feature_extractor import EnhancedFeatureExtractor
from utils.model_loader import model_loader

app = Flask(__name__)
CORS(app)

# Initialize enhanced feature extractor
feature_extractor = EnhancedFeatureExtractor()

# Load model
model_loader.load_model()
print("✅ Enhanced MCP Phishing Server Ready!")

# ========== WEB INTERFACE ROUTES ==========
@app.route('/')
def serve_web_interface():
    return send_from_directory('.', 'web_interface.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

class PhishingAnalyzer:
    def analyze_url(self, url):
        try:
            # Extract features using enhanced extractor
            features = feature_extractor.extract_features(url)
            
            if model_loader.is_loaded:
                model_result = model_loader.predict(features)
                if model_result:
                    # FIX: Ensure all types are JSON serializable
                    is_phishing = bool(model_result['is_phishing'])  # Convert to Python bool
                    confidence = float(model_result['confidence'])    # Convert to Python float
                    method = 'AI Model'
                    missing_features = model_result.get('missing_features', [])
                else:
                    is_phishing, confidence, method = self.rule_based_analysis(features)
                    missing_features = []
            else:
                is_phishing, confidence, method = self.rule_based_analysis(features)
                missing_features = []
            
            explanation = self.generate_explanation(features, is_phishing)
            
            result = {
                'url': str(url),  # Ensure string
                'is_phishing': bool(is_phishing),  # Ensure Python bool
                'confidence': float(confidence),    # Ensure Python float
                'explanation': str(explanation),    # Ensure string
                'method': str(method),              # Ensure string
                'timestamp': str(datetime.now().isoformat()),  # Ensure string
                'features_analyzed': int(len(features))  # Ensure int
            }
            
            if missing_features:
                result['warning'] = str(f"{len(missing_features)} features unavailable")
            
            return result
            
        except Exception as e:
            return {'error': str(e), 'url': str(url)}
    
    def rule_based_analysis(self, features):
        """Fallback rule-based analysis"""
        risk_score = 0
        if features.get('having_IP_Address', 0): 
            risk_score += 0.3
        if features.get('Shortening_Service', 0): 
            risk_score += 0.25
        if features.get('having_At_Symbol', 0): 
            risk_score += 0.2
        if features.get('double_slash_redirecting', 0): 
            risk_score += 0.1
        if features.get('HTTPS_token', 0): 
            risk_score += 0.15
        
        risk_score = min(risk_score, 1.0)
        is_phishing = risk_score > 0.5
        confidence = risk_score if is_phishing else (1 - risk_score)
        
        return is_phishing, confidence, 'Rule-Based'
    
    def generate_explanation(self, features, is_phishing):
        """Generate detailed explanation based on features"""
        reasons = []
        
        if features.get('having_IP_Address', 0): 
            reasons.append("IP address in URL")
        if features.get('Shortening_Service', 0): 
            reasons.append("URL shortening service")
        if features.get('having_At_Symbol', 0): 
            reasons.append("@ symbol in URL")
        if features.get('HTTPS_token', 0): 
            reasons.append("suspicious HTTPS usage")
        if features.get('Prefix_Suffix', 0): 
            reasons.append("hyphen in domain")
        if features.get('having_Sub_Domain', 0) > 2: 
            reasons.append("multiple subdomains")
        
        if reasons:
            return f"Detected features: {', '.join(reasons)}"
        return "No strong phishing indicators detected"

analyzer = PhishingAnalyzer()

# ========== API ROUTES ==========
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'model_loaded': model_loader.is_loaded,
        'features_available': len(model_loader.feature_columns) if model_loader.feature_columns else 0
    })

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'URL required'}), 400
    
    url = data['url']
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    result = analyzer.analyze_url(url)
    return jsonify(result)

# ========== DEBUG ROUTES ==========
@app.route('/debug-features', methods=['POST'])
def debug_features():
    """Debug endpoint to see extracted features"""
    data = request.json
    url = data['url']
    
    try:
        features = feature_extractor.extract_features(url)
        
        return jsonify({
            'url': url,
            'features': features,
            'total_features': len(features),
            'non_zero_features': {k: v for k, v in features.items() if v != 0}
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/model-info')
def model_info():
    """Get model information"""
    return jsonify({
        'model_loaded': model_loader.is_loaded,
        'feature_columns': model_loader.feature_columns,
        'total_features': len(model_loader.feature_columns) if model_loader.feature_columns else 0
    })

@app.route('/test-features', methods=['POST'])
def test_features():
    """Test feature extraction for debugging"""
    data = request.json
    url = data['url']
    
    try:
        features = feature_extractor.extract_features(url)
        
        return jsonify({
            'url': url,
            'features_extracted': features,
            'feature_count': len(features),
            'model_loaded': model_loader.is_loaded,
            'model_features_count': len(model_loader.feature_columns) if model_loader.feature_columns else 0
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', config.PORT))
    app.run(host=config.HOST, port=port, debug=config.DEBUG)