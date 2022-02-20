from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Using a dictionary for the in-memory storage
# Not best practice but convenient for take-home project
schedule_storage = {}

@app.route('/')
def hello():
    return 'Welcome to the Appointment Service API -- read the READme on how to use'

@app.route('/set-appointment', methods=['POST'])
def set_appointment():
    user_id = request.form['userid']
    date = request.form['date']
    # Handle bad inputs
    invalid_params = ["", None] # TODO expand to handle more invalid types
    if date in invalid_params or user_id in invalid_params:
        return "INVALID PARAMETERS", 400

    date_object = datetime.strptime(date, '%m/%d/%Y %H:%M')

    # TODO: Move this logic into a sperate module with classes and functions

    # Check if appointment is set at the start of hour or half hour
    # valid --> 9:00, 9:30
    # invalid --> 9:05, 9:36
    minute = date_object.minute
    if minute not in [0, 30]:
        return "PLEASE ONLY SET APPOINTMENTS AT THE BEGINING OF HOUR OR HALF HOUR E.G 9:00 OR 9:30", 400

    appointments = schedule_storage.get(user_id, None)

    # checks whether an appointment is already set for that day
    if appointments:
        for appointment in appointments:
            if date_object.date() == appointment.date():
                return "CANNOT CREATE APPOINTMENT BECAUSE ONE IS ALREADY SET", 400
        
        # If we get to this point then that means this appointment can be set
        appointments.append(date_object)
        schedule_storage[user_id] = appointments
    else:
        schedule_storage[user_id] = [date_object]

    return jsonify(schedule_storage)

@app.route('/view-appointments', methods=['GET'])
def view_appointment():
    user_id = request.args['userid']
    appointments = schedule_storage.get(user_id)

    return jsonify(appointments)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=82)
