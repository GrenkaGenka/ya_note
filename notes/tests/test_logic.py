from http import HTTPStatus
from pytils.translit import slugify

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user = User.objects.create(username='Мимо Крокодил')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.url = reverse('notes:add')
        cls.form_data = {'title': 'aaa', 'text': 'bb'}

    def test_anonymous_user_cant_create_note(self):

        self.client.post(self.url, data=self.form_data)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_can_create_note(self):

        self.auth_client.force_login(self.user)
        self.auth_client.post(self.url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.user)

    def test_cant_create_2_note_same_slug(self):

        data = {'title': 'aaa', 'text': 'bb', 'slug': 'ee'}
        self.auth_client.force_login(self.user)
        self.auth_client.post(self.url, data=data)
        self.auth_client.post(self.url, data=data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_unicue_slug(self):

        self.auth_client.force_login(self.user)
        self.auth_client.post(self.url, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.slug, slugify(note.title)[:100])


class TestNoteEditDelete(TestCase):

    FORM_DATA = {'title': 'aaa', 'text': 'bb'}

    @classmethod
    def setUpTestData(cls):

        cls.author = User.objects.create(username='Автор')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader = User.objects.create(username='Читатель')
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
            slug='one_note'
        )

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))
        cls.note_url = reverse('notes:detail', args=(cls.note.slug,))

    def test_author_can_delete_comment(self):

        response = self.author_client.delete(self.delete_url)
        url = reverse('notes:success')
        self.assertRedirects(response, url)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 0)

    def test_user_cant_delete_note_of_another_user(self):

        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        comments_count = Note.objects.count()
        self.assertEqual(comments_count, 1)

    def test_author_can_edit_note(self):

        self.author_client.post(self.edit_url, data=self.FORM_DATA)
        self.note.refresh_from_db()
        note = Note.objects.get()
        self.assertEqual(self.note.text, note.text)

    def test_user_cant_edit_comment_of_another_user(self):

        response = self.reader_client.post(self.edit_url, data=self.FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        note = Note.objects.get()
        self.assertEqual(self.note.text, note.text)
