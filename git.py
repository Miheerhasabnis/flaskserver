import re
import requests
from googlesearch import search
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

def extract_emails_from_text(text):
    # Define a regex pattern to match email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[\w.-]+'
    return re.findall(email_pattern, text)

def scrape_emails_from_query(query, num_results=5):
    emails = set()  # To store unique email addresses
    # Collect search results
    urls = list(search(query))  # Get all results without limiting
    for url in urls[:num_results]:  # Limit to num_results
        try:
            # Send a GET request to the URL
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()  # Get all text from the page
            
            # Extract emails from the text
            emails.update(extract_emails_from_text(text))
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
    
    return list(emails)

@app.route('/', methods=['GET'])
def extract_emails():
    # Get query parameters from the URL
    search_query = 'email of bajaj' # Extract the query
    num_results = 5;  # Extract the number of results as an integer
    
    # Call the email scraping function
    emails = scrape_emails_from_query(search_query, num_results)
    
    # Return the emails as a JSON response
    return jsonify(emails)

if __name__ == '__main__':
    app.run(debug=False)
