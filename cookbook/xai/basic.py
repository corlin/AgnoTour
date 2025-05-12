from agno.agent import Agent, RunResponse  # noqa
from agno.models.xai import xAI

agent = Agent(model=xAI(
    id="x-ai/grok-3-beta",
    #grok-3
    #grok-3-mini
    #x-ai/grok-3-mini-beta
    base_url="https://openrouter.ai/api/v1"
    #"https://api.x.ai/v1"
    ), 
    markdown=True
)

# Print the response in the terminal
agent.print_response("请模仿曹雪芹,写一首风花雪月的七律诗!",stream=True)