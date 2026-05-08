from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# --- NEW: This adds a home page so you don't see 'Not Found' ---
@app.route('/')
def home():
    return "<h1>🌌 Nova Cloud Brain is LIVE</h1><p>Status: Ready to process intelligence.</p>"

@app.route('/nova_fetch', methods=['GET'])
def nova_fetch():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(target_url, headers=headers, timeout=12)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text()) > 40]
            return jsonify({"content": " ".join(paragraphs[:8])})
        return jsonify({"content": "Source access denied."})
    except Exception as e:
        return jsonify({"content": f"Fetch error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
