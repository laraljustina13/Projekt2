from flask import Flask, render_template, jsonify
from utils.mongo_client import get_patients_by_cohort, get_patient_by_id
from config import TARGET_GENES

app = Flask(__name__)

@app.route('/')
def index():
    """Početna stranica s vizualizacijom"""
    return render_template('index.html', cohorts=['coad', 'brca', 'luad'], target_genes=TARGET_GENES)

@app.route('/api/patients/<cohort_name>')
def get_patients(cohort_name):
    """API endpoint za pacijente u kohorti"""
    try:
        patients = get_patients_by_cohort(cohort_name)
        # Ukloni _id iz svakog pacijenta za čisti JSON
        for patient in patients:
            if '_id' in patient:
                del patient['_id']
        return jsonify(patients)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/patient/<patient_id>')
def get_patient(patient_id):
    """API endpoint za pojedinog pacijenta - SA SVIM PODACIMA"""
    try:
        patient = get_patient_by_id(patient_id)
        if patient:
            # Ukloni _id za čisti JSON
            if '_id' in patient:
                del patient['_id']
            return jsonify(patient)
        else:
            return jsonify({'error': 'Patient not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)