from django.conf import settings
from django.test import TestCase
# Импортируем функцию reverse(), она понадобится для получения адреса страницы.
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from datetime import datetime, timedelta

from notes.models import Note
from notes.forms import NoteForm


User = get_user_model()


class TestHomePage(TestCase):

    LIST_URL = reverse('notes:list')
    NOTE_COUNT = 10

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        all_news = []
        for index in range(cls.NOTE_COUNT):
            news = Note(
                title=f'note {index}',
                text='Просто текст.',
                slug=index,
                author=cls.author,
            )
            all_news.append(news)
        Note.objects.bulk_create(all_news)

    def test_news_count(self):
        self.client.force_login(self.author)
        # Загружаем главную страницу.
        response = self.client.get(self.LIST_URL)
        # Код ответа не проверяем, его уже проверили в тестах маршрутов.
        # Получаем список объектов из словаря контекста.
        object_list = response.context['object_list']
        # Определяем количество записей в списке.
        note_count = object_list.count()
        # Проверяем, что на странице именно 10 новостей.
        self.assertEqual(note_count, self.NOTE_COUNT) 
