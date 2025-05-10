import json
from textwrap import dedent

import httpx
from agno.agent import Agent
from agno.models.openai import OpenAIChat


def get_top_hackernews_stories(num_stories: int = 10) -> str:
    """Use this function to get top stories from Hacker News.

    Args:
        num_stories (int): Number of stories to return. Defaults to 10.

    Returns:
        str: JSON string of top stories.
    """

    # Fetch top story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()

    # Fetch story details
    stories = []
    for story_id in story_ids[:num_stories]:
        story_response = httpx.get(
            f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        )
        story = story_response.json()
        if "text" in story:
            story.pop("text", None)
        stories.append(story)
    return json.dumps(stories)


# Create a Tech News Reporter Agent with a Silicon Valley personality
agent = Agent(
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
    instructions=dedent("""\
        您是一位精通科技的 Hacker News 记者，对所有科技事物充满热情！🤖
将自己想象成硅谷内部人士和科技记者的结合体。

您的风格指南：
- 以引人注目的科技标题开头，使用表情符号
- 以热情和科技前沿的态度呈现 Hacker News 故事
- 保持回答简洁但信息丰富
- 在适当的时候使用科技行业参考和初创公司术语
- 以引人入胜的科技主题告别语结束，如“回到终端！”或“推送到生产环境！”

限制和约束
- 必须以中文输出内容

记住要彻底分析 HN 故事，同时保持高度的科技热情！\
    """),
    tools=[get_top_hackernews_stories],
    show_tool_calls=True,
    markdown=True,
)

# Example questions to try:
# - "What are the trending tech discussions on HN right now?"
# - "Summarize the top 5 stories on Hacker News"
# - "What's the most upvoted story today?"
agent.print_response("总结 Hacker News 上的前 5 个故事?", stream=True)