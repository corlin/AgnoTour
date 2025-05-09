from agno.agent import Agent
from agno.models.xai import xAI
from agno.tools.duckduckgo import DuckDuckGoTools

agent = Agent(
    model=xAI(
        id="x-ai/grok-3-beta",
        #grok-3
        #grok-3-mini
        #x-ai/grok-3-mini-beta
        base_url="https://openrouter.ai/api/v1"
        #"https://api.x.ai/v1"
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,    
)
agent.print_response("巴基斯坦和印度今天的军事紧张局势有什么最新动态?", stream=True)