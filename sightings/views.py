from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages

from .models import Squirrel
from .forms import SightingForm
from datetime import date, datetime
import json
import pandas as pd
import numpy as np

def all_sightings(request):
    sightings = Squirrel.objects.all()
    context = {
        'sightings': sightings,
    }
    return render(request, 'sightings/all.html', context)

def sighting_map(request):
    sightings = Squirrel.objects.all()
    context = {
        'sightings': sightings,
    }
    return render(request, 'sightings/map.html', context)

def add_sighting(request):
    if request.method == 'POST':
        form = SquirrelForm(request.POST)
        if form.is_valid():
            new_sighting = form.save()
            return redirect('/sightings/')
    else:
        form = SquirrelForm()

    return render(request, 'sightings/add.html', {'form': form.as_p()})

def sighting_details(request, squirrel_id):
    if request.method == 'POST' and 'delete' in request.POST:
        sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
        sighting.delete()
        messages.success(request, 'Successfully Delete!')
        return redirect('/sightings/')
    elif request.method == 'POST':
        sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
        form = SquirrelForm(request.POST, instance=sighting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Update!')
            return redirect(f'/sightings/{squirrel_id}/')
    elif request.method == 'GET':
        sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
        form = SquirrelForm(instance=sighting)
        context = {
            'form': form.as_p(),
            'sighting': sighting,
        }
        return render(request, 'sightings/edit.html', context)




