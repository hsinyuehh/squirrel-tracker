from django.core.management.base import BaseCommand, CommandError
from sightings.models import Squirrel
import datetime
import pandas as pd


class Command(BaseCommand):
    help = 'Export Squirrel data to a csv file'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str, help="/path/to/file.csv")

    def handle(self, *args, **options):
        path = options['path'][0]
        df = pd.DataFrame(Squirrel.objects.all().values())
        df.replace('other', '', inplace=True)
        df.drop(columns='id')
        df['date'] = df['date'].apply(lambda x: x.strftime("%m%d%Y"))
        df.to_csv(path)
        self.stdout.write(self.style.SUCCESS(f'Successfully export data to {path}'))