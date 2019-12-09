from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from django.contrib import messages
import json
from .models import Squirrel
from .forms import SightingForm
from datetime import date, datetime
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

## column_chart
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

## line_chart
def behavior_change(df):
    ## foraging number
    df = df[df['foraging'] == True]
    f = df.groupby('date').count()
    ## Running number
    df = df[df['running'] == True]
    r = df.groupby('date').count()

    list_=list(f.index)
    datelist = [date.strftime(i, "%Y-%m-%d") for i in list_]
    foraging_num=[str(i) for i in list(f['foraging'].values)]
    running_num=[str(i) for i in list(r['running'].values)]

    line_chart = {
        'chart': {
            'type': 'line'
        },
        'title': {
            'text': 'Time vs The number of Foraging and Running squirrels'
        },
        'xAxis': {
            'time': datelist
        },
        'yAxis': {
            'title': {
                'text': 'Number of Squirrels'
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
            'name': 'Foraging',
            'data': foraging_num
        }, {
            'name': 'Running',
            'data': running_num
        }]
    }

    return json.dumps(line_chart)


def stats(request):
    df = pd.DataFrame(Squirrel.objects.all().values())

    black = Squirrel.objects.filter(fur_color='Black').count()
    cinnamon = Squirrel.objects.filter(fur_color='Cinnamon').count()
    gray = Squirrel.objects.filter(fur_color='Gray').count()
    adult = Squirrel.objects.filter(age='Adult').count()
    juvenile = Squirrel.objects.filter(age='Juvenile').count()
    chasing = Squirrel.objects.filter(chasing=True).count()
    climbing = Squirrel.objects.filter(climbing=True).count()
    eating = Squirrel.objects.filter(eating=True).count()
    foraging = Squirrel.objects.filter(foraging=True).count()
    column_chart = age_color(df)
    line_chart = behavior_change(df)
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
        'column_chart': column_chart,
        'line_chart': line_chart,
    }
    return render(request, 'sightings/stats.html', context)



