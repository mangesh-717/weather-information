from django.db import models

# Create your models here.
class weatherdata(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    location=models.CharField(max_length=100)

    def __str__(self):
        return f'{self.timestamp} - {self.temperature}°C'

















