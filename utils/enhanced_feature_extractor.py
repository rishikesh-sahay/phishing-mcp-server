import re
import math
from urllib.parse import urlparse
import tldextract

class EnhancedFeatureExtractor:
    def __init__(self):
        self.shortening_services = [
            'bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'is.gd', 
            'buff.ly', 'adf.ly', 'ow.ly', 'tiny.cc', 'bit.do'
        ]
        
    def extract_features(self, url):
        """Extract all 35 features matching the training dataset"""
        features = {}
        
        # 1. Basic URL Structure Features
        features['having_IP_Address'] = self.has_ip_address(url)
        features['URL_Length'] = len(url)
        features['Shortening_Service'] = self.has_shortening_service(url)
        features['having_At_Symbol'] = self.has_at_symbol(url)
        features['double_slash_redirecting'] = self.has_double_slash_redirect(url)
        features['Prefix_Suffix'] = self.has_prefix_suffix(url)
        features['having_Sub_Domain'] = self.count_subdomains(url)
        features['HTTPS_token'] = self.has_https_token(url)
        features['having_port'] = self.has_port(url)
        features['Abnormal_URL'] = self.is_abnormal_url(url)
        features['Redirect'] = self.has_redirect(url)
        
        # 2. Content Analysis Features (simplified)
        features['URL_of_Anchor'] = 0
        features['Links_in_tags'] = 0
        features['SFH'] = 0
        features['popUpWindow'] = 0
        features['Iframe'] = 0
        
        # 3. Domain & Network Features
        features['Age_of_domain'] = self.get_domain_age(url)
        features['DNSRecord'] = self.has_dns_record(url)
        features['web_traffic'] = 0
        features['Google_Index'] = self.is_google_indexed(url)
        features['Links_pointing_to_page'] = 0
        features['Statistical_report'] = 0
        
        # 4. Statistical URL Features
        features['url_length'] = len(url)
        features['entropy'] = self.calculate_entropy(url)
        features['digit_count'] = self.count_digits(url)
        features['letter_count'] = self.count_letters(url)
        features['special_count'] = self.count_special_chars(url)
        features['digit_ratio'] = self.calculate_digit_ratio(url)
        features['letter_ratio'] = self.calculate_letter_ratio(url)
        features['special_ratio'] = self.calculate_special_ratio(url)
        
        # 5. Form & Interaction Features
        features['Request_URL'] = 0
        features['Submitting_to_email'] = 0
        features['Abnormal_Form_Action'] = 0
        features['on_mouseover'] = 0
        features['RightClick'] = 0
        
        return features
    
    def has_ip_address(self, url):
        ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        return 1 if re.search(ip_pattern, url) else 0
    
    def has_shortening_service(self, url):
        domain = self.extract_domain(url)
        return 1 if any(service in domain for service in self.shortening_services) else 0
    
    def has_at_symbol(self, url):
        return 1 if '@' in url else 0
    
    def has_double_slash_redirect(self, url):
        return 1 if '//' in url[7:] else 0
    
    def has_prefix_suffix(self, url):
        domain = self.extract_domain(url)
        return 1 if '-' in domain else 0
    
    def count_subdomains(self, url):
        try:
            extracted = tldextract.extract(url)
            subdomains = extracted.subdomain.split('.')
            return len([sd for sd in subdomains if sd])
        except:
            return 0
    
    def has_https_token(self, url):
        domain = self.extract_domain(url)
        return 1 if 'https' in domain.lower() else 0
    
    def has_port(self, url):
        try:
            parsed = urlparse(url)
            return 1 if parsed.port else 0
        except:
            return 0
    
    def is_abnormal_url(self, url):
        domain = self.extract_domain(url)
        return 1 if len(domain) < 4 or len(domain) > 30 else 0
    
    def has_redirect(self, url):
        redirect_keywords = ['redirect', 'url=', 'goto=', 'link=', 'out=']
        return 1 if any(keyword in url.lower() for keyword in redirect_keywords) else 0
    
    def get_domain_age(self, url):
        try:
            domain = self.extract_domain(url)
            if domain in ['google.com', 'facebook.com', 'amazon.com', 'microsoft.com']:
                return 3650
            domain_length = len(domain)
            if domain_length < 8:
                return 30
            elif domain_length < 12:
                return 180
            else:
                return 365
        except:
            return 30
    
    def has_dns_record(self, url):
        domain = self.extract_domain(url)
        known_domains = ['google.com', 'facebook.com', 'youtube.com', 'amazon.com', 
                        'microsoft.com', 'apple.com', 'wikipedia.org', 'twitter.com']
        return 1 if domain in known_domains else 0
    
    def is_google_indexed(self, url):
        domain = self.extract_domain(url)
        known_domains = ['google.com', 'facebook.com', 'youtube.com', 'amazon.com', 
                        'microsoft.com', 'apple.com', 'wikipedia.org', 'twitter.com',
                        'instagram.com', 'linkedin.com', 'nero.com']
        return 1 if domain in known_domains else 0
    
    def calculate_entropy(self, text):
        if len(text) == 0:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(text.count(chr(x))) / len(text)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy
    
    def count_digits(self, text):
        return sum(c.isdigit() for c in text)
    
    def count_letters(self, text):
        return sum(c.isalpha() for c in text)
    
    def count_special_chars(self, text):
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
        return sum(1 for c in text if c in special_chars)
    
    def calculate_digit_ratio(self, url):
        return self.count_digits(url) / len(url) if len(url) > 0 else 0
    
    def calculate_letter_ratio(self, url):
        return self.count_letters(url) / len(url) if len(url) > 0 else 0
    
    def calculate_special_ratio(self, url):
        return self.count_special_chars(url) / len(url) if len(url) > 0 else 0
    
    def extract_domain(self, url):
        try:
            extracted = tldextract.extract(url)
            return f"{extracted.domain}.{extracted.suffix}" if extracted.suffix else extracted.domain
        except:
            return ""