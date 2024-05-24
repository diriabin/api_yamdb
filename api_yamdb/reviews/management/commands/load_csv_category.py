import csv

from django.core.management import BaseCommand

from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка данных о категориях из csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)
            for row in reader:
                Category.objects.create(
                    id=row[0],
                    name=row[1],
                    slug=row[2],
                )
# python manage.py load_csv_category --path static/data/category.csv
