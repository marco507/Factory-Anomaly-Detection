from django.db.models.base import Model
from django.shortcuts import render
import numpy as np
from .apps import ApiConfig as api
from rest_framework.views import APIView
from rest_framework.response import Response
from administration.models import Machine, Part, Log
from django.utils import timezone
from decimal import Decimal

# Define view for handling predictions
class Prediction(APIView):

    # Handle a POST request
    def post(self,request):
        # Save the data from the request
        data = request.data

        # Check if the request is from a registered machine
        if Machine.objects.filter(token=request.headers['Authorization'], description=data['machine']): 

            # New part should be created
            if data['action'] == 'new':
                new_part = Part(description=data['description'],
                                machine=data['machine'],
                                start_datetime=timezone.now(),
                                anomaly_score=0)
                new_part.save()

                # Return the ID of the part and a success message
                return Response({'Status': 'Part Created', 'Part_ID': new_part.id}) 

            # Log values and predict for existing part
            elif data['action'] == 'log':
                # Query the part
                part = Part.objects.get(pk=data['part'])
                # Log the data
                new_log = Log(temperature=data['temperature'],
                              humidity=data['humidity'],
                              volume=data['volume'],
                              part=part)
                new_log.save()
                
                # Process the data for prediction
                data = np.column_stack((float(data['temperature']), float(data['humidity']), float(data['volume'])))
                # Make a prediction
                classification = api.model.predict(data)
                anomaly_score = api.model.decision_function(data)

                # Compute the cumulative anomaly score (Negative scores are anomalous)
                if anomaly_score < 0:
                    part.anomaly_score += Decimal(anomaly_score[0])
                    part.save()

                return Response({'Prediction': classification, 'AnomalyScore' : anomaly_score,
                                 'CumulativeAnomalyScore' : part.anomaly_score})

            # Finish the part
            elif data['action'] == 'finish':
                # Set the end datetime
                finished_part = Part.objects.get(id=data['part'])
                finished_part.end_datetime = timezone.now()
                finished_part.finished = True
                finished_part.save()

                return Response({'Status': 'Part Finished', 'Part_ID' : finished_part.id})

        # Unauthorized request
        else:
            return Response({'Status': 401})



        
