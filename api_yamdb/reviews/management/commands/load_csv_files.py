import csv
import os

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from api_yamdb.settings import CSV_FILES_DIR
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    TitleGenre,
    User,
)


FILE_NAMES_CLASSES = {
    'users.csv': User,
    'category.csv': Category,
    'genre.csv': Genre,
    'titles.csv': Title,
    'genre_title.csv': TitleGenre,
    'review.csv': Review,
    'comments.csv': Comment,
}
FIELDS = {
    'category': (Category, 'category'),
    'genre_id': (Genre, 'genre'),
    'title_id': (Title, 'title'),
    'author': (User, 'author'),
    'review_id': (Review, 'review'),
}


def open_csv_file(file_name):
    csv_path = os.path.join(CSV_FILES_DIR, file_name)
    try:
        with open(csv_path, encoding='utf-8') as file:
            return tuple(csv.reader(file))
    except FileNotFoundError:
        print(f'Файл {file_name} не найден.')


def get_object_data(fields, data):
    object_data = dict(zip(fields, data))
    for field in tuple(object_data.keys()):
        if field in FIELDS:
            new_field = FIELDS[field][1]
            object_data[new_field] = object_data.pop(field)
            object_data[new_field] = FIELDS[field][0].objects.get(
                id=object_data[new_field]
            )
    return object_data


class Command(BaseCommand):
    help = 'Load csv files to database'

    def handle(self, *args, **options):
        for file_name, class_ in FILE_NAMES_CLASSES.items():
            print(f'Заполнение модели {class_.__name__}')
            fields, *data = open_csv_file(file_name)
            try:
                for row in data:
                    object_data = get_object_data(fields, row)
                    class_.objects.create(**object_data)
                print(f'Модель {class_.__name__} заполнена успешно')
            except (ValueError, IntegrityError, TypeError) as error:
                print(
                    f'Ошибка при заполнении {class_.__name__}: {error}.'
                    f'\nНеверные данные: {row}.'
                )
