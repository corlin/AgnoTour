# AgnoTour - xAI 模型实验项目

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 简介

AgnoTour 是一个实验性项目，旨在探索和展示 xAI 模型（特别是 grok-3-beta）的能力，结合 agno 库进行文本生成和信息搜索。这个项目包含了两个主要脚本，分别用于基本的文本生成和使用工具进行信息搜索。

## 功能

- **文本生成**：使用 xAI 模型生成文本内容，例如模仿特定风格的诗歌。
- **信息搜索**：集成 DuckDuckGo 搜索工具，查询最新的信息和动态。

## 安装

要使用这个项目，您需要设置环境变量并安装必要的依赖项。以下是步骤：

```bash
# 设置 XAI API 密钥
export XAI_API_KEY=your_api_key_here

# 安装依赖项
pip install -U openai agno
pip install -U duckduckgo-search
```

## 使用方法

项目包含两个主要脚本，您可以运行它们来体验不同的功能：

- **基本文本生成**：运行 `basic.py` 脚本，使用 xAI 模型生成文本内容。
  
  ```bash
  python xai/basic.py
  ```

- **使用工具进行信息搜索**：运行 `tools_use.py` 脚本，使用 DuckDuckGo 工具查询信息。
  
  ```bash
  python xai/tools_use.py
  ```

## 贡献

欢迎对这个项目提出建议和贡献！如果您有任何想法或问题，请提交 issue 或 pull request。

## 许可证

本项目采用 MIT 许可证 - 详情请见 [LICENSE](LICENSE) 文件。

## 联系方式

如果您有任何问题或需要进一步的帮助，请联系项目维护者。
