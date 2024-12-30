#Motion Detector System with Desk Status Monitoring
Overview
This project implements a motion detection system using a Raspberry Pi and a PIR motion sensor.
The system monitors the status of a desk, determines whether it is occupied or unoccupied,
and sends updates to ThingSpeak for logging and visualization.
Additionally, email alerts are sent for prolonged desk occupancy or inactivity.
A web interface powered by Flask provides real-time desk status and historical activity logs.
Lastly we are saving all logs in a seperate file which should be created when program launches and writes
to it lasting histrical changes.

Features
Detects motion near a desk using a PIR motion sensor.
Determines if the desk is occupied or unoccupied based on motion activity.
Sends desk status updates to ThingSpeak.
Triggers email alerts for:
Prolonged desk occupancy (30+ minutes).
Prolonged inactivity  5+ minutes).
Provides a web interface to display:
Current desk status.
Historical activity logs
.
Hardware Requirements
Raspberry Pi (tested on Raspberry Pi 4B).
PIR Motion Sensor.
Breadboard and jumper wires for prototyping (although not nescessary)
Internet connection for the Raspberry Pi.
Software Requirements
Python 3.6+ installed on the Raspberry Pi.
MATLAB for ThingSpeak-based email alert functionality.

Required Python libraries:
RPi.GPIO
Flask
requests
As well as sleep and time functions to take account of the passing seconds

Installation and Setup
1.Hardware Setup
Connect the PIR motion sensor to the Raspberry Pi as follows:
VCC → 5V or 3.3V GPIO pin on Raspberry Pi.
GND → Ground pin on Raspberry Pi.
OUT → GPIO4 (Pin 7 on Raspberry Pi).

2 Clone the Repository
Clone the project repository to your Raspberry Pi:
bash
Copy code
git clone https://github.com/Kszlufik/motion-detector-system.git
cd motion-detector-system

3 Install Dependencies
Install the required Python libraries:
bash
Copy code
pip install Flask requests RPi.GPIO

4.Configure ThingSpeak and Alerts
ThingSpeak Setup:
Create a ThingSpeak channel.
Channel ID and read/write api keys will change depending on user,  generate a Read API Key and Write API Key.
ThingSpeak Alerts:
Enable alerts and generate an Alerts API Key.
Update the following variables in motion-detector-system.py:
THINGSPEAK_API_KEY: Write API Key for ThingSpeak.
ALERTS_API_KEY: Alerts API Key for ThingSpeak.
Update the following variables in the MATLAB function:

channelID: ThingSpeak Channel ID.
readAPIKey: Read API Key for ThingSpeak.

5 Run the Flask Application
Start the Flask web interface and motion detection system:

Run python3 motion-detector-system.py
Access the web interface in your browser at address provided http address.
It should display something like: 
http://RaspberryPi_IP:5000
Replace RaspberryPi_IP with the IP address of your Raspberry Pi.

6 Schedule MATLAB for Alerts
To automate MATLAB executio  use a scheduled task monitorDeskStatus function the code is also provided on git.

File Structure

How It Works
Motion Detection:
The PIR sensor detects motion and updates the desk's status as "Occupied" or "Unoccupied."
ThingSpeak Integration:
Sends updates (0 for unoccupied, 1 for occupied) to ThingSpeak for logging and visualization.
Email Alerts:
Alerts are sent via ThingSpeak for:
Desk occupied for over 30 minutes.
Desk unoccupied for over 5 minutes
Des is now "occupied" after 5 minutes pass
Desk is now unoccupied if motion is detected at the desk again after 5 min pass.
Flask Web Interface:
Displays the current desk status and historical activity logs.
Usage
Monitor desk usage in an office or study environment.
Log and visualize desk activity using ThingSpeak.
Receive email alerts for prolonged desk usage or inactivity.

Future Improvements
Add mobile notifications for desk status changes.
Enhance the web interface with live updates.
Add support for multiple desks with additional sensors.
Contributors
Kamil Szlufik  - Project Developer
License
