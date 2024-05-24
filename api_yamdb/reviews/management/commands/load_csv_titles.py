import csv

from django.core.management import BaseCommand

from reviews.models import Title, Category


class Command(BaseCommand):
    help = 'Загрузка данных о названиях из csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)
            for row in reader:
                Title.objects.create(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category.objects.get(id=row[3]),
                )

# python manage.py load_csv_titles --path static/data/titles.csv
