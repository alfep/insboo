from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random

class InstagramBot:
    def __init__(self, reel_url):
        self.reel_url = reel_url
        self.setup_driver()
    
    def setup_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
    
    def boost_views(self, count=10):
        for i in range(count):
            try:
                self.driver.get(self.reel_url)
                time.sleep(random.randint(3, 7))  # Random delay
                print(f"View {i+1} completed")
            except Exception as e:
                print(f"Error: {e}")
        
        self.driver.quit()

# Usage in app.py
def selenium_boost_worker(config):
    bot = InstagramBot(config["video_url"])
    bot.boost_views(config["amount_of_boosts"])