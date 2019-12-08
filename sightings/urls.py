from django.urls import path
from . import views

urlpatterns = [
        path('',views.all_sightings),
        path('add/',views.add_sighting),
        path('<str:squirrel_id>/',views.sighting_details),
        path('stats/',views.stats),
]
