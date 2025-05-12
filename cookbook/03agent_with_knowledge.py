from textwrap import dedent

from agno.agent import Agent
from agno.embedder.mistral import MistralEmbedder#OpenAIEmbedder
from agno.knowledge.pdf_url import PDFUrlKnowledgeBase
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.vectordb.qdrant import Qdrant#, SearchType

from os import getenv

# Create a Recipe Expert Agent with knowledge of Thai recipes
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
            回答问题时请遵循以下步骤：
            1. 首先，在知识库中搜索正宗的泰国食谱和烹饪相关信息
            2. 如果知识库中的信息不完整，或者用户的问题更适合通过网络搜索解答，请通过网络补充缺失内容
            3. 如果在知识库中找到了相关信息，则无需进行网络搜索
            4. 在真实性方面，始终优先采用知识库中的信息，而非网络结果
            5. 如需通过网络搜索补充信息，可用于以下方面：
                - 现代改良做法或食材替代方案
                - 文化背景与历史渊源
                - 额外的烹饪技巧和常见问题解决办法

            沟通风格：
            1. 每个回答都以一个相关的烹饪表情符号开头
            2. 回答结构要清晰：
                - 简短的介绍或背景
                - 主要内容（食谱、解释或历史）
                - 小贴士或文化见解
                - 鼓励性的结尾
            3. 对于食谱，请包括：
                - 包含替代食材选项的材料清单
                - 清晰的分步烹饪说明
                - 成功要点与常见错误提示
            4. 使用友好、鼓励性的语言

            特色功能：
            - 解释不熟悉的泰国食材，并提供替代品
            - 分享相关文化背景与传统
            - 提供适应不同饮食需求的食谱调整建议
            - 包括上菜建议与搭配推荐

            每次回答以积极向上的结束语收尾，例如：
            - ‘祝你烹饪愉快！ขอให้อร่อย（用餐愉快）！’
            - ‘愿你的泰国美食之旅充满喜悦！’
            - ‘享受你亲手制作的泰式盛宴吧！’

            记住：
            - 始终使用知识库验证食谱的真实性
            - 明确指出哪些信息来自网络资源
            - 鼓励和支持所有技能水平的家庭厨师\
"""),
    knowledge=PDFUrlKnowledgeBase(
        urls=["https://media.doterra.com/us/zh/ebooks/%E6%96%99%E7%90%86%E8%A4%87%E6%96%B9%E5%A5%97%E8%A3%9D%E9%A3%9F%E8%AD%9C-cuisine-blends-collection-cookbook.pdf"],
        #https://agno-public.s3.amazonaws.com/recipes/ThaiRecipes.pdf"],
            vector_db=Qdrant(
                url="localhost:6333",
                collection="recipe_knowledge",
                #check_compatibility=False,
                prefer_grpc=True ,
                #search_type=SearchType.hybrid,
                embedder=MistralEmbedder(
                    id="mistral-embed",
                    #base_url="https://api.mistral.ai/v1",
                    api_key=getenv("EMB_MIS_URL")
                    ),
        ),
    ),
    tools=[DuckDuckGoTools()],
    show_tool_calls=True,
    markdown=True,
    add_references=True,
)

# Comment out after the knowledge base is loaded
if agent.knowledge is not None:
    agent.knowledge.load()

agent.print_response(
    "如何制作椰奶鸡胸肉与高良姜汤", stream=True
)
agent.print_response("泰国咖喱的历史是什么?", stream=True)
agent.print_response("制作泰式炒河粉需要哪些食材?", stream=True)
