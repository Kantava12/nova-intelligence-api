from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🌌 Nova Cloud Brain is LIVE</h1>"

@app.route('/nova_fetch', methods=['GET'])
def nova_fetch():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"content": "No URL provided"})
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Get all paragraph text
        text_content = " ".join([p.get_text() for p in soup.find_all('p')])
        # Return just the first 3000 characters to keep it fast
        return jsonify({"content": text_content[:3000]})
    except Exception as e:
        return jsonify({"content": f"Fetch error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
