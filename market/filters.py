from django_filters.rest_framework import FilterSet
from .models import CarModel, Post

class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'type' : ['exact'],
            'carmodel__model' : ['exact'],
            'carmodel__make' : ['exact'],
            'color' : ['exact'],
            'location' : ['exact'],
            'fuel_type' : ['exact'],
            'body_type' : ['exact'],
            'transmission' : ['exact'],
            'price' : ['lt', 'gt'],
            'mileage' : ['lt', 'gt'],
            'displacement' : ['lt', 'gt']
        }
class CarModelFilter(FilterSet):
    class Meta:
        model = CarModel
        fields = {
            'make' : ['exact'],
        }