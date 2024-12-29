#we import all nescessarry libraries. GPIO for to interact with pins
#Flask to build a web framework using HTML template we created 
# time, sleep and strf time to allow for pausing, returning time in seconds and strf which translates data into readable string.
import RPi.GPIO as GPIO 
from flask import Flask, render_template
from time import sleep, time, strftime
import threading
import requests

# Flask app setup initialise flask application to serve web pages
app = Flask(__name__)
desk_status = "Waiting for motion..."
# A list of a history of all desk status changes, with timestamps.
historical_changes = []

# GPIO setup configure to use BCM numbering 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(4, GPIO.IN)

# Variables used
last_motion_time = 0
motion_detected = False
desk_in_use = False  # Tracks whether the desk is considered "in use"
DELAY = 300

# ThingSpeak config basic variables which hold strings used to access thingspeak features 
THINGSPEAK_API_KEY = "KAOTDMBXVQJM5AGF"
THINGSPEAK_URL = "https://api.thingspeak.com/update"
ALERTS_API_KEY = "TAKegks/Ip1vYrF1wBa"
ALERTS_URL = "https://api.thingspeak.com/alerts/send"

# Function to send data to ThingSpeak which sends either 1 or 0 to thing speal and logs to console
# If data is not sent then we return error code so we can trouble shoot the actual problem.
def send_to_thingspeak(value):
    try:
        response = requests.post(THINGSPEAK_URL, {
            "api_key": THINGSPEAK_API_KEY,
            "field1": value
        })
        if response.status_code == 200:
            print(f"Data sent to ThingSpeak: {value}")
        else:
            print(f"Failed to send data to ThingSpeak. Response code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to ThingSpeak: {e}")

# Function to send email alerts
# Sends an email with a given subject and body using the ThingSpeak Alerts API.
# We send HTTP post to ALERTS_URL address  json holds thepayload and API key stored in headers
# If status code is 200 we posted successfully if not we will see whaterror code is returned and the exception catches and loggs error message.

def send_email_alert(subject, body):
    try:
        response = requests.post(ALERTS_URL, json={
            "subject": subject,
            "body": body
        }, headers={
            "ThingSpeak-Alerts-API-Key": ALERTS_API_KEY,
            "Content-Type": "application/json"
        })
        if response.status_code == 200:
            print(f"Email alert sent: {subject}")
        else:
            print(f"Failed to send email alert. Response code: {response.status_code}")
    except Exception as e:
        print(f"Error sending email alert: {e}")

# Function to handle motion detection main loop we use for the motion detection logic
# We use use other variables and import them here globally, we run an indefinite loop that comnstantly checks the status of the RPI.
# Read input from GPIO pins and return true if motion dtected and false if no motion.
# We then create other conditions that change the status of the desk status eg. if the desk was previously marked as "in use" 
# And it detects motion the desk status changes to desk unoccupied and adds a timestamp to historical_changes 
# send to thingSpeak then sends a corresponding value to thingspeak
# the logic is similar across the board in that depending on a status of the desk corresponding logic is executed
def motion_detection():
    global desk_status, motion_detected, desk_in_use, last_motion_time, historical_changes
    try:
        while True:
            if GPIO.input(4):
                current_time = time()
                if desk_in_use:
                    desk_status = "Desk Unoccupied."
                    historical_changes.append(f"{desk_status} at {strftime('%Y-%m-%d %H:%M:%S')}")
                    send_to_thingspeak(0)
                    send_email_alert("Desk Unoccupied Alert", "The desk is now unoccupied.")
                    print(desk_status)
                    desk_in_use = False
                else:
                    desk_status = f"Motion near desk detected at {strftime('%Y-%m-%d %H:%M:%S')}"
                    historical_changes.append(desk_status)
                    send_to_thingspeak(0)
                    print(desk_status)
                last_motion_time = current_time
                motion_detected = True
            else:
                if motion_detected and time() - last_motion_time > DELAY:
                    desk_status = "Desk in use."
                    historical_changes.append(f"{desk_status} at {strftime('%Y-%m-%d %H:%M:%S')}")
                    send_to_thingspeak(1)
                    send_email_alert("Desk Occupied Alert", "The desk is now occupied.")
                    print(desk_status)
                    motion_detected = False
                    desk_in_use = True
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")
        GPIO.cleanup()

# Flask route to display the desk status and history using created template.html doc to display the data in a simple format. 
@app.route("/")
def index():
    return render_template("template.html", status=desk_status, history=historical_changes)

# Main function to start Flask and motion detection
if __name__ == "__main__":
    # Start the motion detection in a separate thread we start them in speperate thread as flask and motion detection
    # were blocking each other.
    motion_thread = threading.Thread(target=motion_detection)
    motion_thread.daemon = True
    motion_thread.start()

    # Start Flask app
    app.run(host="0.0.0.0", port=5000)
