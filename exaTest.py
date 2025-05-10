# pip install exa-py
from exa_py import Exa
from os import getenv
exa = Exa(api_key = getenv("EXA_API_KEY"))
result = exa.search_and_contents(
    "找到有关AGI的博客文章",
    text = { "max_characters": 1000 }
)
print(result)