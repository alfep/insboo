import requests
import uuid

class Zefame:
    def __init__(self, url_video, service_id):
        self.url_video = url_video
        self.service_id = service_id
        
        # Extract reel ID
        try:
            url_parts = url_video.split("/")
            if "reel" in url_parts:
                reel_index = url_parts.index("reel")
                self.post_id = url_parts[reel_index + 1] if reel_index + 1 < len(url_parts) else ""
            else:
                self.post_id = url_parts[4] if len(url_parts) > 4 else ""
        except:
            self.post_id = ""
        
        # Multiple API endpoints (Zefame + Free APIs)
        self.apis = [
            # Original Zefame
            {
                'url': 'https://zefame-free.com/api_free.php?action=order',
                'data': {
                    'service': service_id,
                    'link': url_video,
                    'uuid': str(uuid.uuid4()),
                    'postId': self.post_id
                },
                'headers': {
                    'content-type': 'application/x-www-form-urlencoded',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
            },
            # Free API 1
            {
                'url': 'https://freeviews.net/api/boost',
                'data': {
                    'link': url_video,
                    'service': 'views',
                    'count': 100
                },
                'headers': {'content-type': 'application/x-www-form-urlencoded'}
            },
            # Free API 2
            {
                'url': 'https://viewsup.com/free-api',
                'data': {
                    'url': url_video,
                    'type': 'instagram_views',
                    'amount': 50
                },
                'headers': {'content-type': 'application/x-www-form-urlencoded'}
            }
        ]
        
        self.session = requests.session()

    def send_boost(self):
        for i, api in enumerate(self.apis):
            try:
                print(f"Trying API {i+1}: {api['url']}")
                response = self.session.post(
                    api['url'], 
                    data=api['data'], 
                    headers=api['headers'], 
                    timeout=15
                )
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        if result.get('success') or result.get('status') == 'success':
                            print(f"API {i+1} success!")
                            return True
                    except:
                        if 'success' in response.text.lower():
                            print(f"API {i+1} success (text response)!")
                            return True
                            
            except Exception as e:
                print(f"API {i+1} failed: {e}")
                continue
        
        print("All APIs failed")
        return False