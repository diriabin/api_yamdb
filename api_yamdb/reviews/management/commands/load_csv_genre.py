import csv

from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    help = 'Загрузка данных о жанрах из csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)
            for row in reader:
                Genre.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )

# python manage.py load_csv_genre --path static/data/genre.csv
