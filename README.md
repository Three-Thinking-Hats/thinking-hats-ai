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
    - [Developer mode](#developer-mode)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Background](#background)
- [Creators](#creators)


## Use of Package
### Example script
This example uses the `CHAIN_OF_THOUGHT` [prompting techniques](#prompting-techniques) and the `BLACK` [hat](#hats) for the personality. It also uses [developer mode](#developer-mode) to log the interaction in a separate file.
```python
import thinking_hats_ai

instance = thinking_hats_ai.BrainstormingSession('YOUR-OPENAI-API-KEY')

instance.dev = True

idea = instance.generate_idea(
    thinking_hats_ai.Technique.CHAIN_OF_THOUGHT,
    thinking_hats_ai.Hat.BLACK,
    'how could you make students come to class more often even though there are podcasts provided for each lecture?'
)

print(idea)
```

### Hats
The different hats act as a predefined persona according to Edward de Bono's book about the six thinking hats in brainstorming. You can select which persona should be used for your instance.
Hat   | Role
----  | ----
BLACK | TODO
WHITE | TODO
YELLOW| TODO
GREEN | TODO
BLUE  | TODO
RED   | TODO
source: [Book](https://swisscovery.slsp.ch/permalink/41SLSP_NETWORK/1ufb5t2/alma991081046019705501)


### Prompting techniques
The different prompting techniques help to analyse different approaches of idea generation for each hat. While implementing, we analyzed which of the techniques work best for which hat.
Technique        | Explanation
----             | ----
CHAIN_OF_THOUGHT | TODO


### Developer mode
The developer mode is used to log the in/outputs of the api calls. This was implemented for prompt engineering purposes and help to analyse the history of all API calls made. 

It can be activated by setting the `dev` attribute to `True` or `False`:
```python
instance.dev = True / False
```


## Installation
This package is available through the [Python
Package Index (PyPI)](https://pypi.org/project/thinking-hats-ai).

```sh
pip install thinking-hats-ai
```


## Dependencies
- [LangChain - A framework for developing applications powered by language models](https://www.langchain.com)


## Background
The implementation of ``thinking-hats-ai`` started at [UZH](https://www.uzh.ch) as a part of three bachelors theses.


## Creators
- Timon Derboven - [timon.derboven@uzh.ch](mailto:timon.derboven@uzh.ch)
- Leon Braga - [leonroberto.braga@uzh.ch](mailto:leonroberto.braga@uzh.ch)
- Marc Huber - [marctimothy.huber@uzh.ch](mailto:marctimothy.huber@uzh.ch)


<hr>

[Go to Top](#table-of-contents)