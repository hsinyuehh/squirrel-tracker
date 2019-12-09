from django.urls import path
from . import views

urlpatterns = [
        path('stats/', views.stats),
        path('',views.all_sightings),
        path('add/',views.add_sighting),
        path('<str:squirrel_id>/',views.edit_sighting),
]
