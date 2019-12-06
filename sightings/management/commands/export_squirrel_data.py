from django.core.management.base import BaseCommand, CommandError
import datetime
import pandas as pd
from sightings.models import Squirrel


class Command(BaseCommand):
    help = 'Export Squirrel data to a csv file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', nargs='+', type=str, help="/path/to/file.csv")

    def handle(self, *args, **options):
        file_path = options['file_path'][0]
        df = pd.DataFrame(Squirrel.objects.all().values())
        df.replace('other', '', inplace=True)
        df['date'] = df['date'].apply(lambda x: x.strftime("%m%d%Y"))
        df.to_csv(file_path, encoding='utf-8')
        self.stdout.write(self.style.SUCCESS('Successfully export data to %s' % file_path))