from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext


@dataclass
class WeatherDependencies:
    """天气代理所需的依赖项。"""
    weather_api_key: str  # 用您的实际API密钥替换


class WeatherResult(BaseModel):
    """天气结果的模式。"""
    city: str = Field(description="城市名称")
    temperature: float = Field(description="温度（摄氏度）")
    condition: str = Field(description="天气状况（例如，晴天、雨天）")
    advice: str = Field(description="基于天气的建议")


# Define the agent
weather_agent = Agent(
    'openai:qwen-plus',
    deps_type=WeatherDependencies,
    output_type=WeatherResult,
    instructions=(
        "您是一个天气助手。提供准确的天气信息，并"
        "根据天气为用户提供实用的建议。"
    ),
)


# Tool to simulate getting weather data (replace with real API calls in production)
@weather_agent.tool
async def fetch_weather_data(ctx: RunContext[WeatherDependencies], city: str) -> dict:
    """
    模拟为指定城市获取天气数据。
    在实际应用中，这将向OpenWeatherMap等服务发出API调用。
    
    参数:
        ctx: 包含依赖项的运行时上下文。
        city: 要获取天气数据的城市名称。
    
    返回:
        包含城市天气信息的字典。
    """
    try:
        # 模拟数据 - 在生产环境中替换为实际的API调用
        weather_data = {
            "city": city,
            "temperature": 24.5,
            "condition": "sunny",
            "advice": "天气晴朗，请戴上太阳镜并保持水分充足！"
        }
        return weather_data
    except Exception as e:
        # 处理API调用中可能出现的错误
        return {
            "city": city,
            "temperature": 0.0,
            "condition": "unknown",
            "advice": f"由于错误无法获取天气数据：{str(e)}"
        }


# Simulated run examples
def run_examples():
    """演示同步和异步运行天气代理的两种方式。"""
    deps = WeatherDependencies(weather_api_key="dummy_key")
    
    # 同步运行
    print("正在同步运行...")
    sync_result = weather_agent.run_sync('里约热内卢的天气如何？', deps=deps)
    print("同步结果:", sync_result.output)
    
    # 异步运行
    import asyncio
    print("\n正在异步运行...")
    async_result = asyncio.run(weather_agent.run('东京的天气如何？', deps=deps))
    print("异步结果:", async_result.output)

if __name__ == "__main__":
    run_examples()
