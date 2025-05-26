import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
import tempfile
from HED_Flask_App.tool_utils.file_utils import allowed_file
from HED_Flask_App.HED_Tool.utils.read import read
from HED_Flask_App.HED_Tool.core.process_patient_alleles import process_patient
from HED_Flask_App.tool_utils.mongodb_utils import spin_up_db, load_patients_mongodb, retrieve_from_mongodb
from dotenv import load_dotenv


# Flask app configuration
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
load_dotenv()

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.getenv("FLASK_KEY")

@app.route('/')
def index():
    """Render the home page."""
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file uploads and process the file."""
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        #Use a temp file to write patient data 
        try:
            with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                temp_file.write(file.stream.read())
                temp_file.flush()

                patient_data = read(temp_file.name)
                patient_db = spin_up_db()
                patient_collections = load_patients_mongodb(patient_db, patient_data)

            output_file_path = os.path.join(os.getcwd(), 'processed_results.txt')
            with open(output_file_path, 'w', encoding='utf-8') as output_file:
                for patient in retrieve_from_mongodb(patient_collections):
                    print(patient)
                    result = process_patient(patient, './HED_tool/resources/alignments', True)
                    output_file.write(f"{result}\n")

            flash('File processed successfully! You can download the results below.')

        except Exception as e:
            flash(f'Unable to process file: {e}')
    
    return redirect(url_for('index'))


@app.route('/download')
def download_file():
    output_file_path = os.path.join(os.getcwd(), 'processed_results.txt')
    try:
        return send_file(output_file_path, as_attachment=True, download_name='processed_results.txt')
    except Exception as e:
        flash(f'Error downloading file: {e}')
        return redirect(url_for('index'))

@app.route('/view_results')
def view_results():
    """Render the results page"""
    output_file_path = os.path.join(os.getcwd(), 'processed_results.txt')

    try:
        with open(output_file_path, 'r', encoding='utf-8') as file:
            results = file.readlines()

    except FileNotFoundError:
        flash('Processed results file not found. Please upload and process a file first.')
        return redirect(url_for('index'))
    
    return render_template('view_results.html', results=results)


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", default=5000)), host="0.0.0.0")
