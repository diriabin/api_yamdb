from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = 'Загрузка данных из всех CSV файлов'

    def handle(self, *args, **kwargs):
        commands = [
            ('load_csv_users', 'static/data/users.csv'),
            ('load_csv_category', 'static/data/category.csv'),
            ('load_csv_genre', 'static/data/genre.csv'),
            ('load_csv_titles', 'static/data/titles.csv'),
            ('load_csv_review', 'static/data/review.csv'),
            ('load_csv_comment', 'static/data/comments.csv'),
        ]

        for command, path in commands:
            call_command(command, path=path)

# python manage.py load_csv_all
