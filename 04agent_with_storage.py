from textwrap import dedent
from typing import List, Optional

import typer
from agno.agent import Agent
from agno.embedder.mistral import MistralEmbedder#OpenAIEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.lancedb import LanceDb, SearchType
from rich import print
from os import getenv

agent_knowledge = PDFUrlKnowledgeBase(
    urls=["https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
    vector_db=LanceDb(
        uri="tmp/lancedb",
        table_name="recipe_knowledge",
        search_type=SearchType.hybrid,
        embedder=MistralEmbedder(
                    id="mistral-embed",
                    #base_url="https://api.mistral.ai/v1",
                    api_key=getenv("EMB_MIS_URL")
                    ),
    ),
)

agent_storage = SqliteStorage(table_name="recipe_agent", db_file="tmp/agents.db")


def recipe_agent(user: str = "user"):
    session_id: Optional[str] = None

    # Ask the user if they want to start a new session or continue an existing one
    new = typer.confirm("Do you want to start a new session?")

    if not new:
        existing_sessions: List[str] = agent_storage.get_all_session_ids(user)
        if len(existing_sessions) > 0:
            session_id = existing_sessions[0]

    agent = Agent(
        user_id=user,
        session_id=session_id,
        model=OpenAIChat(
            id="gpt-4o",
            base_url="https://openrouter.ai/api/v1"
            ),
        instructions=dedent("""\
您是一位充满热情且知识渊博的泰国美食专家！🧑‍🍳
将自己视为一位温暖、鼓励的烹饪导师、
泰国美食历史学家以及文化大使的结合体。

回答问题时请遵循以下步骤：
1. 首先，搜索知识库以获取正宗的泰国食谱和烹饪信息
2. 如果知识库中的信息不完整，或者用户提出的问题更适合网络搜索，则通过网络搜索来填补空白
3. 如果在知识库中找到信息，则无需搜索网络
4. 始终优先考虑知识库信息而非网络结果，以确保真实性
5. 如有需要，可通过网络搜索补充以下内容：
   - 现代改编或食材替代
   - 文化背景和历史背景
   - 额外的烹饪技巧和故障排除

沟通风格：
1. 每条回复以相关的烹饪表情符号开头
2. 清晰地组织您的回复：
   - 简短的介绍或背景
   - 主要内容（食谱、解释或历史）
   - 专业提示或文化见解
   - 鼓励性的结语
3. 对于食谱，包括：
   - 食材列表及可能的替代品
   - 清晰的、编号的烹饪步骤
   - 成功秘诀和常见陷阱
4. 使用友好、鼓励的语言

特别功能：
- 解释不熟悉的泰国食材并建议替代品
- 分享相关的文化背景和传统
- 提供调整食谱以适应不同饮食需求的建议
- 包括搭配建议和配菜

每次回复结束时使用令人振奋的签名，例如：
- '祝您烹饪愉快！ขอให้อร่อย（享用您的美食）！'
- '愿您的泰国烹饪冒险带来欢乐！'
- '享受您自制的泰国盛宴！'

记住：
- 始终通过知识库验证食谱的真实性
- 明确指出信息来自网络来源
- 对所有技能水平的家庭厨师保持鼓励和支持
\
        """),
        storage=agent_storage,
        knowledge=agent_knowledge,
        tools=[DuckDuckGoTools()],
        # Show tool calls in the response
        show_tool_calls=True,
        # To provide the agent with the chat history
        # We can either:
        # 1. Provide the agent with a tool to read the chat history
        # 2. Automatically add the chat history to the messages sent to the model
        #
        # 1. Provide the agent with a tool to read the chat history
        read_chat_history=True,
        # 2. Automatically add the chat history to the messages sent to the model
        # add_history_to_messages=True,
        # Number of historical responses to add to the messages.
        num_history_responses=3,
        markdown=True,
    )

    print("You are about to chat with an agent!")
    if session_id is None:
        session_id = agent.session_id
        if session_id is not None:
            print(f"Started Session: {session_id}\n")
        else:
            print("Started Session\n")
    else:
        print(f"Continuing Session: {session_id}\n")

    # Runs the agent as a command line application
    agent.cli_app(markdown=True,stream=
                  True)


if __name__ == "__main__":
    # Comment out after the knowledge base is loaded
    if agent_knowledge is not None:
        agent_knowledge.load()

    typer.run(recipe_agent)