---
title: YouTube Assistant
emoji: 🤖
colorFrom: blue
colorTo: yellow
sdk: streamlit
sdk_version: 1.44.0
app_file: app.py
pinned: false
license: mit
short_description: Generate Blogs,Notes and Summarize YouTube Video
---

# 🎬 YouTube Assistant

A powerful tool that leverages LLMs (Large Language Models) to automatically generate blogs, summaries, and study notes from YouTube videos.

## 📋 Overview

YouTube Assistant is a Streamlit-based application that extracts transcripts from YouTube videos and processes them using LLMs to create valuable content. The application follows a graph-based workflow architecture powered by LangGraph to handle different content generation use cases.

### ✨ Key Features

- **📝 Blog Generation**: Create comprehensive, well-structured blog posts from YouTube video content
- **📊 Video Summarization**: Generate concise summaries capturing the key points of YouTube videos
- **📚 Study Notes Creation**: Transform educational videos into structured learning notes
- **🔄 Multiple LLM Support**: Compatible with Anthropic, OpenAI, and Groq models
- **🧩 Modular Architecture**: Built with LangGraph for flexible workflow composition
- **🎯 User-friendly Interface**: Simple Streamlit UI for easy interaction

## 🔧 Prerequisites

Before setting up the YouTube Assistant, make sure you have:

- Python 3.8 or higher
- API keys for at least one of:
  - [OpenAI](https://platform.openai.com/account/api-keys)
  - [Anthropic](https://console.anthropic.com/settings/keys)
  - [Groq](https://console.groq.com/keys)
- A stable internet connection for accessing YouTube and API services

## 📦 Installation

Follow these steps to set up YouTube Assistant locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/suraj-yadav-aiml/youtube-assistant.git
   cd youtube-assistant
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

### Starting the Application

Run the application with:

```bash
python app.py
```

This will start the Streamlit server, and the app will be accessible in your web browser (typically at http://localhost:8501).

### Using the Application

1. **Configure the LLM**:
   - In the sidebar, select your preferred LLM provider (OpenAI, Anthropic, or Groq)
   - Choose a specific model from the available options
   - Enter your API key for the selected provider

2. **Select a Use Case**:
   - Choose from:
     - YouTube Video Blog Generation
     - YouTube Video Summarization
     - YouTube Video Notes

3. **Enter a YouTube URL**:
   - Paste the URL of the YouTube video you want to process
   - Click "Submit" to start the generation process

4. **View and Download Results**:
   - Once processing is complete, the generated content will be displayed
   - Use the "Download" button to save the content as a Markdown file

## ⚙️ Configuration

The application uses a configuration file (`uiconfigfile.ini`) to manage available options. You can modify this file to:

- Add or remove LLM providers
- Update model selections
- Change default use cases

The configuration file is located at: `src/youtube_assistant/ui/uiconfigfile.ini`

### Environment Variables

Instead of entering API keys in the UI, you can set them as environment variables:

```bash
# For OpenAI
export OPENAI_API_KEY=your_openai_api_key

# For Anthropic
export ANTHROPIC_API_KEY=your_anthropic_api_key

# For Groq
export GROQ_API_KEY=your_groq_api_key
```

## 🏗️ Project Structure

```
youtube-assistant/
├── app.py                 # Main application entry point
├── requirements.txt       # Project dependencies
├── src/
│   └── youtube_assistant/
│       ├── main.py        # Application logic
│       ├── edges/         # Graph edge definitions
│       ├── graph/         # LangGraph workflow builders
│       ├── llm/           # LLM provider implementations
│       ├── nodes/         # Processing nodes for the graph
│       ├── state/         # State management
│       └── ui/            # User interface components
```

## 🔄 How It Works

The application uses a graph-based workflow:

1. **Input Processing**: Extracts and validates the YouTube URL
2. **Transcript Extraction**: Uses YouTubeTranscriptApi to get video transcript
3. **Content Generation**: Sends transcript to the selected LLM with task-specific prompts
4. **Result Formatting**: Structures the generated content for display and download

Each use case follows a specific workflow path defined in the `GraphBuilder` class.

## 🔍 Detailed Documentation

### Available LLM Providers

- **OpenAI**: Supports models like gpt-3.5-turbo and gpt-4o
- **Anthropic**: Supports Claude models
- **Groq**: Supports various models including LLaMA and Gemma

### Use Case Details

- **Blog Generation**: Creates a comprehensive blog post with title, introduction, sections, and conclusion
- **Summarization**: Produces a concise summary with key points and takeaways
- **Notes Generation**: Formats educational content into structured study notes with highlights


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Related Resources

- [LangChain Documentation](https://python.langchain.com/docs/introduction/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [YouTube Transcript API](https://github.com/jdepoix/youtube-transcript-api)