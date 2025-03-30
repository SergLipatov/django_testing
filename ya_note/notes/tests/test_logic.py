from http import HTTPStatus

from pytils.translit import slugify

from .base import BaseTestCase, REDIRECT_ADD_URL
from .base import (ADD_URL, SUCCESS_URL, AUTHOR_EDIT_URL,
                   AUTHOR_DELETE_URL)
from notes.models import Note


class NoteCRUDTests(BaseTestCase):
    """Тесты CRUD-операций с заметками."""

    def test_author_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        initial_ids = set(Note.objects.values_list("id", flat=True))
        response = self.author_client.post(ADD_URL, self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_notes_queryset = Note.objects.exclude(id__in=initial_ids)
        self.assertEqual(
            new_notes_queryset.count(), 1,
        )
        new_note = new_notes_queryset.first()
        self.assertEqual(new_note.title, self.form_data["title"])
        self.assertEqual(new_note.text, self.form_data["text"])
        self.assertEqual(new_note.author, self.author)
        self.assertEqual(new_note.slug, self.form_data["slug"])

    def test_author_can_edit_note(self):
        """Автор может редактировать свою заметку."""
        response = self.author_client.post(AUTHOR_EDIT_URL, self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        updated_note = Note.objects.get(pk=self.note_by_author.pk)
        self.assertEqual(updated_note.title, self.form_data["title"])
        self.assertEqual(updated_note.text, self.form_data["text"])
        self.assertEqual(updated_note.author, self.note_by_author.author)
        self.assertEqual(updated_note.slug, self.form_data["slug"])

    def test_anonym_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        initial_ids = set(Note.objects.values_list("id", flat=True))
        response = self.client.post(ADD_URL, self.form_data)
        self.assertRedirects(response, REDIRECT_ADD_URL)
        self.assertEqual(set(
            Note.objects.values_list("id", flat=True)), initial_ids)

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        initial_count = Note.objects.count()
        response = self.author_client.post(AUTHOR_DELETE_URL)
        self.assertRedirects(response, SUCCESS_URL)
        self.assertEqual(Note.objects.count(), initial_count - 1)
        self.assertFalse(Note.objects.filter(
            id=self.note_by_author.id).exists())

    def test_user_cannot_edit_someone_elses_note(self):
        """Обычный пользователь не может редактировать чужую заметку."""
        response = self.reader_client.post(AUTHOR_EDIT_URL, self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        unchanged_note = Note.objects.get(pk=self.note_by_author.pk)
        self.assertEqual(unchanged_note.title, self.note_by_author.title)
        self.assertEqual(unchanged_note.text, self.note_by_author.text)
        self.assertEqual(unchanged_note.slug, self.note_by_author.slug)
        self.assertEqual(unchanged_note.author, self.note_by_author.author)

    def test_user_cannot_delete_someone_elses_note(self):
        """Обычный пользователь не может удалить чужую заметку."""
        response = self.reader_client.post(AUTHOR_EDIT_URL, self.form_data)
        self.assertNotEqual(response.status_code, HTTPStatus.OK)
        unchanged_note = Note.objects.get(pk=self.note_by_author.pk)
        self.assertEqual(unchanged_note.title, self.note_by_author.title)
        self.assertEqual(unchanged_note.text, self.note_by_author.text)
        self.assertEqual(unchanged_note.slug, self.note_by_author.slug)
        self.assertEqual(unchanged_note.author, self.note_by_author.author)

    def test_create_note_without_slug(self):
        """Slug формируется из заголовка, если не передан."""
        self.form_data.pop("slug", None)
        initial_ids = set(Note.objects.values_list("id", flat=True))
        response = self.author_client.post(ADD_URL, self.form_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_notes = Note.objects.exclude(id__in=initial_ids)
        self.assertEqual(new_notes.count(), 1,)
        new_note = new_notes.get()
        self.assertEqual(new_note.slug, slugify(self.form_data["title"]))
        self.assertEqual(new_note.title, self.form_data["title"])
        self.assertEqual(new_note.text, self.form_data["text"])
        self.assertEqual(new_note.author, self.note_by_author.author)
