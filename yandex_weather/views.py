from .models import Weather
from .serializers import WeatherSerializer

from rest_framework.response import Response
from rest_framework.views import APIView


class WeatherAPIView(APIView):
    def get(self, request):
        city = request.query_params.get('city')
        weather = Weather.objects.filter(city=city).first()
        serializer_class = WeatherSerializer(weather)
        return Response(serializer_class.data)
