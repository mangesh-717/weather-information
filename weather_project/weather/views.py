from django.shortcuts import render
# Create your views here.
from weather.models import weatherdata
from django.db.models import Avg
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from datetime import datetime, timedelta
import requests
import copy 
def fetch_weather_data(request):
    if request.method == 'POST':
        location = request.POST['location'] #here location is taken from user to show weather information
        location2=str(copy.deepcopy(location)).upper() #here location name is convirted to upper for intigerity
        API_KEY = '' #this is my api key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()# return data in json
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']

            # inserting data in to django models
            weather_data = weatherdata.objects.create(
                temperature= temperature-273.15,
                humidity=humidity,
                wind_speed=wind_speed,
                location=location2
            )

            weather_data.save()
            print(weather_data)
            print("success")
            print(data)
            
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            weather_data = weatherdata.objects.filter(timestamp__range=[start_date, end_date])
        
            avg_temp = weatherdata.objects.filter(timestamp__range=[start_date, end_date]).aggregate(avg_temp=Avg('temperature'))['avg_temp']
            avg_humidity = weatherdata.objects.filter(timestamp__range=[start_date, end_date]).aggregate(avg_humidity=Avg('humidity'))['avg_humidity']
        
            timestamps = [data.timestamp for data in weather_data]
            temperatures = [data.temperature for data in weather_data]
            humidities = [data.humidity for data in weather_data]
        
            fig, ax = plt.subplots(2, 1, figsize=(10, 8))
        
            ax[0].plot(timestamps, temperatures, label='Temperature (°C)')
            ax[0].set_title(f'Temperature Trends for {location} Over Time')
            ax[0].set_xlabel('Time')
            ax[0].set_ylabel('Temperature (°C)')
            ax[0].legend()
        
            ax[1].plot(timestamps, humidities, label='Humidity (%)', color='green')
            ax[1].set_title(f'Humidity Trends for {location} Over Time')
            ax[1].set_xlabel('Time')
            ax[1].set_ylabel('Humidity (%)')
            ax[1].legend()
        
            buffer = BytesIO()
            plt.tight_layout()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
        
            graph = base64.b64encode(image_png).decode('utf-8')
        
            context = {         
                'location': location,
                'avg_temp': avg_temp,
                'avg_humidity': avg_humidity,
                'graph': graph,
            }
            return render(request, 'analyzer_weather.html', context)
        
        else:
            print("Error fetching data.")
            return None


    return render(request, 'user_data.html')

