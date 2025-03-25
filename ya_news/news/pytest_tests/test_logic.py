import pytest
from http import HTTPStatus

from news.models import Comment
from news.forms import WARNING, BAD_WORDS

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("bad_word", BAD_WORDS)
def test_prohibited_words_in_comment(author_client, detail_url, bad_word):
    """Проверяем, что тест на запрещённые слова работает корректно."""
    data = {"text": f"Это {bad_word}!"}
    response = author_client.post(detail_url, data=data)
    assert Comment.objects.count() == 0
    assert WARNING in response.context["form"].errors["text"]


def test_user_can_edit_own_comment(author_client, comment, edit_url):
    """Авторизованный пользователь может редактировать свои комментарии."""
    updated_data = {"text": "Обновленный комментарий"}
    response = author_client.post(edit_url, data=updated_data)
    edited_comment = Comment.objects.get(pk=comment.pk)

    assert edited_comment.text == updated_data["text"]
    assert edited_comment.author == comment.author
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_edit_others_comment(another_author_client, comment,
                                         edit_url):
    """Пользователь не может редактировать чужие комментарии."""
    updated_data = {"text": "Новый несанкционированный текст"}
    response = another_author_client.post(edit_url, data=updated_data)

    unchanged_comment = Comment.objects.get(pk=comment.pk)
    assert unchanged_comment.text != updated_data["text"]
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_can_delete_own_comment(author_client, comment, delete_url):
    """Авторизованный пользователь может удалить свой комментарий."""
    response = author_client.post(delete_url)
    assert Comment.objects.filter(pk=comment.pk).count() == 0
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_delete_others_comment(another_author_client, comment,
                                           delete_url):
    """Авторизованный пользователь не может удалить чужой комментарий."""
    response = another_author_client.post(delete_url)

    assert Comment.objects.filter(pk=comment.pk).count() == 1
    assert response.status_code == HTTPStatus.NOT_FOUND
