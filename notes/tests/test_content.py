from http import HTTPStatus

from django.contrib.auth import get_user_model

from notes.forms import NoteForm
from notes.tests.conftest import TestBase


User = get_user_model()


class TestHomePage(TestBase):

    def test_note_object(self):

        url = self.list_url
        response = self.author_client.get(url)
        note_list = response.context['object_list']
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note, note_list)

    def test_only_autor_list(self):

        url = self.list_url
        response = self.reader_client.get(url)
        note_list = response.context['object_list']
        self.assertNotIn(self.note, note_list)

    def test_client_has_edit_form(self):

        url = self.edit_url
        response = self.author_client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)

    def test_client_has_add_form(self):

        url = self.add_url
        response = self.author_client.get(url)
        self.assertIn('form', response.context)
        self.assertIsInstance(response.context['form'], NoteForm)
