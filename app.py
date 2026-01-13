from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import re
import threading
import time
from zefame import Zefame

app = Flask(__name__)

CONFIG_FILE = "config.json"
boost_status = {"running": False, "progress": 0, "total": 0}

quantity_types = {'views': 500, 'likes': 20}
delay_types = {'views': 5, 'likes': 3}
service_id = {'views': 237, 'likes': 234}

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            print(f"Config loaded: {data}")  # Debug log
            return data
    except Exception as e:
        print(f"Config load error: {e}")  # Debug log
        # Create default config
        default_config = {"video_url": "https://www.instagram.com/reel/DTVOdboiRvC/", "amount_of_boosts": 100, "type": "views"}
        save_config(default_config)
        return default_config

def save_config(data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Config saved: {data}")  # Debug log
    except Exception as e:
        print(f"Config save error: {e}")  # Debug log

def is_valid_reel_url(url):
    # Clean URL first
    url = url.replace('&amp;', '&')
    pattern = r"^https?://(www\.)?instagram\.com/reel/[\w\-]+/?.*$"
    result = re.match(pattern, url) is not None
    print(f"URL validation: {url} -> {result}")  # Debug log
    return result

def clean_instagram_url(url):
    """Clean Instagram URL from tracking parameters"""
    # Decode HTML entities
    url = url.replace('&amp;', '&')
    
    if "/reel/" in url:
        parts = url.split("/reel/")
        if len(parts) > 1:
            reel_id = parts[1].split("/")[0].split("?")[0]
            return f"https://www.instagram.com/reel/{reel_id}/"
    return url

def boost_worker(config):
    global boost_status
    boost_status["running"] = True
    boost_status["progress"] = 0
    boost_status["total"] = config["amount_of_boosts"]
    
    zefame = Zefame(config["video_url"], service_id[config["type"]])
    used = 0
    
    while used < config["amount_of_boosts"] and boost_status["running"]:
        response = zefame.send_boost()
        if response == True:
            used += 1
            boost_status["progress"] = used
        elif isinstance(response, int):
            time.sleep(response)
        else:
            time.sleep(delay_types[config["type"]])
    
    boost_status["running"] = False

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "Insta-Booster is running"})

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update_config', methods=['POST'])
def update_config():
    config = load_config()
    
    if 'video_url' in request.form:
        url = clean_instagram_url(request.form['video_url'])
        if is_valid_reel_url(url):
            config['video_url'] = url
        else:
            return jsonify({"error": "Invalid Instagram Reel URL"})
    
    if 'amount_of_boosts' in request.form:
        try:
            config['amount_of_boosts'] = int(request.form['amount_of_boosts'])
        except ValueError:
            return jsonify({"error": "Invalid boost amount"})
    
    if 'type' in request.form:
        config['type'] = request.form['type']
    
    save_config(config)
    return jsonify({"success": True})

@app.route('/start_boost', methods=['POST'])
def start_boost():
    if boost_status["running"]:
        return jsonify({"error": "Boost already running"})
    
    config = load_config()
    print(f"Start boost config: {config}")  # Debug log
    
    if not config.get('video_url') or not is_valid_reel_url(config['video_url']):
        print(f"Invalid URL: {config.get('video_url')}")  # Debug log
        return jsonify({"error": "Please set a valid Instagram Reel URL first"})
    
    thread = threading.Thread(target=boost_worker, args=(config,))
    thread.start()
    
    return jsonify({"success": True})

@app.route('/stop_boost', methods=['POST'])
def stop_boost():
    boost_status["running"] = False
    return jsonify({"success": True})

@app.route('/status')
def status():
    return jsonify(boost_status)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)