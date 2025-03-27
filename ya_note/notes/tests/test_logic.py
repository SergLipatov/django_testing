from pytils.translit import slugify

from .base import BaseTestCase
from .base import (ADD_URL, SUCCESS_URL, AUTHOR_DELETE_URL, AUTHOR_EDIT_URL,
                   AUTHOR_DELETE_URL)
from notes.models import Note


class NoteCRUDTests(BaseTestCase):
    """Тесты CRUD-операций с заметками."""

    def test_author_can_create_note(self):
        """Авторизованный пользователь может создать заметку."""
        initial_ids = set(Note.objects.values_list('id', flat=True))
        response = self.author_client.post(ADD_URL, self.new_note_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_notes_queryset = Note.objects.exclude(id__in=initial_ids)
        self.assertEqual(
            new_notes_queryset.count(), 1,
        )
        new_note = new_notes_queryset.first()
        self.assertEqual(new_note.title, self.new_note_data["title"])
        self.assertEqual(new_note.text, self.new_note_data["text"])
        self.assertEqual(new_note.author, self.author)
        expected_slug = self.new_note_data["slug"]
        self.assertEqual(new_note.slug, expected_slug)

    def test_edit_note(self):
        """Автор может редактировать свою заметку."""
        initial_ids = set(Note.objects.values_list("id", flat=True))
        response = self.author_client.post(ADD_URL, self.new_note_data)
        self.assertRedirects(response, SUCCESS_URL)
        new_notes = Note.objects.exclude(id__in=initial_ids)
        self.assertEqual(new_notes.count(), 1,)
        new_note = new_notes.get()
        self.assertEqual(new_note.title, self.new_note_data["title"])
        self.assertEqual(new_note.text, self.new_note_data["text"])
        self.assertEqual(new_note.author,
                         self.author)
        self.assertEqual(new_note.slug,
                         self.new_note_data["slug"])

    def test_anonymous_cannot_create_note(self):
        """Анонимный пользователь не может создать заметку."""
        self.assertNotEqual(
            self.client.post(ADD_URL, self.new_note_data),
            200,)
        self.assertFalse(
            Note.objects.filter(title=self.new_note_data["title"]).exists(),)

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку."""
        note_id = self.note_by_author.id
        self.assertRedirects(self.author_client.post(
            AUTHOR_DELETE_URL), SUCCESS_URL)
        self.assertFalse(Note.objects.filter(id=note_id).exists(),)

    def test_user_cannot_edit_someone_elses_note(self):
        """Обычный пользователь не может редактировать чужую заметку."""
        self.assertNotEqual(
            self.reader_client.post(
                AUTHOR_EDIT_URL, {
                    **self.edit_note_data,
                    "slug": self.note_by_author.slug
                }).status_code,
            200,
        )
        unchanged_note = Note.objects.get(id=self.note_by_author.id)
        self.assertEqual(unchanged_note.title, "Заметка автора",)
        self.assertEqual(unchanged_note.text, "Текст 1",)

    def test_user_cannot_delete_someone_elses_note(self):
        """Обычный пользователь не может удалить чужую заметку."""
        note_id = self.note_by_author.id
        response = self.reader_client.post(AUTHOR_DELETE_URL)
        self.assertNotEqual(response.status_code,
                            200)
        self.assertTrue(Note.objects.filter(
            id=note_id).exists())

    def test_create_note_without_slug(self):
        """Slug формируется физ заголовка, если не передан."""
        note_data_without_slug = {**self.new_note_data}
        note_data_without_slug.pop("slug", None)  # Убираем ключ `slug`
        initial_ids = set(Note.objects.values_list("id", flat=True))
        response = self.author_client.post(ADD_URL, note_data_without_slug)
        self.assertRedirects(response, SUCCESS_URL)
        new_notes = Note.objects.exclude(id__in=initial_ids)
        self.assertEqual(new_notes.count(), 1,)
        new_note = new_notes.get()
        expected_slug = slugify(
            note_data_without_slug["title"])
        self.assertEqual(new_note.slug, expected_slug)
