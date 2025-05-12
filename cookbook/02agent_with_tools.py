from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

# Create a News Reporter Agent with a fun personality
agent = Agent(
    model=OpenAIChat(
        id="deepseek/deepseek-chat-v3-0324",
        #"openai/gpt-4o",
        #x-ai/grok-3-beta",
        #grok-3
        #grok-3-mini
        #x-ai/grok-3-mini-beta
        base_url="https://openrouter.ai/api/v1"
        #"https://api.x.ai/v1"
        
        ),
    instructions=dedent("""\
        你是一位充满热情的新闻报道员，具有讲故事的天赋！🗽
        将自己想象成一位机智的喜剧演员与敏锐的记者的结合体。

        请遵循以下每条报道指南：
        1. 使用相关的表情符号开头，吸引注意力
        2. 利用搜索工具查找当前且准确的信息
        3. 以真实的纽约热情和本地特色呈现新闻
        4. 按照清晰的结构组织报道：
        - 抢眼的标题
        - 简要概括新闻内容
        - 关键细节和引语
        - 本地影响或背景信息
        5. 回应保持简洁但有信息量（最多2-3段）
        6. 加入纽约风格的评论和本地参考内容
        7. 以标志性的结束语结尾

        结束语示例：
        - ‘回到演播室，大家再见！’
        - ‘来自不眠之城现场报道！’
        - ‘这里是[你的名字]，从曼哈顿中心为您直播！’

        记住：始终通过网络搜索核实事实，并保持那股真实的纽约能量！\
    """),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
)

# Example usage
agent.print_response(
    "今天是2025年5月8日,巴基斯坦和印度今天的军事紧张局势有什么最新动态?", stream=True
)

# More example prompts to try:
"""
尝试以下引人入胜的新闻查询：
1. “纽约市科技圈最近有什么新动态？”
2. “告诉我有关麦迪逊广场花园即将举行的活动。”
3. “请告诉我时代广场正在发生的突发新闻。”
4. “纽约地铁系统有什么最新消息？”
5. “目前曼哈顿最火的美食潮流是什么？”
6. "今天是2025年5月3日,今天天气对纽约市有何影响？"
"""