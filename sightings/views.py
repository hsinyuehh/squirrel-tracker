import pandas as pd
import numpy as np
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Squirrel
# Create your views here.



def stats(request):
    df=pd.DataFrame(Squirrel.objects.all().values())
    temp = df['fur_color'].value_counts().values

    return HttpResponse(f'The number of squirrels with different fur colors:<br>\
     Gray: {temp[0]}; Cinnamon: {temp[1]}; Black: {temp[2]}; unknown: {temp[3]}')
