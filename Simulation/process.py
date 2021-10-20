import requests
from random import randint
from time import sleep
import numpy as np
import pandas as pd
import pickle

# Authentication via Token

# Maschine simulieren
class machine():

        def __init__(self, description, token):
            self.machine_desc = description
            self.token = token
            self.url = 'https://factory-anomaly-detection.herokuapp.com/api/predict/'
            self.headers = {'Authorization': self.token}
            self.isof = pickle.load(open('isof.model', 'rb'))

        def process(self, description):
            body = {
                'action': 'new',
                'description': description,
                'machine': self.machine_desc
            }

            response = requests.post(url=self.url, headers=self.headers,
                                     data = body)
            
            # Check if the request has been accepted
            if response.json()['Status'] == 401:
                print('Unauthorized Request')
            
            elif response.json()['Status'] == 'Part Created':
                # Save the ID of the current part
                self.current_part = response.json()['Part_ID']
                # Print the response
                print(response.json())

                # Generate a random number of sensor values (Frequency is 2Hz and part duration is from 1 to 5 minutes)
                sensor_count = randint(120, 600)
                val_temp = np.random.normal(25, 5, sensor_count)
                val_hum = np.random.normal(60, 5, sensor_count)
                val_vol = np.random.normal(100, 10, sensor_count)
                data = np.column_stack((val_temp, val_hum, val_vol))
                
                # Convert the data into a dataframe
                df = {'Temperature': val_temp, 'Humidity': val_hum, 'Volume': val_vol}
                df = pd.DataFrame(data=df)

                # Predict the labels and add them to the DataFrame
                df['outlier'] = self.isof.predict(data)

                # Extract all outliers of the generated data
                outliers = df.loc[(df['outlier'] == -1)]

                # Delete all the outliers from the original data
                df = df.loc[(df['outlier']) != -1]

                # Reeindex the dataframe
                df.reset_index(inplace=True, drop=True)

                # Split the original data a random point
                df_beg = df.iloc[:randint(0, df.shape[0]-1)]
                df_end = df.iloc[df_beg.shape[0]:]

                # Concatenate the data
                df = pd.concat([df_beg, outliers, df_end])

                # Reindex the dataframe
                df.reset_index(inplace=True, drop=True)

                # Drop the outlier column
                df.drop(columns=['outlier'], inplace=True)

                # Convert the data into a dictionary
                data = df.to_dict('records')

                for row in data:
                    body = {
                        'action': 'log',
                        'machine': self.machine_desc,
                        'part': self.current_part,
                        'temperature': row['Temperature'],
                        'humidity': row['Humidity'],
                        'volume': row['Volume']
                    }
                    response = requests.post(url=self.url, headers=self.headers,
                                            data = body)
                    print(response.json())
                    # Wait for 500ms (Send data with 2Hz Frequency)
                    sleep(0.5)

                # Set the finished flag for the part
                body = {
                    'action': 'finish',
                    'machine': self.machine_desc,
                    'part': self.current_part
                }

                response = requests.post(url=self.url, headers=self.headers,
                                        data = body)
                print(response.json())
            

if __name__ == "__main__":
    # Create a new machine
    milling_01 = machine('milling_01', 'd9a0a598827225261a7e4360927fd1d565ce9f5e')

    # Create a new part
    milling_01.process('part_001')



  
