import csv
import os

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError

from ingredients.models import Tag


class Command(BaseCommand):
    help = 'populates ingredients_tag table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model_name = Tag

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='filename for csv file')

    def get_current_app_path(self):
        return apps.get_app_config('ingredients').path

    def get_csv_file(self, filename):
        app_path = self.get_current_app_path()
        # file_path = os.path.join(app_path, 'data', filename)
        return os.path.join(app_path, 'data', filename)

    def clear_model(self):
        try:
            self.model_name.objects.all().delete()
        except Exception as e:
            raise CommandError(
                f'Error in clearing {self.model_name}: {str(e)}'
            )

    def insert_genre_to_db(self, data):
        try:
            self.model_name.objects.create(
                name=data['name'],
                color=data['color'],
                slug=data['slug'],
            )
        except Exception as e:
            raise CommandError(
                f'Error in inserting {self.model_name}: {str(e)}'
            )

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        self.stdout.write(self.style.SUCCESS(f'filename:{filename}'))
        file_path = self.get_csv_file(filename)
        line_count = 0
        try:
            with open(file_path, encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                self.clear_model()
                for row in csv_reader:
                    if row != '' and line_count >= 1:
                        data = {}
                        data['name'] = row[0]
                        data['color'] = row[1]
                        data['slug'] = row[2]
                        self.insert_genre_to_db(data)
                    line_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'{line_count} entries added to Tags'
                )
            )
        except FileNotFoundError:
            raise CommandError(f'File {file_path} does not exist')
