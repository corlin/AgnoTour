import asyncio
from master_investment_team.workflows.investment_workflow import InvestmentStrategyWorkflow
from master_investment_team.agents.specialist_agents import ( # Still useful for team display
    FinancialDataAgent,
    QuantitativeAnalysisAgent,
    RiskAssessmentAgent,
    PortfolioOrchestrationAgent,
)
from master_investment_team.agents.investor_agents import ( # Still useful for team display
    ValueInvestorAgent,
    GrowthInvestorAgent,
    MacroInvestorAgent,
    ContrarianInvestorAgent,
)
from agno.teams import Team # To show team structure

async def main():
    print("--- Master Investment Team Simulation using Workflow ---")

    # 1. Instantiate the Workflow
    investment_workflow = InvestmentStrategyWorkflow()
    print(f"Initialized Workflow: {investment_workflow.name} - {investment_workflow.description}")

    # 2. Define mock inputs for the workflow - SCENARIO 1: MSFT (Tech, Neutral)
    target_ticker_msft = "MSFT"
    target_sector_tech = "Technology"
    market_conditions_neutral = {
        "overall_trend": "neutral", 
        "news_sentiment": "mixed",
        "interest_rate_outlook": "stable",
        "key_economic_indicators": {"gdp_growth": "0.5%", "inflation": "2.0%"}
    }
    
    # SCENARIO 2: GOOG (Tech, Bullish)
    target_ticker_goog = "GOOG"
    market_conditions_bullish = {
        "overall_trend": "bullish",
        "news_sentiment": "positive",
        "interest_rate_outlook": "low",
        "key_economic_indicators": {"gdp_growth": "1.5%", "inflation": "1.8%"}
    }

    # SCENARIO 3: JPM (Financials, Bearish)
    target_ticker_jpm = "JPM"
    target_sector_financials = "Financials"
    market_conditions_bearish = {
        "overall_trend": "bearish",
        "news_sentiment": "negative",
        "interest_rate_outlook": "rising",
        "key_economic_indicators": {"gdp_growth": "-0.2%", "inflation": "3.5%", "unemployment": "5.0%"}
    }

    # SCENARIO 4: BABA (E-commerce/China, Volatile - Mock non-US stock)
    target_ticker_baba = "BABA"
    target_sector_ecommerce = "E-commerce" # Could also be "Emerging Markets Technology"
    market_conditions_volatile_em = {
        "overall_trend": "volatile",
        "news_sentiment": "mixed with high uncertainty",
        "regulatory_outlook": "tightening",
        "currency_fluctuation_risk": "high",
        "key_economic_indicators": {"gdp_growth_china": "4.5%", "global_shipping_index": "elevated"}
    }


    # 3. Call the workflow for each scenario
    print(f"\n--- Scenario 1: Running Workflow for {target_ticker_msft} ({target_sector_tech}, Neutral Market) ---")
    workflow_output_msft = await investment_workflow.run(
        target_ticker=target_ticker_msft,
        target_sector=target_sector_tech,
        market_conditions=market_conditions_neutral
    )
    print(f"\n--- Workflow Output (Final Investment Instructions for {target_ticker_msft}) ---")
    print(workflow_output_msft)

    print(f"\n--- Scenario 2: Running Workflow for {target_ticker_goog} ({target_sector_tech}, Bullish Market) ---")
    workflow_output_goog = await investment_workflow.run(
        target_ticker=target_ticker_goog,
        target_sector=target_sector_tech,
        market_conditions=market_conditions_bullish
    )
    print(f"\n--- Workflow Output (Final Investment Instructions for {target_ticker_goog}) ---")
    print(workflow_output_goog)

    print(f"\n--- Scenario 3: Running Workflow for {target_ticker_jpm} ({target_sector_financials}, Bearish Market) ---")
    workflow_output_jpm = await investment_workflow.run(
        target_ticker=target_ticker_jpm,
        target_sector=target_sector_financials,
        market_conditions=market_conditions_bearish
    )
    print(f"\n--- Workflow Output (Final Investment Instructions for {target_ticker_jpm}) ---")
    print(workflow_output_jpm)

    print(f"\n--- Scenario 4: Running Workflow for {target_ticker_baba} ({target_sector_ecommerce}, Volatile EM Market) ---")
    workflow_output_baba = await investment_workflow.run(
        target_ticker=target_ticker_baba,
        target_sector=target_sector_ecommerce,
        market_conditions=market_conditions_volatile_em
    )
    print(f"\n--- Workflow Output (Final Investment Instructions for {target_ticker_baba}) ---")
    print(workflow_output_baba)


    # 4. (Optional) Display Team Structure
    print("\n--- (Optional) Displaying Team Structure ---")
    team_members_for_display = [
        investment_workflow.financial_data_agent, 
        investment_workflow.quantitative_analysis_agent,
        investment_workflow.risk_assessment_agent,
        investment_workflow.value_investor_agent,
        investment_workflow.growth_investor_agent,
        investment_workflow.macro_investor_agent,
        investment_workflow.contrarian_investor_agent,
        investment_workflow.portfolio_orchestration_agent
    ]
    
    investment_team_display = Team(
        name="MasterInvestmentTeamDisplay",
        agents=team_members_for_display,
        mode="collaborate",
    )
    print(f"Team Name: {investment_team_display.name}")
    print(f"Team Mode: {investment_team_display.mode}")
    member_names = [agent.name for agent in investment_team_display.agents if hasattr(agent, 'name')]
    print(f"Team Members ({len(member_names)}): {member_names}")

    print("\n--- Simulation Complete ---")

if __name__ == "__main__":
    asyncio.run(main())
