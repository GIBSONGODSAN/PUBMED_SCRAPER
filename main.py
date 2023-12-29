import subprocess
from flask import Flask, render_template, request
import os
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Read the contents of scraped_data.json if it exists
    scraped_data = []
    file_path = '/sccraper/wikiscraper/scraped_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                scraped_data = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding JSON file or file is empty")

    return render_template('index.html', scraped_data=scraped_data)

@app.route('/submit', methods=['POST'])
def submit():
    search_term = request.form['search_term']
    
    # Change directory to /sccraper/wikiscraper
    os.chdir('/sccraper/wikiscraper')

    # Delete the contents of output.json if it exists
    output_file = '/sccraper/wikiscraper/output.json'
    if os.path.exists(output_file):
        open(output_file, 'w').close()  # Clears the file by opening it in write mode

    # Run the Scrapy crawl command with correct escaping for quotes
    command = f'scrapy crawl pubmed -a query="{search_term}" -o output.json'
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)

        # Read the scraped data directly from the output file
        scraped_data = []
        if os.path.exists(output_file):
            with open(output_file, 'r') as file:
                try:
                    scraped_data = json.load(file)
                except json.JSONDecodeError:
                    print("Error decoding JSON file or file is empty")

        return render_template('submit.html', scraped_data=scraped_data)
    except subprocess.CalledProcessError as e:
        return f"Error occurred"

if __name__ == '__main__':
    app.run(host='192.168.1.4', port=80, debug=True)

