from http import HTTPStatus

from django.contrib.auth import get_user_model
from pytils.translit import slugify

from notes.models import Note
from notes.tests.conftest import TestBase


User = get_user_model()


class TestNoteCreation(TestBase):

    def test_anonymous_user_cant_create_note(self):

        comments_count = Note.objects.count()
        self.client.post(self.add_url, data=self.form_data)
        self.assertEqual(comments_count, Note.objects.count())

    def test_user_can_create_note(self):

        note_count = Note.objects.count()
        self.auth_client.post(self.add_url, data=self.form_data)
        self.assertEqual(Note.objects.count(), note_count + 1)
        created_note = Note.objects.latest('id')
        note = Note.objects.get(id=created_note.id)
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.author, self.user)

    def test_cant_create_2_note_same_slug(self):

        data = {'title': 'aaa', 'text': 'bb', 'slug': 'ee'}
        note_count = Note.objects.count()
        self.auth_client.post(self.add_url, data=data)
        self.auth_client.post(self.add_url, data=data)
        self.assertEqual(Note.objects.count(), note_count + 1)

    def test_unicue_slug(self):

        note_count = Note.objects.count()
        self.auth_client.post(self.add_url, data=self.form_data)
        self.assertEqual(Note.objects.count(), note_count + 1)
        # note = Note.objects.get()
        self.note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note_from_db.slug,
                         slugify(self.note_from_db.slug))


class TestNoteEditDelete(TestBase):

    FORM_DATA = {'title': 'aaa', 'text': 'bb'}

    def test_author_can_delete_comment(self):

        comments_count = Note.objects.count()
        response = self.author_client.delete(self.delete_url)
        url = self.success_url
        self.assertRedirects(response, url)
        self.assertEqual(Note.objects.count(), comments_count - 1)

    def test_user_cant_delete_note_of_another_user(self):
        comments_count = Note.objects.count()
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), comments_count)

    def test_author_can_edit_note(self):

        self.author_client.post(self.edit_url, data=self.FORM_DATA)
        self.note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note_from_db.title, self.FORM_DATA['title'])
        self.assertEqual(self.note_from_db.text, self.FORM_DATA['text'])
        self.assertEqual(self.note_from_db.author, self.author)

    def test_user_cant_edit_comment_of_another_user(self):
        self.note_before_cange = Note.objects.get(id=self.note.id)
        response = self.reader_client.post(self.edit_url, data=self.FORM_DATA)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note_before_cange.text, self.note_from_db.text)
        self.assertEqual(self.note_before_cange.title, self.note_from_db.title)
        self.assertEqual(self.note_before_cange.author,
                         self.note_from_db.author)
