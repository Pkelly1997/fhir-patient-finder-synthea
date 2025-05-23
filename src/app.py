import requests
import os
from flask import Flask, request, render_template
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()

FHIR_SERVER_BASE_URL=os.getenv("FHIR_SERVER_BASE_URL")
username = os.getenv("FHIR_USERNAME")
password = os.getenv("FHIR_PASSWORD")

def request_patient(patient_id, credentials):

    req = requests.get(FHIR_SERVER_BASE_URL + "/Patient/" + str(patient_id), auth = credentials)

    print(f"Requests status: {req.status_code}")

    response = req.json()
    print(response.keys())

    return response



@app.route('/', methods=['GET', 'POST'])
def index():

    result = None
    credentials = (username, password)

    if request.method == 'POST':
        try:
            number = int(request.form['number'])
            result = request_patient(number, credentials=credentials)
        except ValueError:
            result = 'Invalid input. Please enter a number.'

    return render_template('index.html', result=result)

if __name__ == '__main__':
    port_str = os.environ['FHIR_PORT']
    port_int = int(port_str)
    app.run(debug=True, port=port_int)