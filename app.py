from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

# --- THE CORE INTELLIGENCE LOGIC ---
def deep_fetch(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract paragraphs that actually contain content
            paragraphs = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text()) > 50]
            return " ".join(paragraphs[:5])
        return ""
    except:
        return ""

@app.route('/nova_fetch', methods=['GET'])
def nova_fetch():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400
    
    content = deep_fetch(target_url)
    return jsonify({"content": content})

if __name__ == "__main__":
    # Render and Heroku use the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
