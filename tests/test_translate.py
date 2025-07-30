from unittest.mock import patch

import pytest
from openai import OpenAI

from app.translate_app import openai_api_key, translate_with_openai


@pytest.mark.parametrize(
    "text, src, tgt, expected",
    [
        ("Hello", "English", "French", "Bonjour"),
        (
            "Wie ist das Wetter?",
            "German",
            "English",
            "What is the weather like?",
        ),
        ("Wie geht's?", "German", "English", "How's it going?"),
        (
            "Come stai oggi?",
            "Italian",
            "French",
            "Comment vas-tu aujourd'hui?",
        ),
    ],
)
def test_translate_with_openai_mock(text, src, tgt, expected):
    client = OpenAI(api_key=openai_api_key)
    with patch(
        "app.translate_app.client.chat.completions.create"
    ) as mock_create:
        mock_create.return_value.choices = [
            type(
                "obj",
                (object,),
                {"message": type("obj", (object,), {"content": expected})()},
            )()
        ]
        result = translate_with_openai(client, text, src, tgt)
        assert result == expected
