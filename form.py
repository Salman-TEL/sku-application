from flask import Flask, request, redirect, url_for, render_template
import ollama
import pandas as pd
import os

app = Flask(__name__)

# Function to generate a response from the LLM using ollama
def generate_llm_response(prompt, model="llama3.2"):
    messages = [
        {
            'role': 'user',
            'content': f"Correct only the spelling errors in the following text, and return *only* the corrected text without any additional explanation or formatting.remove the special characters also . Make the word capitalized and in the last word give an & sign. If there are custom words like 'mangocream,' leave them as they are.and leave the corrected words also please not change or add additional words with correct spelling words Text to correct: '{prompt}'"
        }
    ]
    
    response = ollama.chat(model=model, messages=messages)
    return response['message']['content']

@app.route('/')
def index():
    # Render the HTML form
    return render_template('form.html')  # Ensure 'form.html' is in the 'templates' folder
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Extract data from the form
    production_date = request.form.get('production_date')
    code = request.form.get('code')
    green_coffee_name = request.form.get('green_coffee_name')
    tel_name = request.form.get('tel_name')
    origin = request.form.get('origin')
    producer = request.form.get('producer')
    process = request.form.get('process')
    elevation = request.form.get('elevation')
    region = request.form.get('region')
    variety = request.form.get('variety')
    tasting_notes = request.form.get('tasting_notes')
    tags = request.form.get('tags')

    # Correct the spelling of tasting notes
    corrected_tasting_notes = generate_llm_response(tasting_notes)

    # Create a DataFrame with all the data (save only the corrected tasting notes)
    data = {
        "Production Date": [production_date],
        "Code": [code],
        "Green Coffee Name": [green_coffee_name],
        "TEL Name": [tel_name],
        "Origin": [origin],
        "Producer": [producer],
        "Process": [process],
        "Elevation": [elevation],
        "Region": [region],
        "Variety": [variety],
        "Corrected Tasting Notes": [corrected_tasting_notes],  # Only save corrected tasting notes
        "Tags": [tags]
    }

    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    csv_file_path = "coffee_product_data.csv"
    if os.path.exists(csv_file_path):
        df.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(csv_file_path, index=False)

    return redirect(url_for('success'))  # Redirect to a success page or back to the form
@app.route('/success')
def success():
    return "Form submitted successfully and data saved to CSV!"

if __name__ == '__main__':
    app.run(debug=True)
