


<img width="820" height="838" alt="Screenshot" src="https://github.com/user-attachments/assets/9d1bee09-5f2e-481e-998a-bb5a89d71345" />

# phishing-mcp-server
MCP server for phishing URL detection


# 🛡️ MCP Phishing URL Detection System

An AI-powered phishing detection system with web interface, GPT integration, and real-time URL analysis.

## 🖥️ MCP Client Setup Instructions

You can connect MCP clients (Claude desktop, VS Code Copilot, etc.) to this server for phishing URL analysis and feature extraction.

### 1. Start the MCP Server

Run the server over stdio (recommended for MCP clients):

```bash
python -m phishmcp.server
```

Or run directly from the repo root:

```bash
python phishmcp/server.py
```

### 2. Configure MCP Client

Note: This server communicates over stdio (standard input/output) using the FastMCP protocol. Most MCP clients auto-detect it when launched as a subprocess.

- Claude Desktop: Add this server via the MCP servers config, pointing to the command above.
- VS Code Copilot / MCP: Use the "MCP: Connect to Local Server" flow and select the command to run.

### 3. Available Tools

- `extract_features`: Extracts 35+ phishing detection features from a URL
- `predict`: Predicts phishing probability using extracted features and the trained model
- `load_model`: Loads or reloads the phishing detection model and feature columns

Refer to the tool descriptions in the server for details on arguments and outputs.

## 🌟 Features

- **AI-Powered Detection**: Random Forest model trained on 35+ URL features
- **Web Interface**: Beautiful, responsive web UI for easy URL analysis
- **GPT Integration**: ChatGPT-powered security advisor
- **Real-time Analysis**: Instant phishing detection with confidence scores
- **Enhanced Feature Extraction**: 35 sophisticated URL features
- **RESTful API**: Easy integration with other applications
- **Ngrok Deployment**: Remote access ready

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/phishing-mcp-server.git
   cd phishing-mcp-server
