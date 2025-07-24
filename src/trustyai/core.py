import re

from google import genai

from .prompts import (
    SELF_REFLECTION_CERTAINTY_PROMPT_1,
    SELF_REFLECTION_CERTAINTY_PROMPT_2,
)

SUPPORTED_GEMINI_MODELS = ["gemini-2.5-pro", "gemini-2.5-flash"]
SELF_REFLECTION_CERTAINTY_SCORE = {
    "A": 1.0,
    "B": 0.0,
    "C": 0.5,
}


class TrustyAI:
    def __init__(self, *, provider: str, model: str, api_key: str) -> None:
        if provider != "gemini":
            # NOTE: Could create a specific exception, e.g. `UnsupportedLLMProvider`
            raise ValueError(f"Unsupported provider: {provider}. Supported providers include: gemini")

        if model not in SUPPORTED_GEMINI_MODELS:
            raise ValueError(
                f"Unsupported model: {model}. Supported models include: {', '.join(SUPPORTED_GEMINI_MODELS)}"
            )

        # NOTE: When more providers are supported, we only need to check if the
        # specified model is supported for the specified provider, not for all
        # providers

        self.provider = provider
        self.model = model
        self.api_key = api_key

        if provider == "gemini":
            self.client = genai.Client(api_key=api_key)

        self.SELF_REFLECTION_CERTAINTY_ANSWER_PATTERN = re.compile(r".*answer: (?P<answer>[ABC])$")

    def ask(self, question: str, calc_confidence_score: bool = True):
        if self.provider == "gemini":
            response = self.client.models.generate_content(
                model=self.model,
                contents=question,
            )
            answer = response.text

        confidence_score = None
        if calc_confidence_score:
            self_reflection_certainty = self.calc_self_reflection_certainty(question, answer)
            # For simplicity, we are taking the overall confidence score as just
            # the self-reflection certainty score. TODO: Calculate the observed
            # consistency score as well and use it to determine the overall
            # confidence score.
            confidence_score = self_reflection_certainty

        return AskResponse(question, answer, confidence_score)

    def calc_self_reflection_certainty(self, question: str, answer) -> float | None:
        """
        Calculates the self-reflection certainty score as defined by
        Chen et al., 2023.

        Ref: https://arxiv.org/pdf/2308.16175
        """
        prompt1 = SELF_REFLECTION_CERTAINTY_PROMPT_1.format(question=question, answer=answer)
        prompt2 = SELF_REFLECTION_CERTAINTY_PROMPT_2.format(question=question, answer=answer)

        prompts = [prompt1, prompt2]
        answers = []
        if self.provider == "gemini":
            for prompt in prompts:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                )
                answers.append(response.text)

        scores = []
        avg_score = None
        for ans in answers:
            matches = self.SELF_REFLECTION_CERTAINTY_ANSWER_PATTERN.search(ans)
            if not matches:
                # TODO: Can handle differently based on requirements
                break

            letter = matches.group("answer")
            scores.append(SELF_REFLECTION_CERTAINTY_SCORE[letter])

        if scores:
            avg_score = sum(scores) / len(scores)

        return avg_score


class AskResponse:
    def __init__(
        self,
        question: str,
        answer: str,
        confidence_score: float | None = None,
    ) -> None:
        self.question = question
        self.answer = answer
        self.confidence_score = confidence_score
