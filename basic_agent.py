from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Create our News Reporter with a fun personality
agent = Agent(
    model=OpenAIChat(
        id="x-ai/grok-3-beta",
        #grok-3
        #grok-3-mini
        #x-ai/grok-3-mini-beta
        base_url="https://openrouter.ai/api/v1"
        #"https://api.x.ai/v1"
        ),
    instructions=dedent("""\
    你是一位充满热情的新闻报道员，具有讲故事的天赋！🗽
    你的风格融合了机智的喜剧演员和敏锐的记者。

    你的风格指南：
    - 使用表情符号开头，吸引注意力
    - 以热情和纽约风格分享新闻
    - 回应保持简洁但有趣
    - 在适当的时候加入本地参考和纽约俚语
    - 结尾使用朗朗上口的结束语，例如“回到演播室！”或“从大苹果现场报道！”

    在保持高能量的同时，请务必核实所有事实！\
"""),
    markdown=True,
)

# Example usage
agent.print_response(
    "请告诉我时代广场正在发生的突发新闻。", stream=True
)

# More example prompts to try:
"""
尝试以下有趣的场景：
1. “布鲁克林最新的美食潮流是什么？”
2. “告诉我今天地铁上发生的一件奇特事件。”
3. “曼哈顿最新屋顶花园有什么消息？”
4. “报道一起由逃跑动物园动物引起的异常交通堵塞。”
5. “报道在大中央车站发生的快闪求婚活动。”
"""