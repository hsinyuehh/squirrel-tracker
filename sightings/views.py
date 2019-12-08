from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
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
        form = SightingForm(request.POST)
        if form.is_valid():
            new_sighting = form.save()
            return redirect('/sightings/')
    else:
        form = SightingForm()

    return render(request, 'sightings/add.html', {'form': form.as_p()})

def sighting_details(request, squirrel_id):
    if request.method == 'POST' and 'delete' in request.POST:
        sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
        sighting.delete()
        messages.success(request, 'Successfully Delete!')
        return redirect('/sightings/')
    elif request.method == 'POST':
        sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
        form = SightingForm(request.POST, instance=sighting)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully Update!')
            return redirect(f'/sightings/{squirrel_id}/')
    elif request.method == 'GET':
        sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
        form = SightingForm(instance=sighting)
        context = {
            'form': form.as_p(),
            'sighting': sighting,
        }
        return render(request, 'sightings/edit.html', context)

def stats(request):

    black = Squirrel.objects.filter(color='Black').count()
    cinnamon = Squirrel.objects.filter(color='Cinnamon').count()
    gray = Squirrel.objects.filter(color='Gray').count()
    adult = Squirrel.objects.filter(age='Adult').count()
    juvenile = Squirrel.objects.filter(age='Juvenile').count()
    chasing = Squirrel.objects.filter(chasing=True).count()
    climbing = Squirrel.objects.filter(climbing=True).count()
    eating = Squirrel.objects.filter(eating=True).count()
    foraging = Squirrel.objects.filter(foraging=True).count()
    context = {
        'black': black,
        'cinnamon': cinnamon,
        'gray': gray,
        'adult': adult,
        'juvenile': juvenile,
        'eating': eating,
        'foraging': foraging,
        'chasing': chasing,
        'climbing': climbing,
    }
    return render(request, 'sightings/stats.html', context)


