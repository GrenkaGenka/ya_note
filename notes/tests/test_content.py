from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.models import Note


User = get_user_model()


class TestHomePage(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.other_user = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='one_note'
        )

    def test_note_object(self):
        self.client.force_login(self.author)
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note, object_list)

    def test_only_autor_list(self):
        self.client.force_login(self.other_user)
        new_note = Note.objects.create(
            title='Вторая заметка',
            text='Текст2',
            author=self.other_user,
            slug='2_note'
        )
        url = reverse('notes:list')
        response = self.client.get(url)
        object_list_count = response.context['object_list'].count()
        self.assertEqual(object_list_count, 1)

    def test_client_has_delete_form(self):

        self.client.force_login(self.author)
        url = reverse('notes:delete', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'notes/delete.html')

    def test_client_has_add_form(self):

        self.client.force_login(self.author)
        url = reverse('notes:add')
        response = self.client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
