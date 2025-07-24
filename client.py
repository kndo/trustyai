import os
from trustyai import TrustyAI

tai = TrustyAI(
    provider="gemini",
    model="gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"]
)

# response = tai.ask("what is 1+1?")
response = tai.ask("what color background are the stars in the syrian flag on?")
print(response.self_reflection_certainty)
# response = tai.ask("what is the date today?")
# response = tai.ask("what the color of the sky at 5:30pm in Seattle today?")
# response = tai.ask("what is the third month in alphabetical order?")
