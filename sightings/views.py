from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib import messages
import json
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
    sightings = Squirrel.objects.all()[:100]
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

def edit_sighting(request, squirrel_id):
    sighting = Squirrel.objects.get(squirrel_id=squirrel_id)
    if request.method == 'POST':
        form = SightingForm(request.POST, instance=sighting)
        # check data with form
        if form.is_valid():
            form.save()
            messages.success(request, 'This sighting has been successfully updated!')
            return HttpResponseRedirect(f'/sightings/{squirrel_id}/')
    else:
        form = SightingForm(instance=sighting)
        context = {
            'form': form.as_p(),
            'sighting': sighting,
        }
        return render(request, 'sightings/edit.html', context)


def age_color(df):
    ages = ['Adult', 'Juvenile']
    age_color = pd.DataFrame(df.groupby(['age', 'fur_color'])['id'].count()).reset_index()
    black = list()
    cinnamon = list()
    gray = list()

    for age in ages:
        black.append(int(age_color[(age_color['fur_color']=='Black') & (age_color['age']==age)]['id'].iloc[0]))
        cinnamon.append(int(age_color[(age_color['fur_color']=='Cinnamon') & (age_color['age']==age)]['id'].iloc[0]))
        gray.append(int(age_color[(age_color['fur_color']=='Gray') & (age_color['age']==age)]['id'].iloc[0]))

    column_chart = {
            'chart': {
                'type': 'column'
            },
            'title': {
                'text': 'Age vs Primary Fur Color'
            },
            'xAxis': {
                'categories': ages
            },
            'yAxis': {
                'min': 0,
                'title': {
                    'text': 'Count'
                },
                'stackLabels': {
                    'enabled': True,
                    'style': {
                        'fontWeight': 'bold',
                        'color': "( // theme\
                            Highcharts.defaultOptions.title.style &&\
                            Highcharts.defaultOptions.title.style.color\
                        ) || 'gray'"
                    }
                }
            },
            'legend': {
                'align': 'right',
                'x': 10,
                'verticalAlign': 'top',
                'y': 30,
                'floating': True,
                'backgroundColor': "#ffffff",
                'borderColor': '#CCC',
                'borderWidth': 1,
                'shadow': False
            },
            'tooltip': {
                'headerFormat': '<b>{point.x}</b><br/>',
                'pointFormat': '{series.name}: {point.y}<br/>Total: {point.stackTotal}'
            },
            'plotOptions': {
                'column': {
                    'stacking': 'normal',
                    'dataLabels': {
                        'enabled': True
                    }
                }
            },
            'series': [{
                'name': 'Black',
                'data': black,

            }, {
                'name': 'Cinnamon',
                'data': cinnamon
            }, {
                'name': 'Gray',
                'data': gray
            }]
        }

    return json.dumps(column_chart)

def behavior_change(df):
    date_running = df.groupby(['date', 'running'])['id'].count().reset_index()
    date_chasing = df.groupby(['date', 'chasing'])['id'].count().reset_index()
    date_climbing = df.groupby(['date', 'climbing'])['id'].count().reset_index()
    date_eating = df.groupby(['date', 'eating'])['id'].count().reset_index()
    date_foraging = df.groupby(['date', 'foraging'])['id'].count().reset_index()

    datelist = list(set(date_running['date']) & set(date_chasing['date']) & set(date_climbing['date']) & set(date_eating['date']) & set(date_foraging['date']))
    datelist.sort()
    run = list()
    chase = list()
    climb = list()
    eat = list()
    forage = list()

    for i in datelist:
        run.append(int(date_running[(date_running['date'] == i) & (date_running['running'] == True)]['id'].iloc[0]))
        chase.append(int(date_chasing[(date_chasing['date'] == i) & (date_chasing['chasing'] == True)]['id'].iloc[0]))
        climb.append(int(date_climbing[(date_climbing['date'] == i) & (date_climbing['climbing'] == True)]['id'].iloc[0]))
        eat.append(int(date_eating[(date_eating['date'] == i) & (date_eating['eating'] == True)]['id'].iloc[0]))
        forage.append(int(date_foraging[(date_foraging['date'] == i) & (date_foraging['foraging'] == True)]['id'].iloc[0]))

    datelist = [date.strftime(i, "%Y-%m-%d") for i in datelist]

    line_chart = {
        'chart': {
            'type': 'line'
        },
        'title': {
            'text': 'Time vs Number of Squirrels Behaviors'
        },
        'xAxis': {
            'categories': datelist
        },
        'yAxis': {
            'title': {
                'text': 'Count'
            }
        },
        'plotOptions': {
            'line': {
                'dataLabels': {
                    'enabled': True
                },
                'enableMouseTracking': True
            }
        },
        'series': [{
            'name': 'Running',
            'data': run
        }, {
            'name': 'Chasing',
            'data': chase
        }, {
            'name': 'Climbing',
            'data': climb
        }, {
            'name': 'Eating',
            'data': eat
        }, {
            'name': 'Foraging',
            'data': forage
        }]
    }

    return json.dumps(line_chart)


def stats(request):
    df = pd.DataFrame(Squirrel.objects.all().values())

    black = Squirrel.objects.filter(fur_color='Black').count()
    cinnamon = Squirrel.objects.filter(fur_color='Cinnamon').count()
    gray = Squirrel.objects.filter(fur_color='Gray').count()
    ground_plane = Squirrel.objects.filter(location='Ground Plane').count()
    above_ground = Squirrel.objects.filter(location='Above Ground').count()
    column_chart = age_color(df)
    line_chart = behavior_change(df)
    context = {
        'black': black,
        'cinnamon': cinnamon,
        'gray': gray,
        'ground_plane': ground_plane,
        'above_ground': above_ground,
        'column_chart': column_chart,
        'line_chart': line_chart,
    }
    return render(request, 'sightings/stats.html', context)
