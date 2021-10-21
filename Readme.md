# Factory Anomaly Detection 
## Overview
The Factory Anomaly Detection is a package for simulating anomaly detection in a factory setting. The package consists of a Python script for
generating and sending simulated sensor readings and a Django-based web application that receives and interprets the received values. 
The web application features a REST-API for communication with the simulation script and a machine learning model based on the isolation forest algorithm
for detecting anomalies. 

## Features
* Registration of new machines
* Token authentication
* Logging of sensor values
* Download of stored data in CSV format
* Listing of key metrics for machined parts

## Installation
To use the anomaly detection package you need an installation of Python 3.9.0
1. Download the repository and extract the contents.
2. Install `pipenv` with `pip install pipenv` if you do not have it already installed.
3. Move the folders Model and Simulation to another directory.
4. To setup the web application open a command prompt inside the main folder and type `pipenv install`.
5. Enter the virtual environment with `pipenv shell`. 
6. First enter the command `py manage.py migrate` and following the command `py manage.py createsuperuser`.
7. Follow the instructions on the command prompt and then launch the web application with `py manage.py runserver`.
8. Open http://127.0.0.1:800/ with a web browser.
9. To setup the simulation script open a separate command prompt inside the Simulation folder.
10. Create and enter the virtual environment like described in steps 4 and 5.

## Usage
For registering machines and inspecting parts refer to the instructions on the homepage of the web application.
To start simulating sensor data you must first register a new machine. After registration open the `process.py`
file inside the Simulation folder with a text editor. Scroll to the end of the file and replace the default machine's credentials
with the information of the newly registered machine. Replace the default part's description with your own part and save the file.
Type `py process.py` to start sending sensor data and wait until no more sensor data is generated.

