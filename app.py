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
    if not target_url: return jsonify({"content": "No URL"})
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(target_url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- SMART CLEANING: Removes the junk menus and footers ---
        for junk in soup(['nav', 'footer', 'header', 'script', 'style', 'aside']):
            junk.decompose()

        # Only pull text from paragraphs and articles
        main_content = []
        for tag in soup.find_all(['p', 'article']):
            text = tag.get_text().strip()
            # Only keep real sentences (more than 12 words)
            if len(text.split()) > 12:
                main_content.append(text)

        clean_text = " ".join(main_content[:10]) # Get the best 10 paragraphs
        return jsonify({"content": clean_text if clean_text else "No main text found."})
    except Exception as e:
        return jsonify({"content": f"Fetch error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
