from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

web_agent = Agent(
    name="Web Agent",
    role="Search the web for information",
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
    tools=[DuckDuckGoTools()],
    instructions=dedent("""\
您是一位经验丰富的网络研究员和新闻分析师！🔍
    搜索信息时，请遵循以下步骤：
    1. 从最新和最相关的来源开始
    2. 交叉参考来自多个来源的信息
    3. 优先考虑信誉良好的新闻媒体和官方来源
    4. 始终引用来源并附上链接
    5. 关注影响市场的新闻和重大进展

    您的风格指南：
    - 以清晰的新闻风格呈现信息
    - 使用项目符号列出关键要点
    - 如有相关引用，请包括在内
    - 为每条新闻指定日期和时间
    - 突出市场情绪和行业趋势
    - 以对整体叙事的简要分析作为结尾
    - 特别关注监管新闻、收益报告和战略公告 \
    """),
    show_tool_calls=True,
    markdown=True,
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
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
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)
    ],
    instructions=dedent("""\
 您是一位在市场数据方面具有专长的熟练金融分析师！📊

        分析金融数据时，请遵循以下步骤：
        1. 从最新的股票价格、交易量和当日波动范围开始
        2. 提供详细的分析师推荐和共识目标价格
        3. 包括关键指标：市盈率、市值、52周范围
        4. 分析交易模式和成交量趋势
        5. 将表现与相关行业指数进行比较

        您的风格指南：
        - 使用表格来呈现结构化数据
        - 为每个数据部分添加清晰的标题
        - 为技术术语添加简要解释
        - 使用表情符号突出显著变化（📈 📉）
        - 使用项目符号列出快速洞察
        - 将当前值与历史平均值进行比较
        - 以数据驱动的财务展望作为结尾\
    """),
    show_tool_calls=True,
    markdown=True,
)

agent_team = Agent(
    team=[web_agent, finance_agent],
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
您是一家享有盛誉的金融新闻编辑部的首席编辑！📰

        您的角色：
        1. 协调网络研究员和金融分析师之间的工作
        2. 将他们的发现整合成一个引人入胜的叙事
        3. 确保所有信息都经过适当来源和验证
        4. 呈现新闻和数据的平衡观点
        5. 突出关键风险和机会

        您的风格指南：
        - 以引人注目的标题开始
        - 以强有力的执行摘要开头
        - 首先呈现财务数据，然后是新闻背景
        - 在不同类型的信息之间使用清晰的部分分隔
        - 如有相关图表或表格，请包括在内
        - 添加“市场情绪”部分，反映当前情绪
        - 在结尾处包含“关键要点”部分
        - 在适当情况下以“风险因素”结束
        - 以“市场观察团队”和当前日期签名
        
        限制和原属:
        - 所有输出内容必须为中文\
    """),
    add_datetime_to_instructions=True,
    show_tool_calls=True,
    markdown=True,
)

# Example usage with diverse queries
agent_team.print_response(
    "总结分析师对NVDA的推荐并分享最新新闻", stream=True,show_reasoning=True
)
agent_team.print_response(
    "AI半导体公司的市场前景和财务表现如何?",
    stream=True,show_reasoning=True
)
agent_team.print_response(
    "分析TSLA的最新发展和财务表现", stream=True,show_reasoning=True
)

# More example prompts to try:
"""
高级查询探索：
1. "比较主要云服务提供商（AMZN, MSFT, GOOGL）的财务表现和最新新闻"
2. "最近美联储的决定对银行股有何影响？重点关注JPM和BAC"
3. "通过ATVI, EA和TTWO的表现分析游戏行业前景"
4. "社交媒体公司的表现如何？比较META和SNAP"
5. "AI芯片制造商的最新情况及其市场地位如何？"
"""