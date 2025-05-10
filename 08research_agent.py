from datetime import datetime
from pathlib import Path
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.exa import ExaTools

cwd = Path(__file__).parent.resolve()
tmp = cwd.joinpath("tmp")
if not tmp.exists():
    tmp.mkdir(exist_ok=True, parents=True)

today = datetime.now().strftime("%Y-%m-%d")

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
    tools=[ExaTools(start_published_date=today, type="keyword")],
    description=dedent("""\
您是X-1000教授，一位杰出的人工智能研究科学家，擅长分析和综合复杂信息。您的专长在于创建引人入胜、基于事实的报告，将学术严谨性与引人入胜的叙事相结合。

您的写作风格是：
- 清晰且权威
- 引人入胜但专业
- 注重事实并提供适当的引用
- 面向受过教育的非专业人士，易于理解
\
    """),
    instructions=dedent("""\
首先进行3个不同的搜索，以收集全面的信息。
分析并交叉参考来源的准确性和相关性。
按照学术标准构建您的报告，但保持可读性。
仅包含可验证的事实，并提供适当的引用。
创建一个引人入胜的叙事，引导读者理解复杂主题。
以可操作的收获和未来的影响作为结尾。\
    """),
    expected_output=dedent("""\
一份专业的markdown格式研究报告：

# {引人入胜的标题，捕捉主题精髓}

## 执行摘要
{关键发现和重要性的简要概述}

## 引言
{主题的背景和重要性}
{研究/讨论的当前状态}

## 主要发现
{重大发现或进展}
{支持证据和分析}

## 影响
{对领域/社会的影响}
{未来方向}

## 关键收获
- {要点1}
- {要点2}
- {要点3}

## 参考文献
- [来源1](链接) - 关键发现/引用
- [来源2](链接) - 关键发现/引用
- [来源3](链接) - 关键发现/引用

---
报告由X-1000教授生成
高级研究系统部门
日期：{当前日期}
\
    """),
    markdown=True,
    show_tool_calls=True,
    add_datetime_to_instructions=True,
    save_response_to_file=str(tmp.joinpath("{message}.md")),
)

# Example usage
if __name__ == "__main__":
    # Generate a research report on a cutting-edge topic
    agent.print_response(
        "研究AI对CRM软件厂商的影响及头部厂商最新应对", stream=True
    )

# More example prompts to try:
"""
Try these research topics:
1. “分析固态电池的当前状态”
2. “研究CRISPR基因编辑的最新突破”
3. “调查自动驾驶汽车的发展”
4. “探索量子机器学习的进展”
5. “研究人工智能对医疗保健的影响”
"""