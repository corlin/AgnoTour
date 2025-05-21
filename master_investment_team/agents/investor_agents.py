from agno.agent import Agent
from agno.tools.reasoning import ReasoningTools

# Assuming other necessary tools like your custom financial tools might be added later or via a team setup.
# TODO: Ensure custom financial tools (ValuationTool, TechnicalAnalysisTool, FundamentalRatioTool) are correctly passed and accessible if needed directly by agents,
# or ensure their outputs are passed via company_profile or market_data.

class BaseInvestorAgent(Agent):
    def __init__(self, model=None, tools=None, instructions=None, knowledge_base=None, name: str = "BaseInvestorAgent", **kwargs):
        default_tools = [ReasoningTools(add_instructions=True)]
        if tools:
            # Ensure tools are appended correctly, avoiding list of lists
            if isinstance(tools, list):
                default_tools.extend(tools)
            else:
                default_tools.append(tools)
        
        super().__init__(model=model, tools=default_tools, instructions=instructions, name=name, **kwargs)
        self.knowledge_base = knowledge_base if knowledge_base is not None else []

    async def run_analysis(self, company_profile: dict, market_data: dict) -> dict:
        # company_profile example: {"ticker": "AAPL", "name": "Apple Inc.", "sector": "Technology"}
        # market_data example: {"AAPL": {"price": 150, "volume": 1000000}, "market_sentiment": "neutral", "AAPL_financials": {...}, "AAPL_quant_signals": "..."}
        print(f"{self.name} using knowledge: {self.knowledge_base} and instructions: {self.instructions} to analyze {company_profile.get('ticker', 'N/A')}")
        
        # TODO: Replace mock reasoning with actual LLM calls using self.call_llm() or specific reasoning tool methods, incorporating self.knowledge_base and self.instructions.
        # Example:
        # prompt = (
        #     f"As a {self.name.replace('Agent', '')}, your instructions are: {self.instructions}. "
        #     f"Your knowledge base includes: {self.knowledge_base}. "
        #     f"Analyze the company: {company_profile}. "
        #     f"Consider the market data: {market_data}. "
        #     f"Provide your investment recommendation (Buy/Sell/Hold), confidence level (0.0-1.0), and a brief reasoning summary."
        # )
        # llm_response = await self.reason(prompt=prompt) # or self.call_llm(prompt=prompt)
        # reasoning_summary = llm_response.get("output", "Could not generate reasoning.")
        # recommendation = llm_response.get("recommendation", "Hold") # Assuming LLM provides structured output
        # confidence = llm_response.get("confidence", 0.5)

        # TODO: Implement logic to parse and use data from custom financial tools (ValuationTool, TechnicalAnalysisTool, FundamentalRatioTool) passed via the Team/Workflow.
        # This data would typically be found within market_data (e.g., market_data.get(f"{company_profile.get('ticker')}_valuation_tool_output")).
        # Example: valuation_metrics = market_data.get(f"{company_profile.get('ticker')}_valuation", {})
        # dcf_value = valuation_metrics.get("dcf_value")
        # This would influence the prompt or logic above.

        reasoning_summary = f"Based on {self.name}'s philosophy and placeholder analysis of {company_profile.get('ticker', 'N/A')}, a decision has been formulated."

        return {
            "ticker": company_profile.get('ticker', 'N/A'),
            "recommendation": "Hold", 
            "confidence": 0.5,
            "reasoning_summary": reasoning_summary,
            "philosophy": self.name.replace("Agent", " Investing")
        }

class ValueInvestorAgent(BaseInvestorAgent):
    def __init__(self, model=None, tools=None, **kwargs):
        value_instructions = [
            "Analyze the provided financial data for intrinsic value, focusing on P/E, P/B ratios, and debt levels.",
            "Formulate an investment thesis based on identifying companies trading below their fair value."
        ]
        value_knowledge = [
            "Focus on undervalued companies with a strong margin of safety.",
            "Prefer businesses with consistent earnings, strong free cash flow, and low debt."
        ]
        super().__init__(model=model, 
                         tools=tools, 
                         instructions=value_instructions, 
                         knowledge_base=value_knowledge, 
                         name="ValueInvestorAgent",
                         **kwargs)

    async def run_analysis(self, company_profile: dict, market_data: dict) -> dict:
        print(f"{self.name} using knowledge: {self.knowledge_base} and instructions: {self.instructions} to analyze {company_profile.get('ticker', 'N/A')}")
        
        # TODO: Replace mock reasoning with actual LLM calls using self.call_llm() or specific reasoning tool methods, incorporating self.knowledge_base and self.instructions.
        # TODO: Implement logic to parse and use data from custom financial tools (e.g., ValuationTool's DCF output from market_data).
        reasoning_summary = f"Based on value principles and placeholder analysis of {company_profile.get('ticker', 'N/A')}'s fundamentals, the company appears undervalued."
        
        return {
            "ticker": company_profile.get('ticker', 'N/A'),
            "recommendation": "Buy", 
            "confidence": 0.75,
            "reasoning_summary": reasoning_summary,
            "philosophy": "Value Investing"
        }

