# AI Chat Interface

A powerful and flexible chat interface built with Streamlit that supports multiple AI models and APIs.

## Features

- **Multi-API Support**
  - OpenAI API integration
  - Ollama local models support
  - Easy to extend for other APIs

- **Model Selection**
  - Switch between different OpenAI models (GPT-3.5, GPT-4)
  - Support for various Ollama models
  - Custom model configuration options

- **Privacy Mode**
  - Toggle privacy mode to start fresh conversations
  - Automatic session management
  - Persistent chat history when privacy mode is off

- **User Experience**
  - Real-time streaming responses
  - Markdown support in messages
  - Code syntax highlighting
  - Responsive design
  - Dark/Light mode support

- **Session Management**
  - Automatic session creation
  - Persistent chat history
  - Session state management
  - Privacy controls

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chat-interface
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Configure your settings:
   - Select your preferred API (OpenAI or Ollama)
   - Choose a model
   - Adjust temperature and other parameters
   - Toggle privacy mode as needed

## Configuration

### OpenAI Configuration
- Set your OpenAI API key in the `.env` file
- Available models: gpt-3.5-turbo, gpt-4, etc.

### Ollama Configuration
- Install Ollama locally
- Available models: llama2, mistral, etc.
- Configure model parameters in the UI

## Project Structure

```
chat-interface/
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
└── README.md          # This file
```

## Dependencies

- streamlit
- openai
- python-dotenv
- requests
- markdown
- streamlit-extras

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

# AI 聊天界面

一个使用 Streamlit 构建的强大且灵活的聊天界面，支持多种 AI 模型和 API。

## 功能特点

- **多 API 支持**
  - OpenAI API 集成
  - Ollama 本地模型支持
  - 易于扩展支持其他 API

- **模型选择**
  - 在 OpenAI 模型间切换（GPT-3.5、GPT-4）
  - 支持多种 Ollama 模型
  - 自定义模型配置选项

- **隐私模式**
  - 切换隐私模式开始新对话
  - 自动会话管理
  - 关闭隐私模式时保持聊天历史

- **用户体验**
  - 实时流式响应
  - 消息支持 Markdown
  - 代码语法高亮
  - 响应式设计
  - 深色/浅色模式支持

- **会话管理**
  - 自动创建会话
  - 持久化聊天历史
  - 会话状态管理
  - 隐私控制

## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd chat-interface
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 设置环境变量：
在项目根目录创建 `.env` 文件，添加以下变量：
```
OPENAI_API_KEY=your_openai_api_key
```

## 使用方法

1. 启动应用：
```bash
streamlit run app.py
```

2. 在浏览器中访问 `http://localhost:8501`

3. 配置设置：
   - 选择首选 API（OpenAI 或 Ollama）
   - 选择模型
   - 调整温度和其他参数
   - 根据需要切换隐私模式

## 配置说明

### OpenAI 配置
- 在 `.env` 文件中设置 OpenAI API 密钥
- 可用模型：gpt-3.5-turbo、gpt-4 等

### Ollama 配置
- 本地安装 Ollama
- 可用模型：llama2、mistral 等
- 在界面中配置模型参数

## 项目结构

```
chat-interface/
├── app.py              # 主应用文件
├── requirements.txt    # 项目依赖
├── .env               # 环境变量
└── README.md          # 说明文档
```

## 依赖项

- streamlit
- openai
- python-dotenv
- requests
- markdown
- streamlit-extras

## 贡献指南

1. Fork 本仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件 