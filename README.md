# trustyai

TrustyAI is a lightweight LLM wrapper that estimates the trustworthiness of the
LLM's answers. It can integrate with any LLM provider (Gemini, OpenAI, etc.),
given API access. The confidence score, in particular the self-reflection
certainty, of an answer is calculated based on the work of
[Chen et al., 2023](https://arxiv.org/pdf/2308.16175).

## Setup

1. Clone the repo
```bash
git clone git@github.com:kndo/trustyai.git
cd trustyai/
```

2. Create a virtual env and activate it
```bash
python3 -m venv .venv/
source .venv/bin/activate
```

3. Install the `trustyai` library
```bash
pip install -e .  # in editable mode (changes to the library code is live)
# or not
pip install .
```

4. Run the included example client script:
```bash
python client.py
```
Note that the example uses Google Gemini as the LLM provider and
`gemini-2.5-flash` for the model. Therefore, you must [obtain a Gemini API
key](https://ai.google.dev/gemini-api/docs/api-key) an set it as an environment
variable (`GEMINI_API_KEY`).

The library can be readily extended to integrate with OpenAI, Claude, etc.

5. Run tests
```bash
pytest tests/
```

## Development Process

I first read the instructions of the take-home assignment and made sure I
understood all of the requirements. Since I was asked to implement an algorithm
that's based on a research paper, I went there first to see if I could
understand it, as it would likely be the bottleneck to completing the
assignment. I read Section 3.2 and expanded outwards as necessary until I read
enough to understand the background/context of what I would be implementing.

Then, I went to the Google Gemini docs to obtain an API key, since it's free.
I asked Gemini/Claude to give me an example of a very simple/basic usage of the
Gemini API in python. After that, I didn't really need to use any LLM to
generate code; I only used it to look up documentation. Since this assignment
is quite small, I just created the project structure and code files by hand.

For the `TrustyAI` API, I aimed for simplicity and intuitiveness. To integrate
with an LLM provider, we just need to specify the provider, a model, and an API
key. Thus, those parameters should be configurable by the client. Then, we can
ask (`TrustyAI.ask()`) a question and the response (`AskResponse`) contains the
original `question`, `answer`, and `confidence_score` (which is just the
self-reflection certainty score).


## Time Spent
Overall time spent was 3 hours, because I believe in understanding the algorithm
confidently before building. I spent 1.5 hours on reading the paper thoroughly,
then 1.5 hours implementing. Any additional time was spent on polishing the repo
in order to make the best impression.
