import csv

from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.models import Comment

User = get_user_model()


class Command(BaseCommand):
    help = 'Загрузка данных о комменатариях из csv'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding='utf-8') as f:
            reader = csv.reader(f, dialect='excel')
            next(reader)
            for row in reader:
                Comment.objects.create(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    pub_date=row[4],
                )

# python manage.py load_csv_comment --path static/data/comments.csv
