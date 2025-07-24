"""
This file shows how a client can use TrustyAI to ask questions to an LLM like
Google Gemini, get the answer and a confidence score for the answer, and
perform some logic based on that confidence score.
"""

import os

from trustyai import TrustyAI

tai = TrustyAI(
    provider="gemini",
    model="gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"],
)

questions = [
    "what is 1+1?",
    "what color background are the stars in the syrian flag on?",  # sometimes confidence score is 0.0
    "what is the third month in alphabetical order?",
    "what is larger, 1.11 or 1.9?",
]
for question in questions:
    response = tai.ask(question)
    print("question:", response.question)
    print("answer:", response.answer)
    print("confidence score:", response.confidence_score)
    if response.confidence_score < 0.5:
        print("Not a trustworthy answer!")
    else:
        print("No reason to doubt the answer!")
