import pytest

from trustyai import TrustyAI


def test_unsupported_llm_provider():
    with pytest.raises(ValueError) as exc_info:
        tai = TrustyAI(
            provider="openai",
            model="gpt-4o",
            api_key="whatever",
        )

    assert str(exc_info.value) == "Unsupported provider: openai. Supported providers include: gemini"


def test_unsupported_gemini_model():
    with pytest.raises(ValueError) as exc_info:
        tai = TrustyAI(
            provider="gemini",
            model="gpt-4o",
            api_key="whatever",
        )

    assert (
        str(exc_info.value) == "Unsupported model: gpt-4o. Supported models include: gemini-2.5-pro, gemini-2.5-flash"
    )


# TODO: Write more tests
