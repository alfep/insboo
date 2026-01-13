import requests
import uuid

class SMMPanel:
    def __init__(self, url_video, service_id):
        self.url_video = url_video
        self.api_key = "YOUR_API_KEY_HERE"  # Get from SMM panel
        self.endpoints = [
            "https://smm-world.com/api/v2",
            "https://justanotherpanel.com/api/v2", 
            "https://socialpanel.io/api/v2"
        ]
        self.service_id = service_id
        
    def send_boost(self):
        for endpoint in self.endpoints:
            try:
                data = {
                    'key': self.api_key,
                    'action': 'add',
                    'service': self.service_id,
                    'link': self.url_video,
                    'quantity': 500
                }
                
                response = requests.post(endpoint, data=data, timeout=15)
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get('order'):
                        return True
                    elif result.get('error'):
                        print(f"API Error: {result['error']}")
                        continue
                        
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
                
        return False