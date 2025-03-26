from django.utils.text import slugify

from .base import BaseTestCase
from .urls import ADD_URL, SUCCESS_URL
from notes.models import Note


class NoteCRUDTests(BaseTestCase):
    """Тесты CRUD-операций с заметками."""

    def test_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        initial_ids = set(Note.objects.values_list('id', flat=True))

        response = self.author_client.post(ADD_URL, self.new_note_data)
        self.assertRedirects(response, SUCCESS_URL)

        new_notes_queryset = Note.objects.exclude(id__in=initial_ids)

        self.assertEqual(
            new_notes_queryset.count(), 1,
            "Должна быть создана ровно одна новая заметка"
        )

        new_note = new_notes_queryset.first()

        self.assertEqual(new_note.title, self.new_note_data["title"])
        self.assertEqual(new_note.text, self.new_note_data["text"])
        self.assertEqual(new_note.author, self.author)

        expected_slug = self.new_note_data.get("slug", slugify(
            self.new_note_data["title"]))
        self.assertEqual(new_note.slug, expected_slug)

    def test_edit_note(self):
        """Автор может редактировать свою заметку."""
        edit_data = {
            **self.edit_note_data,
            "slug": self.author_note.slug,
        }

        response = self.author_client.post(self.author_edit_url, edit_data)
        self.assertRedirects(response, SUCCESS_URL)

        edited_note = Note.objects.get(id=self.author_note.id)
        self.assertEqual(edited_note.title, self.edit_note_data["title"])
        self.assertEqual(edited_note.text, self.edit_note_data["text"])
        self.assertEqual(edited_note.slug, self.author_note.slug)
