from flask import Flask, render_template, request, jsonify
import json
import re

app = Flask(__name__, template_folder='../templates')

def load_config():
    try:
        with open('../config.json', 'r') as f:
            return json.load(f)
    except:
        return {"video_url": "", "amount_of_boosts": 100, "type": "views"}

def is_valid_reel_url(url):
    pattern = r"^https?://(www\.)?instagram\.com/reel/[\w\-]+/?$"
    return re.match(pattern, url) is not None

def clean_instagram_url(url):
    if "/reel/" in url:
        parts = url.split("/reel/")
        if len(parts) > 1:
            reel_id = parts[1].split("/")[0].split("?")[0]
            return f"https://www.instagram.com/reel/{reel_id}/"
    return url

@app.route('/')
def index():
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/update_config', methods=['POST'])
def update_config():
    return jsonify({"error": "Config update disabled on Vercel"})

@app.route('/start_boost', methods=['POST'])
def start_boost():
    return jsonify({"error": "Boost feature disabled on Vercel serverless"})

@app.route('/status')
def status():
    return jsonify({"running": False, "progress": 0, "total": 0})

# Vercel handler
app = app