import os
from pathlib import Path
from typing import Optional

from agno.agent import Agent
from agno.media import Image
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Define the query for geography identification
geo_query = """
# 地理专家任务

您是一位地理专家。您的任务是分析给定的图像，并根据可见线索提供一个合理的地点猜测，线索包括：
- 地标
- 建筑风格
- 自然特征（山脉、河流、海岸线）
- 语言或符号（文本、路标、广告牌、图片中提到的任何名称作为线索）
- 人们的服装或文化方面
- 环境线索，如天气、一天中的时间

## 返回格式
地点名称，城市，国家及推理

## 指导说明：
1. 彻底检查图像。
2. 提供一个合理的猜测，包括街道名称、城市、州和国家。
3. 详细解释您的推理，指出导致您结论的视觉线索。
4. 如果不确定，提供可能的猜测并说明理由。

## 限制和约束
1. 以中文输出结果
"""

# Initialize the GeoBuddy agent
geo_agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp"), tools=[DuckDuckGoTools()], markdown=True
)


# Function to analyze the image and return location information
def analyze_image(image_path: Path) -> Optional[str]:
    try:
        response = geo_agent.run(geo_query, images=[Image(filepath=image_path)])
        return response.content
    except Exception as e:
        raise RuntimeError(f"An error occurred while analyzing the image: {e}")