class GrowthInvestorAgent(BaseInvestorAgent):
    def __init__(self, model=None, tools=None, **kwargs):
        growth_instructions = [
            "Identify companies with significant revenue and earnings growth potential.",
            "Assess the scalability of the business model and the size of the total addressable market."
        ]
        growth_knowledge = [
            "Identify companies with high growth potential, even if currently unprofitable, focusing on revenue acceleration.",
            "Look for disruptive technologies, innovative products, and large, expanding addressable markets."
        ]
        super().__init__(model=model, 
                         tools=tools, 
                         instructions=growth_instructions, 
                         knowledge_base=growth_knowledge, 
                         name="GrowthInvestorAgent",
                         **kwargs)

    async def run_analysis(self, company_profile: dict, market_data: dict) -> dict:
        print(f"{self.name} using knowledge: {self.knowledge_base} and instructions: {self.instructions} to analyze {company_profile.get('ticker', 'N/A')}")
        
        # TODO: Replace mock reasoning with actual LLM calls using self.call_llm() or specific reasoning tool methods, incorporating self.knowledge_base and self.instructions.
        # TODO: Implement logic to parse and use data from custom financial tools (e.g., looking at growth metrics from FundamentalRatioTool or market trends).
        reasoning_summary = f"Based on growth potential analysis of {company_profile.get('ticker', 'N/A')}, the company shows strong prospects for expansion."
        
        return {
            "ticker": company_profile.get('ticker', 'N/A'),
            "recommendation": "Buy", 
            "confidence": 0.80,
            "reasoning_summary": reasoning_summary,
            "philosophy": "Growth Investing"
        }

class MacroInvestorAgent(BaseInvestorAgent):
    def __init__(self, model=None, tools=None, **kwargs):
        macro_instructions = [
            "Analyze broad economic indicators (e.g., GDP growth, inflation, interest rates) and geopolitical events provided in market_data.",
            "Formulate investment strategies based on anticipated macroeconomic shifts and their impact on the given market_sector or company_profile."
        ]
        macro_knowledge = [
            "Analyze broad economic trends, fiscal/monetary policies, and geopolitical factors.",
            "Identify investment opportunities or risks based on macroeconomic shifts, sector rotations, and global capital flows."
        ]
        super().__init__(model=model, 
                         tools=tools, 
                         instructions=macro_instructions, 
                         knowledge_base=macro_knowledge, 
                         name="MacroInvestorAgent",
                         **kwargs)

    async def run_analysis(self, company_profile: dict, market_data: dict, market_sector: str = "General Market") -> dict:
        print(f"{self.name} using knowledge: {self.knowledge_base} and instructions: {self.instructions} to analyze macro trends affecting {market_sector} and potentially {company_profile.get('ticker', 'N/A')}.")
        
        # TODO: Replace mock reasoning with actual LLM calls using self.call_llm() or specific reasoning tool methods, incorporating self.knowledge_base and self.instructions.
        # The prompt for this agent would heavily focus on the 'market_conditions' part of market_data and the 'market_sector'.
        # Example prompt focus: "Given market_data: {market_data['key_economic_indicators']}, how does this impact {market_sector} and {company_profile.get('ticker')}?"
        reasoning_summary = f"Based on macroeconomic analysis of {market_sector} (details in market_data: {market_data.get('key_economic_indicators', {})}), current trends suggest a specific outlook for {company_profile.get('sector', 'this sector')}."
        
        return {
            "sector_analyzed": market_sector,
            "ticker_context": company_profile.get('ticker', 'N/A'),
            "recommendation": "Allocate to sector", 
            "confidence": 0.65,
            "reasoning_summary": reasoning_summary,
            "philosophy": "Macro Investing"
        }

class ContrarianInvestorAgent(BaseInvestorAgent):
    def __init__(self, model=None, tools=None, **kwargs):
        contrarian_instructions = [
            "Identify assets that are currently unpopular or undervalued by the market due to irrational pessimism, based on company_profile and market_data.",
            "Challenge prevailing market sentiment (e.g., market_data['news_sentiment']) and look for opportunities where the consensus view may be wrong."
        ]
        contrarian_knowledge = [
            "Look for investments that are currently out of favor with the market, despite sound fundamentals.",
            "Question conventional wisdom, identify mispriced assets due to herd behavior or excessive negativity."
        ]
        super().__init__(model=model, 
                         tools=tools, 
                         instructions=contrarian_instructions, 
                         knowledge_base=contrarian_knowledge, 
                         name="ContrarianInvestorAgent",
                         **kwargs)

    async def run_analysis(self, company_profile: dict, market_data: dict) -> dict:
        print(f"{self.name} using knowledge: {self.knowledge_base} and instructions: {self.instructions} to analyze {company_profile.get('ticker', 'N/A')}")
        
        # TODO: Replace mock reasoning with actual LLM calls using self.call_llm() or specific reasoning tool methods, incorporating self.knowledge_base and self.instructions.
        # Prompt focus: "Company {company_profile.get('ticker')} has market sentiment {market_data.get('news_sentiment')}. Is this a contrarian opportunity?"
        reasoning_summary = f"Based on a contrarian viewpoint, recent negative sentiment towards {company_profile.get('ticker', 'N/A')} (sentiment: {market_data.get('news_sentiment')}) might be overblown, presenting a potential opportunity."
        
        return {
            "ticker": company_profile.get('ticker', 'N/A'),
            "recommendation": "Consider Buy (Contrarian)", 
            "confidence": 0.60,
            "reasoning_summary": reasoning_summary,
            "philosophy": "Contrarian Investing"
        }
