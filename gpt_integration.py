import openai
import requests
import re
from config import config

class PhishingGPT:
    def __init__(self, mcp_server_url="http://localhost:5000"):
        self.mcp_server_url = mcp_server_url
        self.openai_api_key = config.OPENAI_API_KEY
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
    
    def analyze_url(self, url):
        try:
            response = requests.post(
                f"{self.mcp_server_url}/analyze",
                json={'url': url},
                timeout=10
            )
            return response.json()
        except Exception as e:
            return {'error': f'MCP error: {str(e)}'}
    
    def chat(self, user_message):
        urls = re.findall(r'https?://[^\s]+', user_message)
        results = {}
        
        for url in urls:
            results[url] = self.analyze_url(url)
        
        system_msg = self.create_system_message(results)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7
            )
            
            return {
                'response': response.choices[0].message.content,
                'analysis': results
            }
        except Exception as e:
            return {'error': f'OpenAI error: {str(e)}'}
    
    def create_system_message(self, results):
        base = "You are a cybersecurity expert. Use the phishing analysis below to advise users."
        
        if not results:
            return base
        
        analysis_text = "\n\nPHISHING ANALYSIS:\n"
        for url, result in results.items():
            if 'error' in result:
                analysis_text += f"❌ {url}: Analysis failed\n"
            else:
                status = "🟥 PHISHING" if result.get('is_phishing') else "🟩 SAFE"
                confidence = result.get('confidence', 0)
                analysis_text += f"{status} - {url} (Confidence: {confidence:.1%})\n"
        
        return base + analysis_text

def main():
    print("💬 Phishing Detection Chat")
    print("Type 'quit' to exit\n")
    
    gpt = PhishingGPT()
    
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['quit', 'exit']:
            break
        
        result = gpt.chat(user_input)
        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Assistant: {result['response']}")

if __name__ == "__main__":
    main()