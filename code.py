import requests
import os
import re

# Function to download files
def download_file(url, folder):
    try:
        response = requests.get(url)
        filename = os.path.join(folder, url.split('/')[-1])
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

# Define the URL of the website you want to scrape
url = "https://www.iplt20.com/stats/2025"  # Replace with the target website URL

# Create a folder to save files
os.makedirs('website_files', exist_ok=True)

# Fetch the website's HTML content
response = requests.get(url)
html_content = response.text

# Save the HTML content
with open(os.path.join('website_files', 'index.html'), 'w', encoding='utf-8') as file:
    file.write(html_content)
print("Saved HTML content.")

# Extract CSS file URLs using regex
css_files = re.findall(r'<link[^>]*href="([^"]+\.css)"', html_content)
for css_file in css_files:
    # Handle relative URLs (e.g., /styles/main.css)
    if not css_file.startswith(('http://', 'https://')):
        css_file = f"{url.rstrip('/')}/{css_file.lstrip('/')}"
    download_file(css_file, 'website_files')

# Extract JavaScript file URLs using regex
js_files = re.findall(r'<script[^>]*src="([^"]+\.js)"', html_content)
for js_file in js_files:
    # Handle relative URLs (e.g., /scripts/main.js)
    if not js_file.startswith(('http://', 'https://')):
        js_file = f"{url.rstrip('/')}/{js_file.lstrip('/')}"
    download_file(js_file, 'website_files')
