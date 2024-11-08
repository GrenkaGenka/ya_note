from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()

class TestNoteCreation(TestCase):
    # Текст комментария понадобится в нескольких местах кода, 
    # поэтому запишем его в атрибуты класса.
    NOTE_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls):
        # Адрес страницы с новостью.
        
        # Создаём пользователя и клиент, логинимся в клиенте.
        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.user,
            slug='one_note'
        )
        cls.url = reverse('notes:detail', args=(cls.note.slug,))
        # Данные для POST-запроса при создании комментария.
        cls.form_data = {'text': 'qqq', 'title':'q', 'slug':'q'}
        


    def test_anonymous_user_cant_create_comment(self):
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария.     
        self.client.post(self.url, data=self.form_data)
        # Считаем количество комментариев.
        comments_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(comments_count, 1)


    def test_user_can_create_comment(self):
        # Совершаем запрос от анонимного клиента, в POST-запросе отправляем
        # предварительно подготовленные данные формы с текстом комментария. 
        self.client.force_login(self.user)   
        self.client.post(self.url, data=self.form_data)
        self.note = Note.objects.create(
            title='Заголовок2',
            text='Текст2',
            author=self.user,
            slug='one_note2'
        )
        # Считаем количество комментариев.
        comments_count = Note.objects.count()
        # Ожидаем, что комментариев в базе нет - сравниваем с нулём.
        self.assertEqual(comments_count, 2)