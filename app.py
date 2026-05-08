from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
import re

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>🌌 Nova Cloud Brain is LIVE</h1>"

@app.route('/nova_fetch', methods=['GET'])
def nova_fetch():
    target_url = request.args.get('url')
    if not target_url: return jsonify({"content": "No URL"})
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Clean the page
        for junk in soup(['nav', 'footer', 'header', 'script', 'style', 'aside', 'form']):
            junk.decompose()

        # Find only real paragraphs
        paragraphs = [p.get_text().strip() for p in soup.find_all('p') if len(p.get_text().split()) > 15]
        
        # Take the top 3 paragraphs and clean them up
        full_text = " ".join(paragraphs[:3])
        clean_text = re.sub(r'\s+', ' ', full_text) # Fix weird spacing
        
        return jsonify({"content": clean_text if clean_text else "I found the site, but couldn't extract clear text."})
    except Exception as e:
        return jsonify({"content": f"Cloud Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
