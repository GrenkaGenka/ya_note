from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestBase(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.other_user = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )
        cls.form_data = {'title': 'aaa', 'text': 'bb'}
        Note.objects.create(
            title='Вторая заметка',
            text='Текст2',
            author=cls.other_user,
            slug='2_note'
        )

        cls.home_url = reverse('notes:home')
        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.success_url = reverse('notes:success')
        cls.add_url = reverse('notes:add')
        cls.list_url = reverse('notes:list')
        cls.detail_url = reverse('notes:detail', args=(cls.note.slug,))
