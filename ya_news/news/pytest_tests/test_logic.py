from http import HTTPStatus

import pytest

from news.forms import WARNING, BAD_WORDS
from news.models import Comment

pytestmark = pytest.mark.django_db

UPDATED_COMMENT = {"text": "Обновленный комментарий"}
UPDATED_UNAUTHORIZED_COMMENT = {"text": "Новый несанкционированный текст"}
COMMENT_DATA = [
    {"bad_word": bad_word, "data": {
        "text": f"Это {bad_word}!"}} for bad_word in BAD_WORDS
]


@pytest.mark.parametrize("comment_info", COMMENT_DATA)
def test_prohibited_words_in_comment(author_client, detail_url, comment_info):
    """Проверяем, что тест на запрещённые слова работает корректно."""
    response = author_client.post(detail_url, data=comment_info["data"])
    assert Comment.objects.count() == 0
    assert WARNING in response.context["form"].errors["text"]


def test_user_can_edit_own_comment(author_client, comment, edit_url):
    """Авторизованный пользователь может редактировать свои комментарии."""
    response = author_client.post(edit_url, data=UPDATED_COMMENT)
    edited_comment = Comment.objects.get(pk=comment.pk)

    assert edited_comment.text == UPDATED_COMMENT["text"]
    assert edited_comment.author == comment.author
    assert edited_comment.created == comment.created
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_edit_others_comment(another_author_client, comment,
                                         edit_url):
    """Пользователь не может редактировать чужие комментарии."""
    response = another_author_client.post(
        edit_url,
        data=UPDATED_UNAUTHORIZED_COMMENT
    )
    unchanged_comment = Comment.objects.get(pk=comment.pk)
    assert unchanged_comment.text == comment.text
    assert unchanged_comment.author == comment.author
    assert unchanged_comment.created == comment.created
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

    unchanged_comment = Comment.objects.get(pk=comment.pk)
    assert unchanged_comment.text == comment.text
    assert unchanged_comment.author == comment.author
    assert unchanged_comment.created == comment.created
    assert response.status_code == HTTPStatus.NOT_FOUND
