from flask import Flask, render_template, request
import os
import json
import io
import matplotlib.pyplot as plt
from whatsapp_profiler import profile_whatsapp_messages
from tribe_personality_classifier import identify_tribe
from bart_work_personality_classifier import identify_work_personality

# this file along with the template folder HTML files make up the Flask web interface. To use it, just run this file and open the interface on your web browser.
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/upload', methods=['GET'])
def upload_file():
    return render_template('upload.html')

@app.route('/classify_tribe', methods=['GET', 'POST'])
def classify_tribe():
    if request.method == 'POST':
        input_text = request.form['input_text1']
        results = identify_tribe(input_text)
        return render_template('classify_tribe.html', results=results)
    return render_template('classify_tribe.html', results="")

@app.route('/classify_work_personality', methods=['GET', 'POST'])
def classify_work_personality():
    if request.method == 'POST':
        input_text = request.form['input_text2']
    # Call your Python function to analyze the input_text here
        results = identify_work_personality(input_text)
        return render_template('classify_work_personality.html', results=results)
    return render_template('classify_work_personality.html', results="")

@app.route('/analyze', methods=['POST'])
def analyze_file():
    file = request.files['file']
    # Call your Python function to analyze the file here
    # and get the results
    if 'file' in request.files:
        file = request.files['file']
        # Save the uploaded file to a temporary location
        temp_filepath = os.path.join('/tmp', file.filename)
        file.save(temp_filepath)
        # Call your Python function to analyze the file by its path here
        data_structure = analyze_whatsapptext(temp_filepath)
        # Optionally, you can remove the temporary file after analysis is done
        os.remove(temp_filepath)
        return render_template('result.html', results_json=json.dumps(data_structure).replace("\\", "\\\\").replace("'", r"\'"))
    else:
        return "No file uploaded."

def analyze_whatsapptext(filepath):
    # Implement your analysis logic here
    # You can read the file and process the data
    # Return the results of the analysis as a string
    # Example:
    # Perform analysis on the text
    return profile_whatsapp_messages(filepath)

    # the following commented out code is a dummy object to test things out on the interface with
    # results = {
    #     "Person 1": [
    #         {'ant': {'percentage': 0.5, 'phrases': ["Ant phras'e 1", "Ant phrase 2"]},
    #          'bee': {'percentage': 0.3, 'phrases': ["Bee ph'rase 1", "Bee phrase 2"]},
    #          'leech': {'percentage': 0.2, 'phrases': ["Leech phrase 1", "Leech phrase 2"]}},
    #         {'fatherlander': {'percentage': 0.25, 'phrases': ["Father p\hrase 1", "Father phrase 2"]},
    #          'treehugger': {'percentage': 0.35, 'phrases': ["Treehugger phrase 1", "Treehugger phrase 2"]},
    #          'nerd': {'percentage': 0.2, 'phrases': ["Nerd phrase 1", "Nerd phrase 2"]},
    #          'spiritualist': {'percentage': 0.2, 'phrases': ["Spiritualist phrase 1", "Spiritualist phrase 2"]}}
    #     ],
    #     "Person 2": [
    #         {'ant': {'percentage': 0.7, 'phrases': ["Ant phrase 1", "Ant phrase 2"]},
    #          'bee': {'percentage': 0.1, 'phrases': ["Bee phrase 1", "Bee phrase 2"]},
    #          'leech': {'percentage': 0.2, 'phrases': ["Leech phrase 1", "Leech phrase 2"]}},
    #         {'fatherlander': {'percentage': 0.3, 'phrases': ["Father phrase 1", "Father phrase 2"]},
    #          'treehugger': {'percentage': 0.3, 'phrases': ["Treehugger phrase 1", "Treehugger phrase 2"]},
    #          'nerd': {'percentage': 0.2, 'phrases': ["Nerd phrase 1", "Nerd phrase 2"]},
    #          'spiritualist': {'percentage': 0.2, 'phrases': ["Spiritualist phrase 1", "Spiritualist phrase 2"]}}
    #     ]
    # }
    # return results

if __name__ == '__main__':
    app.run()