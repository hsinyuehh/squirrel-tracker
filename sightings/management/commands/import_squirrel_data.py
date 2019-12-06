import csv
from django.core.management.base import BaseCommand
from sightings.models import Squirrel
import datetime


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('csv_file')

    def booler(self, b):
        if b.lower() == 'true':
            return True
        else:
            return False

    def handle(self, *args, **options):
        with open(options['csv_file']) as fp:
            reader = csv.DictReader(fp)
            data = list(reader)
        for item in data:
            if item['Shift'] == 'AM':
                shift_ = Squirrel.AM
            else:
                shift_ = Squirrel.PM
            if item['Age'] == 'Adult':
                age_ = Squirrel.ADULT
            elif item['Age'] == 'Juvenile':
                age_ = Squirrel.JUVENILE
            else:
                age_ = Squirrel.UNKNOWN

            if item['Primary Fur Color'] == 'Gray':
                color_ = Squirrel.GRAY
            elif item['Primary Fur Color'] == 'Cinnamon':
                color_ = Squirrel.CINNAMON
            elif item['Primary Fur Color'] == 'Black':
                color_ = Squirrel.BLACK
            else:
                color_ = Squirrel.UNKNOWN
            if item['Location'] == 'Ground Plane':
                location_ = Squirrel.GROUND_PLANE
            elif item['Location'] == 'Above Ground':
                location_ = Squirrel.ABOVE_GROUND
            else:
                location_ = Squirrel.UNKNOWN

            p = Squirrel(
                latitude=float(item['X']),
                longitude=float(item['Y']),
                squirrel_id=item['Unique Squirrel ID'],
                shift=shift_,
                date=datetime.date(int(item['Date'][-4:]), int(item['Date'][:2]), int(item['Date'][2:4])),
                age=age_,
                fur_color=color_,
                location=location_,
                specific_location=item['Specific Location'],
                running=self.booler(item['Running']),
                chasing=self.booler(item['Chasing']),
                climbing=self.booler(item['Climbing']),
                eating=self.booler(item['Eating']),
                foraging=self.booler(item['Foraging']),
                other_activities=item['Other Activities'],
                kuks=self.booler(item['Kuks']),
                quaas=self.booler(item['Quaas']),
                moans=self.booler(item['Moans']),
                tail_flags=self.booler(item['Tail flags']),
                tail_twitches=self.booler(item['Tail twitches']),
                approaches=self.booler(item['Approaches']),
                indifferent=self.booler(item['Indifferent']),
                runs_from=self.booler(item['Runs from']),
            )
            p.save()