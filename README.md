# thinking-hats-ai: Python package implementing six thinking hats prompting

| | |
| --- | --- |
| Package | [![PyPI Latest Release](https://img.shields.io/pypi/v/thinking-hats-ai.svg)](https://pypi.org/project/thinking-hats-ai/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/thinking-hats-ai)|


## What is it?
**thinking-hats-ai** is a Python package that facilitates idea generation by following Edward de Bono's Six Thinking Hats methodology from his [Book](https://swisscovery.slsp.ch/permalink/41SLSP_NETWORK/1ufb5t2/alma991081046019705501). It enables you to generate ideas by selecting one of the six hats and lets you choose one of the implemented prompting technique to follow while generating the idea.


## Table of Contents
- [Use of Package](#use-of-package)
    - [Example script](#example-script)
    - [Hats](#hats)
    - [Prompting techniques](#prompting-techniques)
    - [Brainstorming-input](#brainstorming-input)
    - [Developer mode](#developer-mode)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Background](#background)
- [Creators](#creators)


## Use of Package
### Example script
This example uses the `CHAIN_OF_THOUGHT` [prompting techniques](#prompting-techniques) and the `BLACK` [hat](#hats) for the personality. It also uses [developer mode](#developer-mode) to log the interaction in a separate file.
```python
### Import package
from thinking_hats_ai import BrainstormingSession, Technique, Hat, BrainstormingInput

### Create session
session = BrainstormingSession('YOUR-OPENAI-API-KEY')
session.dev = True # Activate dev mode

### Define current status
brainstormingInput = BrainstormingInput(
    question = 'How could you make students come to class more often even though there are podcasts provided for each lecture?',
    ideas=[
        "Implement an interactive class participation system with incentives",
        "Extra credits or digital badges, encouraging students to attend and engage actively",
        "Offer exclusive in-class activities or discussions that are not available in the podcasts",
        "Create a social media group for students to share their experiences and insights from attending class",
        "Organize regular contests or challenges related to class content, with prizes for participants",
        "Provide a comfortable and engaging classroom environment with refreshments and seating arrangements",
        "Incorporate gamification elements into the class structure, such as quizzes or team-based activities",
    ],
    response_length='5 bullet points'
)

### Generate output
response = session.generate_idea(
    Technique.CHAIN_OF_THOUGHT,
    Hat.BLACK,
    brainstormingInput
)

### Print output
print(response)
```

### Hats
The different hats act as a predefined persona according to Edward de Bono's book about the six thinking hats in brainstorming. You can select which persona should be used for your instance.
Hat   | Role
----  | ----
WHITE | The White Hat represents neutrality and objectivity, focusing on gathering facts, identifying information gaps, and evaluating existing knowledge to ensure all reasoning is grounded in evidence and logic.

GREEN | The Green Hat represents creativity and innovation, focusing on generating new ideas, exploring alternatives, and proposing improvements to existing concepts to encourage original and unconventional thinking.

BLACK | The Black Hat represents critical judgment and caution, focusing on identifying potential risks, weaknesses, and negative outcomes of ideas to ensure they are practical and safe.

YELLOW| The Yellow Hat represents optimism and positivity, focusing on identifying the benefits, strengths, and potential value of ideas to highlight why they are worth pursuing.

BLUE  | The Blue Hat represents control, organization, and overview, guiding the thinking process, setting objectives, managing the discussion, and ensuring that the Six Thinking Hats method is followed effectively.

RED   | The Red Hat represents emotions, intuition, and gut feelings, allowing participants to express their instincts or emotional reactions to ideas without the need for justification or logic.
source: [Book](https://swisscovery.slsp.ch/permalink/41SLSP_NETWORK/1ufb5t2/alma991081046019705501)


### Prompting techniques
The different prompting techniques help to analyse different approaches of idea generation for each hat. While implementing, we analyzed which of the techniques work best for which hat.
Technique               | Explanation
----                    | ----
CHAIN_OF_THOUGHT        | Chain of Thought leverages GPT-o1's advanced reasoning capabilities.

CHAINING                | Chaining creates a chain of three steps: 1. Understand the thinking hat; 2. Use the perspective of the hat on the brainstorming context; 3. Refine the generated response and make sure it aligns with the thinking hat.

FEW_SHOT                | The Few Shot method first uses a meta prompt to generate three examples of how the given hat would reply in a brainstorming session. These examples are then used as guidance for generating a response to the given brainstorming session.

SYSTEM_2_ATTENTION      | S2A is a two step technique, that first prompt organizes and filters the ideas from the brainstorming session and then uses this optimized input for the next prompt.

PERSONA_PATTERN         | The Persona Pattern technique generates ideas by adopting predefined persona, offering unique perspective and goals.

CHAIN_OF_VERIFICATION   | The Chain of Verification technique refines ideas by chaining prompts, generating verification questions, and analyzing responses.

CONTRASTIVE_PROMPTING   | The Contrastive Prompting technique uses examples of good and bad responses to guide the agent towards an optimal output.

MULTI_AGENT             | The Multi-Agent technique involves multiple agents collaborating on a topic before converging on a refined final output.

ZERO_SHOT_COT           | The Zero-shot Chain-of-Thought technique guides the model to reason step-by-step, breaking down complex problems into intermediate steps for improved accuracy and transparency.

REACT                   | The ReAct (Reason and Act) technique combines reasoning and action by allowing models to interleave thought processes with tool use, enabling more accurate and interactive problem-solving.

EMOTION_PROMPT          | The EmotionPrompt technique enhances model performance by embedding emotional stimuli in prompts, encouraging more engaged, human-like, and context-aware responses.

TAKE_A_STEP_BACK        | The Take-a-Step-Back technique adds a follow-up question prompting the model to reflect on its initial reasoning before giving a final answer.



### Brainstorming-input
The instance of BrainstormingInput allows you to pass the brainstorming `question`, `ideas`and `response_length` to the generation of an idea.
Variable Name    | Explanation
----             | ----
question         | This variable takes a `string`, the question that was asked in the brainstorming session
ideas            | This variable takes a `list of strings` where each string is a idea from the brainstorming session
response_length  | This variable takes a `string` which will control the length of the answer. You can say "10 sentences" but also things like "similar to the other ideas". It should fit the sentence: Provide a response with a length of {response_length}.


### Developer mode
The developer mode is used to log the in/outputs of the api calls. A log folder and log files will be created when executing a Script with activated developer mode. This was implemented for prompt engineering purposes and help to analyse the history of all API calls made. 

It can be activated by setting the `dev` attribute to `True` (default `False`).
```python
instance.dev = True
```


## Installation
This package is available through the [Python
Package Index (PyPI)](https://pypi.org/project/thinking-hats-ai).

```sh
pip install thinking-hats-ai
```


## Dependencies
- [LangChain - A framework for developing applications powered by language models](https://www.langchain.com)
- [AG2 - A multi-agent framework for building AI-driven systems](https://ag2.ai)
- [Autogen - A framework for enabling autonomous AI agents to collaborate](https://microsoft.github.io/autogen/stable//index.html)


## Background
The implementation of ``thinking-hats-ai`` started at [UZH](https://www.uzh.ch) as a part of three bachelors theses.


## Creators
- Timon Derboven - [timon.derboven@uzh.ch](mailto:timon.derboven@uzh.ch)
- Leon Braga - [leonroberto.braga@uzh.ch](mailto:leonroberto.braga@uzh.ch)
- Marc Huber - [marctimothy.huber@uzh.ch](mailto:marctimothy.huber@uzh.ch)


<hr>

[Go to Top](#table-of-contents)