from django.urls import path
from . import views

urlpatterns = [
        path('',views.all_sightings),
        path('stats/',views.stats),
        path('add/',views.add_sighting),
        path('<str:squirrel_id>/',views.sighting_details),

]
