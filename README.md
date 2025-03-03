# WeChat Group Chat Assistant

A tool for automating the collection, summarization, and analysis of important information from WeChat group chats, designed to increase information retrieval efficiency and solve information overload problems.

## Project Overview

This project creates an assistant for WeChat group chats that can:
- Automatically receive and store messages from WeChat groups
- Process and analyze message content using AI technologies
- Generate summaries and extract key information
- Provide a user-friendly interface for viewing and searching information

## Features

- **Message Reception and Storage**
  - Capture and save group chat messages
  - Support text, images, links, and other message types
  - Maintain metadata (sender, timestamp, etc.)

- **Data Analysis and Processing**
  - Analyze group activity patterns
  - Extract keywords and important topics
  - Generate message summaries with AI

- **User Interface**
  - Clean, intuitive interface for viewing message history
  - Advanced search capabilities
  - Data visualization and analytics reports

## Technology Stack

- **Backend**: Python with Wechaty framework
- **AI Integration**: GPT API for message analysis
- **Database**: SQLite (local development), PostgreSQL (production)
- **Web Interface**: Flask/FastAPI
- **Data Analysis**: jieba, pandas, matplotlib

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- WeChat account
- Wechaty Token (for PadLocal protocol - recommended)

### Installation

1. Clone the repository
   ```
   git clone <your-repository-url>
   cd wechat-bot
   ```

2. Set up the virtual environment
   ```
   # The virtual environment is already set up in the repository
   # Activate it on Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Configure the application
   ```
   # Create a config.local.py file with your settings
   cp config.example.py config.local.py
   # Edit config.local.py with your Wechaty token and other settings
   ```

5. Start the application
   ```
   python app.py
   ```

### First-time Setup

1. After starting the application, you'll need to scan a QR code to log in to WeChat
2. Select the groups you want to monitor
3. Configure any additional settings through the web interface

## Project Structure

```
wechat-bot/
├── app/                   # Main application directory
│   ├── services/          # Core services
│   │   ├── wechaty_service.py    # Wechaty integration
│   │   ├── message_service.py    # Message processing
│   │   └── ai_service.py         # AI integration
│   ├── models/            # Data models
│   ├── utils/             # Utility functions
│   ├── templates/         # Web templates
│   └── static/            # Static assets
├── data/                  # Data storage
├── venv/                  # Python virtual environment
├── app.py                 # Application entry point
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Development Roadmap

- **Phase 1**: Basic message reception and storage
- **Phase 2**: Message analysis and summarization
- **Phase 3**: Web interface development
- **Phase 4**: Advanced features and optimizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Wechaty team for providing the WeChat bot SDK
- OpenAI for GPT API used in message analysis 