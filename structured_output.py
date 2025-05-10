from textwrap import dedent
from typing import List

from agno.agent import Agent, RunResponse  # noqa
from agno.models.openai import OpenAIChat
from pydantic import BaseModel, Field


class MovieScript(BaseModel):
    setting: str = Field(
        ...,
        description="电影主要地点和时间段的丰富详细、充满氛围的描述。包括感官细节和情绪。",
    )
    ending: str = Field(
        ...,
        description="电影有力的结局，连接所有情节线索。应带来情感冲击和满足感。",
    )
    genre: str = Field(
        ...,
        description="电影的主要和次要类型（例如，'科幻惊悚片'，'浪漫喜剧'）。应与场景和基调一致。",
    )
    name: str = Field(
        ...,
        description="一个引人注目、令人难忘的标题，捕捉故事的精髓并吸引目标观众。",
    )
    characters: List[str] = Field(
        ...,
        description="4-6个主要角色，带有独特的名字和简短的角色描述（例如，'陈洁娜' - 拥有黑暗秘密的杰出量子物理学家'）。",
    )
    storyline: str = Field(
        ...,
        description="一个引人入胜的三句话情节摘要：设置、冲突和赌注。用 阴谋 和 情感 吸引读者。",
    )



# Agent that uses JSON mode
json_mode_agent = Agent(
    model=OpenAIChat(
        id="openai/gpt-4o",
        #"deepseek/deepseek-chat-v3-0324",
        #"openai/gpt-4o",
        #x-ai/grok-3-beta",
        #grok-3
        #grok-3-mini
        #x-ai/grok-3-mini-beta
        base_url="https://openrouter.ai/api/v1"
        #"https://api.x.ai/v1"
    ),
    description=dedent("""\
您是一位备受赞誉的好莱坞编剧，以创作令人难忘的大片而闻名！🎬
拥有克里斯托弗·诺兰、亚伦·索金和昆汀·塔伦蒂诺的综合叙事才能，
您打造出独特的故事情节，吸引了全世界的观众。

您的专长是将地点转化为鲜活的、会呼吸的角色，推动叙事发展。
\
    """),
    instructions=dedent("""\
在创作电影概念时，请遵循以下原则：

1. 场景应成为角色：
   - 用感官细节让地点变得生动
   - 包含影响故事的氛围元素
   - 考虑时间段对叙事的影响

2. 角色发展：
   - 赋予每个角色独特的声音和明确的动机
   - 创造引人入胜的关系和冲突
   - 确保多样化的代表性和真实的背景

3. 故事结构：
   - 以一个吸引注意力的钩子开始
   - 通过不断升级的冲突建立紧张感
   - 提供令人惊讶却又必然的结局

4. 类型掌握：
   - 拥抱类型惯例，同时加入新鲜的转折
   - 深思熟虑地混合类型以获得独特的组合
   - 保持一致的基调贯穿始终

将每个地点转化为令人难忘的电影体验！\
    """),
    response_model=MovieScript,
)

# Agent that uses structured outputs
structured_output_agent = Agent(
    model=OpenAIChat(
        id="openai/gpt-4o",
        #"deepseek/deepseek-chat-v3-0324",
        #"openai/gpt-4o",
        #x-ai/grok-3-beta",
        #grok-3
        #grok-3-mini
        #x-ai/grok-3-mini-beta
        base_url="https://openrouter.ai/api/v1"
        #"https://api.x.ai/v1"
    ),
    description=dedent("""\
您是一位备受赞誉的好莱坞编剧，以创作令人难忘的大片而闻名！🎬
拥有克里斯托弗·诺兰、亚伦·索金和昆汀·塔伦蒂诺的综合叙事才能，
您打造出独特的故事情节，吸引了全世界的观众。

您的专长是将地点转化为鲜活的、会呼吸的角色，推动叙事发展。\
    """),
    instructions=dedent("""\
在创作电影概念时，请遵循以下原则：

1. 场景应成为角色：
   - 用感官细节让地点变得生动
   - 包含影响故事的氛围元素
   - 考虑时间段对叙事的影响

2. 角色发展：
   - 赋予每个角色独特的声音和明确的动机
   - 创造引人入胜的关系和冲突
   - 确保多样化的代表性和真实的背景

3. 故事结构：
   - 以一个吸引注意力的钩子开始
   - 通过不断升级的冲突建立紧张感
   - 提供令人惊讶却又必然的结局

4. 类型掌握：
   - 拥抱类型惯例，同时加入新鲜的转折
   - 深思熟虑地混合类型以获得独特的组合
   - 保持一致的基调贯穿始终

将每个地点转化为令人难忘的电影体验！\
    """),
    response_model=MovieScript,
)

# Example usage with different locations
json_mode_agent.print_response("东京", stream=True)
structured_output_agent.print_response("古罗马", stream=True)

# More examples to try:
"""
探索的创意地点提示：
1. “水下研究站” - 适用于 幽闭恐惧症 式的 科幻惊悚片
2. “维多利亚时代伦敦” - 适用于哥特式神秘故事
3. “迪拜2050” - 适用于未来主义抢劫电影
4. “南极研究基地” - 适用于生存恐怖故事
5. “加勒比岛屿” - 适用于热带冒险浪漫故事

"""

# To get the response in a variable:
from rich.pretty import pprint

json_mode_response: RunResponse = json_mode_agent.run("“维多利亚时代伦敦”")
pprint(json_mode_response.content)
structured_output_response: RunResponse = structured_output_agent.run("迪拜2050")
pprint(structured_output_response.content)