from agno.workflow import Workflow
from ..agents.specialist_agents import (
    FinancialDataAgent,
    QuantitativeAnalysisAgent,
    RiskAssessmentAgent,
    PortfolioOrchestrationAgent,
)
from ..agents.investor_agents import (
    ValueInvestorAgent,
    GrowthInvestorAgent,
    MacroInvestorAgent,
    ContrarianInvestorAgent,
)
# from agno.teams import Team # Not using team as an attribute for now

class InvestmentStrategyWorkflow(Workflow):
    name: str = "InvestmentStrategyWorkflow"
    description: str = "Workflow to analyze a stock, formulate an investment strategy, and issue instructions."

    # Instantiate agents as attributes
    financial_data_agent: FinancialDataAgent = FinancialDataAgent()
    quantitative_analysis_agent: QuantitativeAnalysisAgent = QuantitativeAnalysisAgent()
    risk_assessment_agent: RiskAssessmentAgent = RiskAssessmentAgent()
    portfolio_orchestration_agent: PortfolioOrchestrationAgent = PortfolioOrchestrationAgent()
    
    value_investor_agent: ValueInvestorAgent = ValueInvestorAgent()
    growth_investor_agent: GrowthInvestorAgent = GrowthInvestorAgent()
    macro_investor_agent: MacroInvestorAgent = MacroInvestorAgent()
    contrarian_investor_agent: ContrarianInvestorAgent = ContrarianInvestorAgent()

    async def run(self, target_ticker: str, target_sector: str, market_conditions: dict) -> dict:
        print(f"\n--- Starting Investment Strategy Workflow for {target_ticker} in Sector {target_sector} ---")
        print(f"Initial Market Conditions: {market_conditions}")
        # FUTURE: Cache financial_data or quant_analysis using self.session_state for repeated calls on the same ticker within a session.
        # self.session_state could store results like:
        # if f"{target_ticker}_data" in self.session_state:
        #     stock_data_result = self.session_state[f"{target_ticker}_data"]
        # else:
        #     stock_data_result = await self.financial_data_agent.get_stock_data(ticker=target_ticker)
        #     self.session_state[f"{target_ticker}_data"] = stock_data_result
            

        # 1. Data Gathering & Initial Analysis
        print("\n--- Workflow Step 1: Data Gathering & Quantitative Analysis ---")
        # TODO: Implement actual error handling for agent calls. (e.g., try-except blocks for network errors or tool failures)
        try:
            stock_data_result = await self.financial_data_agent.get_stock_data(ticker=target_ticker)
            print(f"Input to FinancialDataAgent: ticker='{target_ticker}'")
            print(f"Output from FinancialDataAgent for {target_ticker}: {stock_data_result}")
        except Exception as e:
            print(f"Error calling FinancialDataAgent for {target_ticker}: {e}")
            # Handle error appropriately, maybe return a failure state or default data
            return {"error": f"Failed at FinancialDataAgent for {target_ticker}: {e}", "status": "failed"}


        raw_stock_data = stock_data_result.get('data', {})
        company_info = raw_stock_data.get('company_info', {})
        stock_price_info = raw_stock_data.get('stock_price', {})

        company_profile = {
            "ticker": target_ticker,
            "name": company_info.get("name", f"{target_ticker} Name N/A"),
            "sector": company_info.get("sector", target_sector),
            "current_price": stock_price_info.get("price", "N/A"),
            "currency": stock_price_info.get("currency", "N/A")
        }
        print(f"Constructed Company Profile for {target_ticker}: {company_profile}")

        try:
            quant_analysis_result = await self.quantitative_analysis_agent.perform_quantitative_analysis(ticker=target_ticker, data=raw_stock_data)
            print(f"Input to QuantitativeAnalysisAgent: ticker='{target_ticker}', data='{raw_stock_data}'")
            print(f"Output from QuantitativeAnalysisAgent for {target_ticker}: {quant_analysis_result}")
        except Exception as e:
            print(f"Error calling QuantitativeAnalysisAgent for {target_ticker}: {e}")
            return {"error": f"Failed at QuantitativeAnalysisAgent for {target_ticker}: {e}", "status": "failed"}


        current_market_data_for_investors = {
            **market_conditions,
            f"{target_ticker}_financials": raw_stock_data,
            f"{target_ticker}_quant_signals": quant_analysis_result.get("analysis_summary", {}),
            "sector_focus": target_sector
        }
        print(f"Market Data constructed for Investor Agents: {current_market_data_for_investors}")


        # 2. Investor Analyses
        print("\n--- Workflow Step 2: Investor Analyses ---")
        investor_analyses_results = []
        
        standard_investor_agents = [
            self.value_investor_agent,
            self.growth_investor_agent,
            self.contrarian_investor_agent,
        ]
        for agent in standard_investor_agents:
            try:
                print(f"Running analysis with {agent.name} for {target_ticker}...")
                print(f"Input to {agent.name}: company_profile='{company_profile}', market_data='{current_market_data_for_investors}'")
                analysis = await agent.run_analysis(company_profile=company_profile, market_data=current_market_data_for_investors)
                investor_analyses_results.append(analysis)
                print(f"Output from {agent.name}: {analysis}")
            except Exception as e:
                print(f"Error calling {agent.name} for {target_ticker}: {e}")
                investor_analyses_results.append({"agent": agent.name, "error": str(e), "status": "failed_analysis"})


        try:
            print(f"Running analysis with {self.macro_investor_agent.name} for sector {target_sector}...")
            print(f"Input to {self.macro_investor_agent.name}: company_profile='{company_profile}', market_data='{current_market_data_for_investors}', market_sector='{target_sector}'")
            macro_analysis_result = await self.macro_investor_agent.run_analysis(
                company_profile=company_profile,
                market_data=current_market_data_for_investors,
                market_sector=target_sector
            )
            investor_analyses_results.append(macro_analysis_result)
            print(f"Output from {self.macro_investor_agent.name}: {macro_analysis_result}")
        except Exception as e:
            print(f"Error calling {self.macro_investor_agent.name} for {target_sector}: {e}")
            investor_analyses_results.append({"agent": self.macro_investor_agent.name, "error": str(e), "status": "failed_analysis"})
        

        # 3. Risk Assessment
        print("\n--- Workflow Step 3: Risk Assessment ---")
        try:
            print(f"Input to RiskAssessmentAgent: investment_proposals='{investor_analyses_results}'")
            risk_assessment_output = await self.risk_assessment_agent.assess_risk(investment_proposals=investor_analyses_results)
            print(f"Output from RiskAssessmentAgent: {risk_assessment_output}")
        except Exception as e:
            print(f"Error calling RiskAssessmentAgent: {e}")
            return {"error": f"Failed at RiskAssessmentAgent: {e}", "status": "failed"}


        # 4. Portfolio Orchestration
        print("\n--- Workflow Step 4: Portfolio Orchestration ---")
        market_overview_for_orchestrator = {
            **market_conditions,
            "quantitative_summary_for_ticker": quant_analysis_result.get("analysis_summary"),
            "macro_sector_analysis": macro_analysis_result, # Assumes macro_analysis_result is successfully populated
            "overall_risk_assessment_input": risk_assessment_output.get("overall_risk_level")
        }
        try:
            print(f"Input to PortfolioOrchestrationAgent: analyses='{investor_analyses_results}', risk_assessment='{risk_assessment_output}', market_overview='{market_overview_for_orchestrator}'")
            final_investment_instructions = await self.portfolio_orchestration_agent.generate_portfolio_recommendation(
                analyses=investor_analyses_results,
                risk_assessment=risk_assessment_output,
                market_overview=market_overview_for_orchestrator
            )
            print(f"Output from PortfolioOrchestrationAgent (Final Instructions): {final_investment_instructions}")
        except Exception as e:
            print(f"Error calling PortfolioOrchestrationAgent: {e}")
            return {"error": f"Failed at PortfolioOrchestrationAgent: {e}", "status": "failed"}

        # FUTURE: Integrate Agno Evals to test the quality of final_instructions against predefined benchmarks or historical outcomes.
        # For example:
        # evaluation_result = await self.eval_manager.evaluate(
        #     inputs={"ticker": target_ticker, "market_conditions": market_conditions},
        #     output=final_investment_instructions,
        #     expected_outcome={"recommendation_type": "Buy", "confidence_threshold": 0.7} # Simplified example
        # )
        # print(f"Evaluation result: {evaluation_result}")

        print(f"\n--- Investment Strategy Workflow for {target_ticker} Completed ---")
        return final_investment_instructions
