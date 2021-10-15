from django.db import models
from django.utils.translation import ugettext_lazy as _
import binascii
import os
from django.utils import timezone

# Model for Machines
class Machine(models.Model):
    description = models.CharField(max_length=30)                               # Unique description of the machine
    token = models.CharField(max_length=40)                                     # Authentication token

    # Overwrite the save method to automatically generate a token
    def save(self):
        if not self.token:
            self.token = self.generate_token()
        super(Machine, self).save()

    # Generate a token
    def generate_token(self):
        return binascii.hexlify(os.urandom(20)).decode()

# Model for Parts
class Part(models.Model):
    description = models.CharField(max_length=30)                               # Unique description of the part
    machine = models.CharField(max_length=30)                                   # Machine which processed the part
    start_datetime = models.DateTimeField()                                     # Start of the processing
    end_datetime = models.DateTimeField(default=timezone.now)                   # End of the processing
    anomaly_score = models.DecimalField(max_digits=7, decimal_places=5)         # Cumulated score of all anomalous readings
    finished = models.BooleanField(default=False)                               # Flag if the part is finished

# Model for Logging
class Log(models.Model):
    temperature = models.DecimalField(max_digits=3, decimal_places=1)           # Temperature Reading
    humidity = models.DecimalField(max_digits=3, decimal_places=1)              # Humidity Reading
    volume = models.DecimalField(max_digits=4, decimal_places=1)                # Volume Reading
    part = models.ForeignKey(Part, on_delete=models.CASCADE)                    # Relation to the corresponding part


