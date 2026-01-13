import requests
import uuid

class Zefame:
    def __init__(self, url_video,service_id):
        self.url_video = url_video
        # Try different endpoints
        self.endpoints = [
            "https://zefame-free.com/api_free.php?action=order",
            "https://zefame.com/api_free.php?action=order",
            "https://api.zefame.com/free?action=order"
        ]
        self.uuid = str(uuid.uuid4())
        
        # Extract reel ID safely
        try:
            url_parts = url_video.split("/")
            if "reel" in url_parts:
                reel_index = url_parts.index("reel")
                post_id = url_parts[reel_index + 1] if reel_index + 1 < len(url_parts) else ""
            else:
                post_id = url_parts[4] if len(url_parts) > 4 else ""
            print(f"Extracted post_id: {post_id} from URL: {url_video}")
        except Exception as e:
            print(f"Error extracting post_id: {e}")
            post_id = ""
        
        self.data = {
            "service": service_id,
            "link": url_video,
            "uuid": self.uuid,
            "postId": post_id
        }
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=1, i",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referrer": "https://zefame.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        }
        self.session = requests.session()

    def send_boost(self):
        # Try different endpoints
        for endpoint in self.endpoints:
            try:
                print(f"Trying endpoint: {endpoint}")
                response = self.session.post(endpoint, data=self.data, headers=self.headers, timeout=15)
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        resp_json = response.json()
                        print(f"Response JSON: {resp_json}")
                        
                        if resp_json.get('success') == True:
                            return True
                        elif (
                            isinstance(resp_json.get('data'), dict) and
                            resp_json['data'].get('timeLeft') is not None
                        ):
                            return resp_json['data']['timeLeft']
                    except:
                        print(f"Non-JSON response: {response.text[:200]}")
                        
            except Exception as e:
                print(f"Error with {endpoint}: {e}")
                continue
        
        print("All endpoints failed")
        return False