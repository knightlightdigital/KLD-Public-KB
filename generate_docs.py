import os
import requests

# 1. Setup Configuration
OUTLINE_API_URL = os.environ.get("OUTLINE_URL")  # Replace with self-hosted URL if needed
OUTLINE_API_KEY = os.environ.get("OUTLINE_API_KEY")  # Safely load your API Key

HEADERS = {
    "Authorization": f"Bearer {OUTLINE_API_KEY}",
    "Content-Type": "application/json"
}

def fetch_public_docs():
    # Fetch documents from Outline API
    # Outline utilizes POST requests for its RPC-style API endpoints
    response = requests.post(OUTLINE_API_URL, headers=HEADERS, json={})
    
    if response.status_code != 200:
        print(f"Error fetching docs: {response.status_code} - {response.text}")
        return []
        
    all_docs = response.json().get("data", [])
    
    # Filter only documents that have "Share to Web" turned on
    public_docs = []
    for doc in all_docs:
        # Check if the document is published and has a shareUrl active
        if doc.get("publishedAt") and doc.get("shareUrl"):
            public_docs.append({
                "title": doc.get("title"),
                "url": doc.get("shareUrl"),
                "collection": doc.get("collectionId") # Useful if you want to group them
            })
            
    return public_docs

def build_html_page(docs):
    # Base structure of your public static landing page
    links_html = ""
    
    if not docs:
        links_html = "<p class='no-docs'>No public documents available right now.</p>"
    else:
        for doc in docs:
            links_html += f"""
            <div class="doc-card">
                <h3>{doc['title']}</h3>
                <a href="{doc['url']}" target="_blank" class="view-btn">Read Document →</a>
            </div>
            """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Public Documentation Hub</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f9f9fb; color: #111; margin: 0; padding: 40px 20px; }}
            .container {{ max-width: 650px; margin: 0 auto; }}
            h1 {{ font-size: 28px; margin-bottom: 8px; }}
            .subtitle {{ color: #666; margin-bottom: 40px; }}
            .doc-card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #eaeaea; }}
            h3 {{ margin: 0; font-size: 18px; color: #222; }}
            .view-btn {{ text-decoration: none; color: #0066cc; font-weight: 500; font-size: 14px; }}
            .view-btn:hover {{ text-decoration: underline; }}
            .no-docs {{ color: #888; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Public Knowledge Hub</h1>
            <p class="subtitle">Access our official public guides and documentation below.</p>
            <div class="docs-list">
                {links_html}
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save the output directly as your index file
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
    print("Successfully generated index.html with live Outline links!")

if __name__ == "__main__":
    public_documents = fetch_public_docs()
    build_html_page(public_documents)
