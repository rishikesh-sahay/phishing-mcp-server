import re
import urllib.parse
import numpy as np
from urllib.parse import urlparse

class URLFeatureExtractor:
    def __init__(self):
        self.shortening_services = [
            'bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'ow.ly', 
            'is.gd', 'buff.ly', 'shorte.st', 'bc.vc', 'adf.ly'
        ]
        
    def extract_features(self, url):
        features = {}
        
        # Basic features
        features['url_length'] = len(url)
        features['has_ip'] = 1 if self._is_ip_address(url) else 0
        features['has_shortening'] = 1 if any(service in url for service in self.shortening_services) else 0
        features['has_at_symbol'] = 1 if '@' in url else 0
        features['has_double_slash'] = 1 if '//' in url[8:] else 0
        features['has_hyphen'] = 1 if '-' in urlparse(url).netloc else 0
        features['has_multiple_subdomains'] = 1 if urlparse(url).netloc.count('.') >= 3 else 0
        features['has_port'] = 1 if urlparse(url).port and urlparse(url).port not in [80, 443] else 0
        features['misused_https'] = 1 if 'https' in url.lower() and not url.startswith('https://') else 0
        
        # Character analysis
        features['digit_count'] = sum(c.isdigit() for c in url)
        features['letter_count'] = sum(c.isalpha() for c in url)
        features['special_count'] = sum(not c.isalnum() for c in url)
        
        if len(url) > 0:
            features['digit_ratio'] = features['digit_count'] / len(url)
            features['letter_ratio'] = features['letter_count'] / len(url)
            features['special_ratio'] = features['special_count'] / len(url)
        else:
            features['digit_ratio'] = 0
            features['letter_ratio'] = 0
            features['special_ratio'] = 0
        
        features['entropy'] = self._calculate_entropy(url)
        
        return features
    
    def _is_ip_address(self, url):
        domain = urlparse(url).netloc
        ip_pattern = r'^\d+\.\d+\.\d+\.\d+(:\d+)?$'
        return bool(re.match(ip_pattern, domain))
    
    def _calculate_entropy(self, text):
        if len(text) <= 1:
            return 0
        counts = {}
        for char in text:
            counts[char] = counts.get(char, 0) + 1
        entropy = 0.0
        for count in counts.values():
            p_x = count / len(text)
            entropy += -p_x * np.log2(p_x)
        return entropy

feature_extractor = URLFeatureExtractor()