import csv

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузка данных о пользователях из csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)  # Пропустить первую строку (заголовок)
            for row in reader:
                User.objects.create(
                    id=row[0],
                    username=row[1],
                    email=row[2],
                    role=row[3],
                    bio=row[4],
                    first_name=row[5],
                    last_name=row[6]
                )
# python manage.py load_csv_users --path static/data/users.csv
