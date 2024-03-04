from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle
import numpy as np
import json

app = Flask(__name__)

model_path = './piper.pkl'

with open(model_path, 'rb') as file:
    model = pickle.load(file)

def send_email(subject, body):
    sender_email = "<Sender Email>"
    receiver_email = "<Receiver Email>"
    password = "<App Password>"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    detailed_body = """
    {}
    
    A freeze condition has been detected and is likely to occur soon. To prevent your pipes from freezing and potentially bursting, please take the following precautions immediately:
    
    1. **Open Cabinet Doors**: Open kitchen and bathroom cabinet doors to allow warmer air to circulate around the plumbing, especially if your sinks are on an exterior wall.
    
    2. **Let Faucets Drip**: Allow the faucet to drip slightly (both hot and cold water) to relieve pressure in the system. Even a trickle of water can prevent pipes from freezing.
    
    3. **Seal Leaks**: Use caulk or insulation to seal leaks around doors and windows to keep cold air out, especially where pipes are located.
    
    4. **Extra Insulation**: Add extra insulation to attics, basements, and crawl spaces. Insulation will maintain higher temperatures in those areas.
    
    5. **Keep the Thermostat Set**: Keep your thermostat set to the same temperature during both day and night. During a cold snap, it is not advisable to lower the temperature at night.
    
    6. **Portable Heaters**: Use portable heaters carefully to warm up areas where pipes are frozen or are at risk of freezing. Never leave heaters unattended.
    
    7. **Disconnect Garden Hoses**: Disconnect, drain, and store garden hoses. Close inside valves supplying outdoor hose bibs and open the outside hose bibs to drain.
    
    Taking these steps can help prevent your pipes from freezing and avoid the costly damage of burst pipes.
    
    Stay warm and safe,
    [Dr.Piper]
    """.format(body)

    message.attach(MIMEText(detailed_body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route('/log', methods=['POST'])
def receive_log():
    global last_alert_time
    print(request)
    data = request.data
    print("Received data:", data)
    decoded_data = data.decode('utf-8')

    data = json.loads(decoded_data)

    try:
        temperature = data['Temperature']
        water_flow = data['Water Flow']
        default_values = {
            'Pipe Material': 0,#'PVC'
            'Pipe Insulation': 1,#'Low'
            'Pipe Diameter (cm)': 5,
            'Pipe Length (m)': 10,
            'Exposure to Wind': 1,#'Low'
            'Humidity (%)': 50,
            'Pipe Location': 1, #'Basement'
            'Air Circulation': 1 #'Moderate'
        }
    except KeyError:
        return jsonify({"status": "error", "message": "Missing data in request"}), 400

    features = np.array([temperature, water_flow] + list(default_values.values())).reshape(1, -1)

    prediction = model.predict(features)

    current_time = datetime.now()
    if prediction[0] == 1 and (last_alert_time is None or current_time - last_alert_time >= timedelta(hours=1)):
        last_alert_time = current_time
        send_email("Freeze Alert", "A freeze condition is likely to occur.")
        response_message = "Freeze alert sent."
    else:
        response_message = "No alert sent."
    
    # Respond to the AVR-IoT Cellular Mini with success status
    return jsonify({"status": "success", "message": "Data received"}), 200


@app.route('/', methods=['GET'])
def hello():
    return jsonify({"status": "success", "message": "Data received"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
